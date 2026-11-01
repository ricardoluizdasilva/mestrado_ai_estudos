"""TP5 exercício 5: PID diferencial 2D com proteção IR em Python.

Segurança: executar PRIMEIRO com as rodas suspensas; testar em local livre.
Reutiliza a captura Windows, o HandLandmarker e o watchdog Aseba de ±200.
As coordenadas X/Y do polegar (landmark 4) produzem referências
de velocidade linear e de rotação. Dois PID usam as velocidades medidas.
Na zona central, sem mão/frame recente, ou com obstáculo detetado na direção
do movimento, o comando é zero; em bloqueio, os estados PID são reiniciados.
"""
import csv
import importlib.util
import math
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
FRAME = Path('/mnt/c/Users/ricar/ThymioCam/frame.jpg')
MODELO = BASE / 'modelos' / 'hand_landmarker.task'
ASM = BASE / 'src/aseba/watchdog_joystick_200.asm'
PORTA = '/dev/ttyACM0'

# Primeiro teste apenas com rodas suspensas, preferencialmente até ±60.
REFERENCIA_LINEAR_MAX = 150   # avanço / recuo em unidades Thymio
REFERENCIA_ROTACAO_MAX = 110  # rotação 2D calibrada
REFERENCIA_RODA_MAX = 180     # limite total por roda, inferior a 150+110
COMANDO_MAX = 200        # limita saída PID; watchdog também limita a ±200
ZONA_NEUTRA = 0.15      # eixo vertical, igual ao ensaio anterior
CENTRO_X = 0.50          # ajustar apenas se a zona neutra visual estiver deslocada
DESVIO_NEUTRO_X = 0.025  # tolerancia horizontal: 2,5% da largura da imagem
DESVIO_MAX_X = 0.18     # saturacao a 18% da largura: baseado no CSV anterior
IDADE_MAXIMA = 0.5
DETECOES_PARA_ARMAR = 3
INTERVALO_LOOP = 0.02
DT_MIN, DT_MAX = 0.04, 0.4

# Valores iniciais retirados dos ensaios P/PI/PID do exercício 3; calibrar.
KP, KI, KD = 0.30, 0.05, 0.01
INTEGRAL_MAX = 250.0
REFERENCIA_MIN_ATIVA = 45  # evita referencias quase nulas fora da zona neutra
COMANDO_MIN_ATIVO = 40      # inspirado na v10; aplicar apenas quando ha movimento pedido
RAMPA_COMANDO = 25         # variacao maxima por novo fotograma, por motor

# Filtro IR validado funcionalmente na versao 10; aplicacao no Python.
LIMIAR_BLOQUEIO = 2200
LIMIAR_LIBERTACAO = 1400

sys.path.insert(0, str(BASE / 'testes'))
from testar_timer_contador import encerrar  # noqa: E402

spec = importlib.util.spec_from_file_location('joystick_visual', BASE / 'src' / '02_hand_motion.py')
if spec is None or spec.loader is None:
    raise ImportError('02_hand_motion.py nao encontrado')
visual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual)


def signed16(value):
    value = int(value) & 0xffff
    return value - 65536 if value >= 32768 else value


def unsigned16(value):
    return int(value) & 0xffff


