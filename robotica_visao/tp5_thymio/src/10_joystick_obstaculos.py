"""TP5: joystick visual de 2 motores, com watchdog Aseba (teste supervisionado).
Executar a partir do ambiente Conda thymio no WSL2. Apenas em area desimpedida.
"""
import csv
import importlib.util
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
FRAME = Path('/mnt/c/Users/ricar/ThymioCam/frame.jpg')
MODELO = BASE / 'modelos' / 'hand_landmarker.task'
ASM = BASE / 'src' / 'aseba' / 'watchdog_joystick_200.asm'  # limite independente +/-200
PORTA = '/dev/ttyACM0'
VELOCIDADE_MAX = 3000  # escala VIRTUAL do joystick, nunca enviar ao motor
VELOCIDADE_MIN = 300   # limiar VIRTUAL abaixo do qual o motor fica parado
MOTOR_MAX = 200        # limite do comando fisico Thymio
MOTOR_MIN = 40         # comando minimo para vencer atrito (calibravel)
PASSO_RAMP = 15        # variacao maxima por novo fotograma; paragem imediata
IDADE_MAXIMA = 0.5
DETECOES_PARA_ARMAR = 3
INTERVALO_LOOP = 0.02
# Valores brutos dos sensores IR horizontais; calibrar no local.
LIMIAR_BLOQUEIO = 2200
LIMIAR_LIBERTACAO = 1400  # histerese evita alternancias rapidas


sys.path.insert(0, str(BASE / 'testes'))
from testar_timer_contador import encerrar  # noqa: E402

spec = importlib.util.spec_from_file_location('joystick_visual', BASE / 'src' / '02_hand_motion.py')
if spec is None or spec.loader is None:
    raise ImportError('02_hand_motion.py nao encontrado')
visual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual)


def signed16(v):
    n = int(v) & 0xFFFF
    return n - 65536 if n >= 32768 else n


def unsigned16(v):
    return int(v) & 0xFFFF


def limitar_virtual(v):
    return max(-VELOCIDADE_MAX, min(VELOCIDADE_MAX, int(v)))


def rampa(atual, desejado):
    # Nunca atrasar uma paragem ou inverter o sentido sem passar por zero.
    if desejado == 0:
        return 0
    if atual * desejado < 0:
        return 0
    return atual + max(-PASSO_RAMP, min(PASSO_RAMP, desejado - atual))


def converter_para_motor(valor_virtual):
    """Converte 0..3000 virtuais em 0 ou 40..200 motores, preservando sinal.

    Limiar inclusivo: magnitudes menores que 300 ficam a zero.
    O watchdog Aseba limita independentemente os motores a +/-200.
    """
    magnitude = min(abs(int(valor_virtual)), VELOCIDADE_MAX)
    if magnitude < VELOCIDADE_MIN:
        return 0
    fracao = (magnitude - VELOCIDADE_MIN) / (VELOCIDADE_MAX - VELOCIDADE_MIN)
    saida = MOTOR_MIN + round(fracao * (MOTOR_MAX - MOTOR_MIN))
    return (1 if valor_virtual > 0 else -1) * saida


class BloqueioObstaculos:
    """Bloqueia comandos para a direcao do obstaculo; falha de leitura = parar.

    prox.horizontal: 0..4 sensores da frente, 5..6 da retaguarda.
    O bloqueio e realizado no PC, nao e uma protecao autonomamente embarcada.
    """

    def __init__(self):
        self.frente = False
        self.tras = False

    def aplicar(self, esquerda, direita, proximidade):
        try:
            valores = [int(v) for v in proximidade]
            if len(valores) != 7 or any(v < 0 for v in valores):
                raise ValueError('dados de proximidade invalidos')
        except (TypeError, ValueError, IndexError):
            return 0, 0, 'SENSORES INVALIDOS - PARAR', None, None

        frente = max(valores[:5])
        tras = max(valores[5:])
        self.frente = frente >= (LIMIAR_LIBERTACAO if self.frente else LIMIAR_BLOQUEIO)
        self.tras = tras >= (LIMIAR_LIBERTACAO if self.tras else LIMIAR_BLOQUEIO)
        # Um motor positivo pode deslocar a dianteira em direcao ao obstaculo.
        # Um motor negativo pode deslocar a retaguarda em direcao ao obstaculo.
        # Por precaucao, imobilizar ambos os motores, incluindo rotacoes.
        perigo_frente = self.frente and (esquerda > 0 or direita > 0)
        perigo_tras = self.tras and (esquerda < 0 or direita < 0)
        if perigo_frente or perigo_tras:
            etiqueta = 'OBSTACULO FRENTE' if perigo_frente else 'OBSTACULO TRAS'
            return 0, 0, etiqueta, frente, tras
        return esquerda, direita, 'LIVRE', frente, tras


