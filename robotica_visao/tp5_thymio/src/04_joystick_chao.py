"""TP5: joystick visual + watchdog Aseba, teste de 15 s (rodas suspensas).

Reutiliza joystick(), desenhar_ma() e desenhar_interface() de 02_hand_motion.py.
As leituras de motores sao de uma cache, nao necessariamente sincronizadas com comandos.
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
FRAME = Path("/mnt/c/Users/ricar/ThymioCam/frame.jpg")
MODELO = BASE / "modelos" / "hand_landmarker.task"
ASM = BASE / "src" / "aseba" / "watchdog_chao_15.asm"
PORTA = "/dev/ttyACM0"
DURACAO_MAXIMA = 5.0
IDADE_MAXIMA = 0.5
VELOCIDADE_MAX = 15
INTERVALO_LOOP = 0.02
DETECOES_PARA_ARMAR = 3
ZONA_LATERAL = 0.15  # x no intervalo [0.425, 0.575]

sys.path.insert(0, str(BASE / "testes"))
from testar_timer_contador import encerrar  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "joystick_visual", BASE / "src" / "02_hand_motion.py"
)
if spec is None or spec.loader is None:
    raise ImportError("Nao foi possivel carregar 02_hand_motion.py")
visual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual)


def limitar(valor):
    return max(-VELOCIDADE_MAX, min(VELOCIDADE_MAX, int(valor)))


def uint16(valor):
    return int(valor) & 0xFFFF


def int16(valor):
    valor = int(valor) & 0xFFFF
    return valor - 65536 if valor >= 32768 else valor


def guardar_csv(dados):
    if not dados:
        print("Nenhuma amostra recolhida; sem CSV.")
        return
    pasta = BASE / "resultados" / "joystick"
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / ("chao_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".csv")
    with destino.open("w", newline="", encoding="utf-8") as ficheiro:
        escritor = csv.DictWriter(ficheiro, fieldnames=list(dados[0]))
        escritor.writeheader()
        escritor.writerows(dados)
    print(f"Amostras gravadas: {len(dados)}")
    print(f"CSV: {destino}")


def main():
    for ficheiro in (FRAME, MODELO, ASM, BASE / "src" / "02_hand_motion.py"):
        if not ficheiro.is_file():
            raise FileNotFoundError(ficheiro)
    if not Path(PORTA).exists():
        raise RuntimeError(f"Porta serie indisponivel: {PORTA}. Execute o preflight.")

    print("=== TP5 - MODO CHAO (EXPERIMENTAL) ===")
    print("PRIMEIRA EXECUCAO: MANTER RODAS SUSPENSAS. COMANDOS SO AVANCO/PARAGEM.")
    print(f"Duracao maxima: {DURACAO_MAXIMA}s; limite: +/-{VELOCIDADE_MAX}")

    th = Thymio(
        serial_port=PORTA,
        refreshing_rate=0.1,
        refreshing_coverage={
            "motor.left.speed",
            "motor.right.speed",
            "motor.left.target",
            "motor.right.target",
            "leds.top",
            "timer.period",
        },
    )
    node_id = None
    dados = []
    inicio = None
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELO)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    try:
        print("A ligar ao Thymio...")
        th.connect()  # A versao 0.1.2 pode bloquear se nao encontrar o robo.
        node_id = th.first_node()
        if node_id is None:
            raise RuntimeError("Thymio nao encontrado.")
        robot = th[node_id]
        conn = th.thymio_proxy.connection
        if conn is None or node_id not in conn.remote_nodes:
            raise RuntimeError("Ligacao ainda sem metadados do Thymio.")
        node = conn.remote_nodes[node_id]
        offset = node.var_total_size
        if offset + 6 > node.max_var_size:
            raise RuntimeError("Memoria Aseba insuficiente.")

        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0
        time.sleep(0.4)
        th.run_asm(node_id, ASM.read_text(encoding="utf-8"))
        time.sleep(0.5)
        print("Watchdog carregado. Iniciar ensaio visual.")

        # Nao aceitar o JPEG que ja existia antes do arranque.
        ultimo_mtime = FRAME.stat().st_mtime_ns
        ultimo_frame = None
        inicio = time.monotonic()
        ultimo_log = inicio
        ultimo_timestamp = -1
        sequencia = 0
        estado_anterior = None
        esquerda = direita = 0
        direcao = "PARAR"
        mao_detetada = False
        deteccoes_validas = 0
        imagem_atual = np.zeros((480, 640, 3), dtype=np.uint8)

        with mp.tasks.vision.HandLandmarker.create_from_options(options) as detector:
            while time.monotonic() - inicio < DURACAO_MAXIMA:
                agora = time.monotonic()
                frame_novo = None
                try:
                    stat = FRAME.stat()
                    if stat.st_mtime_ns != ultimo_mtime:
                        candidato = cv2.imread(str(FRAME))
                        if candidato is not None:
                            frame_novo = candidato
                            ultimo_mtime = stat.st_mtime_ns
                            ultimo_frame = time.monotonic()
                except OSError:
                    pass

                idade = (
                    time.monotonic() - ultimo_frame
                    if ultimo_frame is not None
                    else float("inf")
                )

                if frame_novo is not None and idade <= IDADE_MAXIMA:
                    rgb = cv2.cvtColor(frame_novo, cv2.COLOR_BGR2RGB)
                    imagem_mp = mp.Image(
                        image_format=mp.ImageFormat.SRGB,
                        data=np.ascontiguousarray(rgb),
                    )
                    timestamp = max(
                        int((time.monotonic() - inicio) * 1000), ultimo_timestamp + 1
                    )
                    ultimo_timestamp = timestamp
                    resultado = detector.detect_for_video(imagem_mp, timestamp)
                    imagem_atual = frame_novo

                    if resultado.hand_landmarks:
                        pontos = resultado.hand_landmarks[0]
                        x, y = visual.desenhar_ma(imagem_atual, pontos)
                        # Somente avancar em frente; nao rodar nem recuar.
                        # Zona neutra vertical preservada da funcao ja validada.
                        lateral_centrada = abs(x - 0.5) <= ZONA_LATERAL / 2
                        vertical = (0.5 - y) * 2
                        pedido_avanco = (
                            lateral_centrada and vertical >= visual.ZONA_NEUTRA
                        )
                        deteccoes_validas += 1
                        mao_detetada = True
                        if deteccoes_validas >= DETECOES_PARA_ARMAR and pedido_avanco:
                            #                            velocidade = max(
                            #                                0, min(VELOCIDADE_MAX, round(vertical * VELOCIDADE_MAX))
                            #                            )
                            velocidade = VELOCIDADE_MAX
                            esquerda = direita = velocidade
                            direcao = "AVANCAR"
                            estado = "AVANCO AUTORIZADO"
                            # Enviar o comando (e heartbeat) so para frame novo.
                            conn.set_variables(
                                node_id, offset + 4, [velocidade, velocidade]
                            )
                            sequencia = (sequencia % 32767) + 1
                            conn.set_variables(node_id, offset, [sequencia])
                        else:
                            esquerda = direita = 0
                            direcao = "PARAR"
                            estado = (
                                "A CONFIRMAR MAO"
                                if deteccoes_validas < DETECOES_PARA_ARMAR
                                else "CENTRO / ZONA NEUTRA"
                            )
                            conn.set_variables(node_id, offset + 4, [0, 0])
                            # Nao autorizar nova marcha a partir do centro.
                    else:
                        deteccoes_validas = 0
                        esquerda = direita = 0
                        direcao = "PARAR / SEM MAO"
                        mao_detetada = False
                        estado = "SEM MAO"
                        conn.set_variables(node_id, offset + 4, [0, 0])
                        # Sem heartbeat: watchdog expira autonomamente.
                elif idade > IDADE_MAXIMA:
                    esquerda = direita = 0
                    direcao = "PARAR / IMAGEM DESATUALIZADA"
                    mao_detetada = False
                    deteccoes_validas = 0
                    estado = "IMAGEM DESATUALIZADA"
                    # Sem heartbeat; nao confiar na imagem anterior.
                else:
                    # Apenas visualizacao; nao renovar heartbeat sem imagem nova.
                    estado = "AGUARDAR FRAME" if mao_detetada else "SEM MAO"

                imagem_visual = imagem_atual.copy()
                visual.desenhar_interface(
                    imagem_visual, direcao, esquerda, direita, estado
                )
                cv2.imshow("TP5 - Thymio REAL", imagem_visual)

                instante_leitura = time.monotonic()
                target_l = int16(robot["motor.left.target"])
                target_r = int16(robot["motor.right.target"])
                speed_l = int16(robot["motor.left.speed"])
                speed_r = int16(robot["motor.right.speed"])
                auth = int(robot["leds.top"][1])
                dados.append(
                    {
                        "tempo": round(instante_leitura - inicio, 4),
                        "estado": estado,
                        "direcao": direcao,
                        "cmd_l": esquerda,
                        "cmd_r": direita,
                        "target_l": target_l,
                        "target_r": target_r,
                        "speed_l": speed_l,
                        "speed_r": speed_r,
                        "auth": auth,
                        "idade_frame": round(idade, 4) if np.isfinite(idade) else "",
                        "frame_novo": int(frame_novo is not None),
                        "deteccoes_validas": deteccoes_validas,
                    }
                )

                if (
                    estado
                    in (
                        "SEM MAO",
                        "IMAGEM DESATUALIZADA",
                        "AVANCO AUTORIZADO",
                        "A CONFIRMAR MAO",
                        "CENTRO / ZONA NEUTRA",
                    )
                    and estado != estado_anterior
                ):
                    print("Estado:", estado)
                    estado_anterior = estado
                if instante_leitura - ultimo_log >= 1.0:
                    print(
                        f"t={instante_leitura - inicio:.1f}s | {direcao} | "
                        f"Cmd L={esquerda} R={direita} | "
                        f"Target L={target_l} R={target_r} | "
                        f"Speed L={speed_l} R={speed_r} | "
                        f"Auth={auth} | Idade={idade:.2f}s"
                    )
                    ultimo_log = instante_leitura
                tecla = cv2.waitKey(1) & 0xFF
                if tecla in (ord("q"), 27):
                    print("Paragem solicitada.")
                    break
                time.sleep(INTERVALO_LOOP)
        print("Fim do ensaio.")
    finally:
        cv2.destroyAllWindows()
        try:
            encerrar(th, node_id)
        finally:
            guardar_csv(dados)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupcao solicitada pelo utilizador.")