@dataclass
class PID:
    kp: float = KP
    ki: float = KI
    kd: float = KD
    integral: float = 0.0
    erro_anterior: float = 0.0
    anterior_valido: bool = False

    def reset(self):
        self.integral = 0.0
        self.erro_anterior = 0.0
        self.anterior_valido = False

    def calcular(self, referencia, medida, dt):
        """PID de correção + feedforward, com anti-windup por integração condicional.

        O alvo de motor já tem um regulador interno; esta é uma malha externa
        experimental. A derivada é calculada no erro e pode amplificar ruído.
        """
        erro = referencia - medida
        derivada = ((erro - self.erro_anterior) / dt) if self.anterior_valido else 0.0
        candidato_i = max(-INTEGRAL_MAX, min(INTEGRAL_MAX, self.integral + erro * dt))
        sem_saturar = referencia + self.kp * erro + self.ki * candidato_i + self.kd * derivada
        limitado = max(-COMANDO_MAX, min(COMANDO_MAX, sem_saturar))
        # Não aumentar a integração enquanto estiver saturado no sentido do erro.
        saturado_a_favor = (sem_saturar > COMANDO_MAX and erro > 0) or (
            sem_saturar < -COMANDO_MAX and erro < 0)
        if not saturado_a_favor:
            self.integral = candidato_i
        self.erro_anterior = erro
        self.anterior_valido = True
        return int(round(limitado)), erro, self.integral, derivada


def eixo_normalizado(coordenada):
    """Centro=0, banda morta, amplitude útil normalizada para [-1, 1]."""
    eixo = max(-1.0, min(1.0, 2.0 * (0.5 - float(coordenada))))
    if abs(eixo) <= ZONA_NEUTRA:
        return 0.0
    return math.copysign((abs(eixo) - ZONA_NEUTRA) / (1.0 - ZONA_NEUTRA), eixo)


def eixo_horizontal(x):
    """Calibra o movimento horizontal para a amplitude REAL observada.

    Em x=CENTRO_X a saida e zero; nos extremos definidos por
    DESVIO_MAX_X atinge +/-1. Nao altera o eixo vertical.
    """
    deslocamento = CENTRO_X - float(x)
    amplitude = abs(deslocamento)
    if amplitude <= DESVIO_NEUTRO_X:
        return 0.0
    ganho = (amplitude - DESVIO_NEUTRO_X) / (DESVIO_MAX_X - DESVIO_NEUTRO_X)
    return math.copysign(min(1.0, ganho), deslocamento)


def referencias_mediapipe(x, y):
    """Y positivo -> avançar; X positivo (polegar à esquerda) -> virar à esquerda.

    ref esquerda = linear - rotação; ref direita = linear + rotação.
    Polegar ao centro dos dois eixos -> ambas referências zero.
    """
    linear = int(round(REFERENCIA_LINEAR_MAX * eixo_normalizado(y)))
    rotacao = int(round(REFERENCIA_ROTACAO_MAX * eixo_horizontal(x)))
    ref_l = max(-REFERENCIA_RODA_MAX, min(REFERENCIA_RODA_MAX, linear - rotacao))
    ref_r = max(-REFERENCIA_RODA_MAX, min(REFERENCIA_RODA_MAX, linear + rotacao))
    # Arranque util a partir de um gesto fora da zona neutra, preservando
    # a possibilidade de uma roda ficar realmente parada numa curva.
    if ref_l:
        ref_l = int(math.copysign(max(abs(ref_l), REFERENCIA_MIN_ATIVA), ref_l))
    if ref_r:
        ref_r = int(math.copysign(max(abs(ref_r), REFERENCIA_MIN_ATIVA), ref_r))
    return linear, rotacao, ref_l, ref_r


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


def gravar(dados):
    pasta = BASE / 'resultados' / 'pid_mediapipe'
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / f'pid_2d_ir_v18_{datetime.now():%Y%m%d_%H%M%S_%f}.csv'
    if dados:
        with destino.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=dados[0].keys())
            writer.writeheader()
            writer.writerows(dados)
        print(f'Amostras: {len(dados)}; CSV: {destino}')
    else:
        print('Sem amostras para gravar.')