def guardar(dados):
    if not dados:
        print('Sem amostras para gravar.')
        return
    pasta = BASE / 'resultados' / 'joystick'
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / f'joystick_obstaculos_{datetime.now():%Y%m%d_%H%M%S_%f}.csv'
    with caminho.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(dados[0]))
        writer.writeheader()
        writer.writerows(dados)
    print(f'Amostras: {len(dados)}')
    print('CSV:', caminho)


def main():
    for caminho in (FRAME, MODELO, ASM):
        if not caminho.is_file():
            raise FileNotFoundError(caminho)

    print('=== TP5 - JOYSTICK 200 + OBSTACULOS / TESTE SUPERVISIONADO ===')
    print(f'Escala virtual +/-{VELOCIDADE_MAX}; motor +/-{MOTOR_MAX}; sem limite de duracao; Q ou ESC para terminar')
    print(f'Limiar virtual: {VELOCIDADE_MIN}; minimo motor: {MOTOR_MIN}; rampa/frame: {PASSO_RAMP}')
    print('Area plana e livre; manter botao fisico do Thymio acessivel.')
    print('Iniciar com a mao fora da imagem; depois levar ao centro. Sem supervisao autonoma.')
    th = Thymio(
        serial_port=PORTA,
        refreshing_rate=0.1,
        refreshing_coverage={
            'motor.left.target', 'motor.right.target',
            'motor.left.speed', 'motor.right.speed', 'leds.top', 'timer.period', 'prox.horizontal'
        },
    )
    node_id = None
    dados = []
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELO)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    try:
        print('A ligar...')
        th.connect()  # requer preflight e porta serie valida
        node_id = th.first_node()
        if node_id is None:
            raise RuntimeError('Thymio nao encontrado')
        robot = th[node_id]
        conn = th.thymio_proxy.connection
        node = conn.remote_nodes[node_id]
        offset = node.var_total_size
        if offset + 6 > node.max_var_size:
            raise RuntimeError('Memoria Aseba insuficiente')
        robot['motor.left.target'] = 0
        robot['motor.right.target'] = 0
        time.sleep(0.4)
        th.run_asm(node_id, ASM.read_text(encoding='utf-8'))
        time.sleep(0.5)
        print('Watchdog carregado. Primeiro posicionar o polegar no centro.')

        st_inicial = FRAME.stat()
        if time.time() - st_inicial.st_mtime > 3.0:
            raise RuntimeError('Captura Windows desatualizada: reinicie capturar_webcam.py')
        ultimo_mtime = st_inicial.st_mtime_ns
        ultimo_frame = None
        inicio = time.monotonic()
        ultimo_log = inicio
        ultimo_timestamp = -1
        sequencia = 0
        deteccoes = 0
        ultimo_estado_visivel = None
        comando_l = comando_r = 0
        bloqueador = BloqueioObstaculos()
        bloqueio_atual = 'LIVRE'
        ir_frente = ir_tras = None
        direcao = 'PARAR'
        estado = 'SEM IMAGEM NOVA'
        imagem_atual = np.zeros((480, 640, 3), dtype=np.uint8)

        with mp.tasks.vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                agora = time.monotonic()
                novo = None
                try:
                    st = FRAME.stat()
                    if st.st_mtime_ns != ultimo_mtime:
                        candidato = cv2.imread(str(FRAME))
                        if candidato is not None:
                            novo = candidato
                            ultimo_mtime = st.st_mtime_ns
                            ultimo_frame = time.monotonic()
                except OSError:
                    pass
                idade = (time.monotonic() - ultimo_frame) if ultimo_frame is not None else float('inf')

                if novo is not None and idade <= IDADE_MAXIMA:
                    rgb = cv2.cvtColor(novo, cv2.COLOR_BGR2RGB)
                    mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
                    timestamp = max(int((time.monotonic() - inicio) * 1000), ultimo_timestamp + 1)
                    ultimo_timestamp = timestamp
                    resposta = detector.detect_for_video(mp_frame, timestamp)
                    imagem_atual = novo
                    if resposta.hand_landmarks:
                        deteccoes += 1
                        x, y = visual.desenhar_ma(imagem_atual, resposta.hand_landmarks[0])
                        if deteccoes >= DETECOES_PARA_ARMAR:
                            l, r, direcao = visual.joystick(x, y)
                            pedido_l = limitar_virtual(round(l * VELOCIDADE_MAX / visual.VELOCIDADE_MAX))
                            pedido_r = limitar_virtual(round(r * VELOCIDADE_MAX / visual.VELOCIDADE_MAX))
                            comando_l = rampa(comando_l, converter_para_motor(pedido_l))
                            comando_r = rampa(comando_r, converter_para_motor(pedido_r))
                            estado = 'MAO CONFIRMADA'
                            try:
                                sensor = robot['prox.horizontal']
                                comando_l, comando_r, bloqueio_atual, ir_frente, ir_tras = bloqueador.aplicar(
                                    comando_l, comando_r, sensor
                                )
                            except (KeyError, TypeError, ValueError, IndexError):
                                comando_l = comando_r = 0
                                bloqueio_atual = 'ERRO LEITURA IR - PARAR'
                                ir_frente = ir_tras = None
                            if bloqueio_atual != 'LIVRE':
                                estado = bloqueio_atual
                                direcao = 'PARAR / ' + bloqueio_atual
                            # Unica via de motor: memoria supervisionada; comando antes do heartbeat.
                            conn.set_variables(node_id, offset + 4, [unsigned16(comando_l), unsigned16(comando_r)])
                            sequencia = (sequencia % 32767) + 1
                            conn.set_variables(node_id, offset, [sequencia])
                        else:
                            comando_l = comando_r = 0
                            direcao = 'PARAR / A CONFIRMAR MAO'
                            estado = 'A CONFIRMAR MAO'
                            conn.set_variables(node_id, offset + 4, [0, 0])
                    else:
                        deteccoes = 0
                        comando_l = comando_r = 0
                        direcao = 'PARAR / SEM MAO'
                        estado = 'SEM MAO'
                        conn.set_variables(node_id, offset + 4, [0, 0])
                        # Nao renovar heartbeat: watchdog autonomo expira.
                elif idade > IDADE_MAXIMA:
                    deteccoes = 0
                    comando_l = comando_r = 0
                    direcao = 'PARAR / FRAME ANTIGO'
                    estado = 'IMAGEM DESATUALIZADA'
                    # Nao renovar heartbeat.
                else:
                    estado = 'AGUARDAR NOVO FRAME'
                    # Preservar apenas visualizacao; nao enviar heartbeat.

                instante = time.monotonic()
                alvo_l = signed16(robot['motor.left.target'])
                alvo_r = signed16(robot['motor.right.target'])
                vel_l = signed16(robot['motor.left.speed'])
                vel_r = signed16(robot['motor.right.speed'])
                auth = int(robot['leds.top'][1])
                dados.append({
                    'tempo': round(instante - inicio, 4), 'estado': estado, 'direcao': direcao,
                    'cmd_l': comando_l, 'cmd_r': comando_r, 'target_l': alvo_l,
                    'target_r': alvo_r, 'speed_l': vel_l, 'speed_r': vel_r,
                    'auth': auth, 'idade_frame': round(idade, 4) if np.isfinite(idade) else '',
                    'frame_novo': int(novo is not None), 'deteccoes_validas': deteccoes,
                    'bloqueio_ir': bloqueio_atual, 'ir_frente_max': ir_frente,
                    'ir_tras_max': ir_tras,
                })
                imagem_visual = imagem_atual.copy()
                visual.desenhar_interface(imagem_visual, direcao, comando_l, comando_r, estado)
                cv2.imshow('TP5 - Thymio joystick 200 + obstaculos', imagem_visual)
                if estado in ('SEM MAO', 'IMAGEM DESATUALIZADA', 'MAO CONFIRMADA', 'A CONFIRMAR MAO', 'OBSTACULO FRENTE', 'OBSTACULO TRAS', 'SENSORES INVALIDOS - PARAR', 'ERRO LEITURA IR - PARAR'):
                    if estado != ultimo_estado_visivel:
                        print('Estado:', estado)
                        ultimo_estado_visivel = estado
                if instante - ultimo_log >= 1:
                    print(f't={instante-inicio:.1f}s {direcao} Cmd={comando_l}/{comando_r} Alvos={alvo_l}/{alvo_r} Vel={vel_l}/{vel_r} Auth={auth} IR={ir_frente}/{ir_tras} Bloqueio={bloqueio_atual}')
                    ultimo_log = instante
                key = cv2.waitKey(1) & 0xFF
                if key in (ord('q'), 27):
                    print('Interrompido pelo teclado')
                    break
                time.sleep(INTERVALO_LOOP)
        print('Fim do controlo')
    finally:
        cv2.destroyAllWindows()
        try:
            encerrar(th, node_id)
        finally:
            guardar(dados)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupcao solicitada pelo utilizador.')