def main():
    for caminho in (FRAME, MODELO, ASM, BASE / 'src/02_hand_motion.py'):
        if not caminho.is_file():
            raise FileNotFoundError(caminho)
    if time.time() - FRAME.stat().st_mtime > 3.0:
        raise RuntimeError('A imagem da webcam está desatualizada; iniciar capturar_webcam.py no Windows')

    print('=== TP5 EXERCÍCIO 5 — PID 2D + OBSTACULOS (v18) ===')
    print('ATENÇÃO: PRIMEIRA EXECUÇÃO COM AS RODAS SUSPENSAS.')
    print(f'Linear ±{REFERENCIA_LINEAR_MAX}; rotação ±{REFERENCIA_ROTACAO_MAX}; comando ±{COMANDO_MAX}.')
    print(f'Eixo X: centro={CENTRO_X}, neutra=±{DESVIO_NEUTRO_X}, saturação=±{DESVIO_MAX_X}.')
    print('Watchdog Aseba ±200; bloqueio IR Python; mínimo=40, rampa=25; Q/Esc.')
    print(f'PID: Kp={KP}, Ki={KI}, Kd={KD}. Centro de ambos os eixos = PARAR.')
    th = Thymio(
        serial_port=PORTA,
        refreshing_rate=0.1,
        refreshing_coverage={
            'motor.left.target', 'motor.right.target',
            'motor.left.speed', 'motor.right.speed', 'leds.top', 'timer.period', 'prox.horizontal'
        }
    )
    opcoes = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELO)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    nid = None
    dados = []
    try:
        th.connect()
        nid = th.first_node()
        if nid is None:
            raise RuntimeError('Thymio não encontrado')
        robot = th[nid]
        conn = th.thymio_proxy.connection
        node = conn.remote_nodes[nid]
        offset = node.var_total_size
        if offset + 6 > node.max_var_size:
            raise RuntimeError('Memória Aseba insuficiente')
        robot['motor.left.target'] = 0
        robot['motor.right.target'] = 0
        time.sleep(0.4)
        th.run_asm(nid, ASM.read_text(encoding='utf-8'))
        time.sleep(0.5)
        print('Watchdog carregado; mãos fora da câmara no início.')

        pid_l, pid_r = PID(), PID()
        bloqueador = BloqueioObstaculos()
        bloqueio_ir = "LIVRE"
        ir_frente = ir_tras = None
        contador = 0
        sequencia = 0
        ultimo_mtime = FRAME.stat().st_mtime_ns
        ultimo_frame = None
        ultimo_pid = None
        ultimo_timestamp = -1
        inicio = time.monotonic()
        ultimo_log = inicio
        status = 'SEM MAO'
        referencia_l = referencia_r = linear = rotacao = cmd_l = cmd_r = 0
        aplicado_l = aplicado_r = 0
        erro_l = erro_r = 0.0
        integral_l = integral_r = 0.0
        derivada_l = derivada_r = 0.0
        x_polegar = y_polegar = None
        tela = np.zeros((480, 640, 3), dtype=np.uint8)

        with mp.tasks.vision.HandLandmarker.create_from_options(opcoes) as detector:
            while True:
                agora = time.monotonic()
                frame = None
                try:
                    stat = FRAME.stat()
                    if stat.st_mtime_ns != ultimo_mtime:
                        possivel = cv2.imread(str(FRAME))
                        if possivel is not None:
                            frame = possivel
                            ultimo_mtime = stat.st_mtime_ns
                            ultimo_frame = agora
                except OSError:
                    pass
                idade = (agora - ultimo_frame) if ultimo_frame is not None else math.inf
                valido = frame is not None and idade <= IDADE_MAXIMA

                if valido:
                    tela = frame
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    imagem_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
                    timestamp = max(int((agora - inicio) * 1000), ultimo_timestamp + 1)
                    ultimo_timestamp = timestamp
                    resultado = detector.detect_for_video(imagem_mp, timestamp)
                    if resultado.hand_landmarks:
                        contador += 1
                        x, y = visual.desenhar_ma(tela, resultado.hand_landmarks[0])
                        x_polegar, y_polegar = float(x), float(y)
                        linear, rotacao, referencia_l, referencia_r = referencias_mediapipe(x, y)
                        if contador >= DETECOES_PARA_ARMAR and (referencia_l != 0 or referencia_r != 0):
                            dt = (agora - ultimo_pid) if ultimo_pid is not None else 0.1
                            dt = max(DT_MIN, min(DT_MAX, dt))
                            ultimo_pid = agora
                            medida_l = signed16(robot['motor.left.speed'])
                            medida_r = signed16(robot['motor.right.speed'])
                            cmd_l, erro_l, integral_l, derivada_l = pid_l.calcular(referencia_l, medida_l, dt)
                            cmd_r, erro_r, integral_r, derivada_r = pid_r.calcular(referencia_r, medida_r, dt)
                            # Mínimo físico por roda ativa, sem alterar a direção pedida.
                            # A rampa limita arranque/aceleração; zero, perda da mão e
                            # bloqueio IR NÃO passam pela rampa.
                            def preparar_comando(cmd, ref, anterior):
                                if ref == 0:
                                    return 0
                                # O PID continua em malha fechada: apenas se evita
                                # um comando incapaz de vencer o atrito.
                                cmd = int(math.copysign(max(abs(cmd), COMANDO_MIN_ATIVO), ref))
                                cmd = max(-COMANDO_MAX, min(COMANDO_MAX, cmd))
                                return max(anterior - RAMPA_COMANDO,
                                           min(anterior + RAMPA_COMANDO, cmd))
                            cmd_l = preparar_comando(cmd_l, referencia_l, aplicado_l)
                            cmd_r = preparar_comando(cmd_r, referencia_r, aplicado_r)
                            # Filtrar as saídas PID com a mesma regra de segurança da v10.
                            # Os motores podem diferir da referencia durante transitorios;
                            # por isso, usar tanto as referencias como os comandos para
                            # identificar movimentos perigosos.
                            try:
                                leituras = robot['prox.horizontal']
                                pedido_l = cmd_l if cmd_l != 0 else referencia_l
                                pedido_r = cmd_r if cmd_r != 0 else referencia_r
                                permitido_l, permitido_r, bloqueio_ir, ir_frente, ir_tras = bloqueador.aplicar(
                                    pedido_l, pedido_r, leituras
                                )
                            except (KeyError, TypeError, ValueError, IndexError):
                                permitido_l = permitido_r = 0
                                bloqueio_ir = 'ERRO LEITURA IR - PARAR'
                                ir_frente = ir_tras = None
                            # Se algum bloqueio foi acionado, ambos os motores param e
                            # ambos os PID perdem os estados integral/derivativo.
                            if bloqueio_ir != 'LIVRE':
                                cmd_l = cmd_r = 0
                                aplicado_l = aplicado_r = 0
                                pid_l.reset(); pid_r.reset(); ultimo_pid = None
                                erro_l = erro_r = integral_l = integral_r = derivada_l = derivada_r = 0.0
                            status = ('AVANÇAR / PID 2D' if linear > 0 else 'RECUAR / PID 2D' if linear < 0
                                      else 'RODAR / PID 2D')
                            if bloqueio_ir != 'LIVRE':
                                status = 'PARAR / ' + bloqueio_ir
                            aplicado_l, aplicado_r = cmd_l, cmd_r
                            conn.set_variables(nid, offset+4, [unsigned16(cmd_l), unsigned16(cmd_r)])
                            sequencia = (sequencia % 32767) + 1
                            conn.set_variables(nid, offset, [sequencia])
                        else:
                            cmd_l = cmd_r = 0
                            aplicado_l = aplicado_r = 0
                            bloqueio_ir = 'LIVRE'
                            pid_l.reset(); pid_r.reset(); ultimo_pid = None
                            erro_l = erro_r = integral_l = integral_r = derivada_l = derivada_r = 0.0
                            status = 'ZONA CENTRAL — PARAR' if referencia_l == 0 and referencia_r == 0 else 'A CONFIRMAR MAO'
                            conn.set_variables(nid, offset+4, [0, 0])
                            # Centro: enviar heartbeat para aplicar zero; espera deixa watchdog expirar.
                            sequencia = (sequencia % 32767) + 1
                            conn.set_variables(nid, offset, [sequencia])
                    else:
                        contador = 0
                        referencia_l = referencia_r = linear = rotacao = cmd_l = cmd_r = 0
                        x_polegar = y_polegar = None
                        bloqueio_ir = 'LIVRE'
                        pid_l.reset(); pid_r.reset(); ultimo_pid = None
                        status = 'SEM MAO — PARAR'
                        conn.set_variables(nid, offset+4, [0, 0])
                        # Sem heartbeat: watchdog corta o movimento autonomamente.
                elif idade > IDADE_MAXIMA:
                    contador = 0
                    referencia_l = referencia_r = linear = rotacao = cmd_l = cmd_r = 0
                    x_polegar = y_polegar = None
                    bloqueio_ir = 'LIVRE'
                    pid_l.reset(); pid_r.reset(); ultimo_pid = None
                    status = 'FRAME ANTIGO — PARAR'
                    # Sem heartbeat: watchdog corta o movimento autonomamente.

                velocidade_l = signed16(robot['motor.left.speed'])
                velocidade_r = signed16(robot['motor.right.speed'])
                alvo_l = signed16(robot['motor.left.target'])
                alvo_r = signed16(robot['motor.right.target'])
                autorizacao = int(robot['leds.top'][1])
                dados.append({
                    'tempo_s': round(agora - inicio, 4), 'frame_novo': int(valido),
                    'estado': status,
                    'x_polegar': round(x_polegar, 4) if x_polegar is not None else '',
                    'y_polegar': round(y_polegar, 4) if y_polegar is not None else '',
                    'linear': linear, 'rotacao': rotacao,
                    'ref_l': referencia_l, 'ref_r': referencia_r, 'cmd_l': cmd_l, 'cmd_r': cmd_r,
                    'target_l': alvo_l, 'target_r': alvo_r,
                    'speed_l': velocidade_l, 'speed_r': velocidade_r,
                    'erro_l': round(erro_l, 3), 'erro_r': round(erro_r, 3),
                    'integral_l': round(integral_l, 3), 'integral_r': round(integral_r, 3),
                    'derivada_l': round(derivada_l, 3), 'derivada_r': round(derivada_r, 3),
                    'auth': autorizacao, 'bloqueio_ir': bloqueio_ir,
                    'ir_frente_max': ir_frente if ir_frente is not None else '',
                    'ir_tras_max': ir_tras if ir_tras is not None else '',
                    'idade_frame': round(idade, 4) if math.isfinite(idade) else '',
                })
                visual.desenhar_interface(tela, status, cmd_l, cmd_r,
                                         f'PID refs={referencia_l}/{referencia_r} | v={velocidade_l}/{velocidade_r}')
                cv2.imshow('TP5 - Exercício 5 - PID MediaPipe', tela)
                tecla = cv2.waitKey(1) & 0xFF
                if tecla in (ord('q'), 27):
                    print('Paragem pelo teclado.')
                    break
                if agora - ultimo_log >= 1.0:
                    print(f't={agora-inicio:.1f}s {status} refs={referencia_l}/{referencia_r} '
                          f'cmd={cmd_l}/{cmd_r} speed={velocidade_l}/{velocidade_r} '
                          f'auth={autorizacao} IR={ir_frente}/{ir_tras} bloqueio={bloqueio_ir}')
                    ultimo_log = agora
                time.sleep(INTERVALO_LOOP)
    except KeyboardInterrupt:
        print('Interrupção manual (Ctrl+C).')
    finally:
        cv2.destroyAllWindows()
        try:
            if nid is not None:
                encerrar(th, nid)
            else:
                try: th.disconnect()
                except Exception: pass
        finally:
            gravar(dados)


if __name__ == '__main__':
    main()
