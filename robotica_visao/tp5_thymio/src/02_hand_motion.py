from pathlib import Path
import time

import cv2
import mediapipe as mp
import numpy as np

# ==========================================================
# CONFIGURACAO
# ==========================================================

BASE = Path(__file__).resolve().parent.parent
MODELO = BASE / "modelos" / "hand_landmarker.task"
FRAME = Path("/mnt/c/Users/ricar/ThymioCam/frame.jpg")

ZONA_NEUTRA = 0.15
VELOCIDADE_MAX = 50
IDADE_MAXIMA = 0.75
INTERVALO_LOOP = 0.02

LIGACOES = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (0, 17),
]


def limitar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def joystick(x, y):
    """Converte a posicao do polegar em comandos virtuais."""

    horizontal = limitar((x - 0.5) * 2, -1.0, 1.0)
    vertical = limitar((0.5 - y) * 2, -1.0, 1.0)

    # Aplicar zona neutra
    if abs(horizontal) < ZONA_NEUTRA:
        horizontal = 0.0

    if abs(vertical) < ZONA_NEUTRA:
        vertical = 0.0

    # Calcular movimento linear e rotacao
    avancar = vertical * VELOCIDADE_MAX
    rodar = horizontal * VELOCIDADE_MAX

    # Calcular velocidades dos motores
    esquerda = int(round(limitar(avancar + rodar, -VELOCIDADE_MAX, VELOCIDADE_MAX)))

    direita = int(round(limitar(avancar - rodar, -VELOCIDADE_MAX, VELOCIDADE_MAX)))

    # Identificar a direcao do movimento
    if vertical == 0 and horizontal == 0:
        direcao = "PARAR"

    elif vertical == 0:
        if horizontal < 0:
            direcao = "RODAR ESQUERDA"
        else:
            direcao = "RODAR DIREITA"

    else:
        if vertical > 0:
            direcao = "AVANCAR"
        else:
            direcao = "RECUAR"

        if horizontal < 0:
            direcao += " / ESQUERDA"
        elif horizontal > 0:
            direcao += " / DIREITA"

    return esquerda, direita, direcao


def desenhar_ma(frame, pontos):
    h, w = frame.shape[:2]

    for origem, destino in LIGACOES:
        a = pontos[origem]
        b = pontos[destino]

        p1 = (int(a.x * w), int(a.y * h))
        p2 = (int(b.x * w), int(b.y * h))

        cv2.line(frame, p1, p2, (0, 255, 0), 2)

    for ponto in pontos:
        cx = int(ponto.x * w)
        cy = int(ponto.y * h)
        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

    polegar = pontos[4]

    cx = int(polegar.x * w)
    cy = int(polegar.y * h)

    cv2.circle(frame, (cx, cy), 11, (0, 0, 255), 2)

    return polegar.x, polegar.y


def desenhar_interface(frame, direcao, esquerda, direita, estado):
    h, w = frame.shape[:2]

    # Zona neutra exata: coordenadas normalizadas
    margem = ZONA_NEUTRA / 2

    x1 = int(w * (0.5 - margem))
    x2 = int(w * (0.5 + margem))
    y1 = int(h * (0.5 - margem))
    y2 = int(h * (0.5 + margem))

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

    cv2.line(frame, (w // 2, 0), (w // 2, h), (100, 100, 100), 1)

    cv2.line(frame, (0, h // 2), (w, h // 2), (100, 100, 100), 1)

    # Fundo escuro para facilitar a leitura
    cv2.rectangle(frame, (0, 0), (w, 100), (20, 20, 20), -1)

    cv2.putText(
        frame,
        f"Direcao: {direcao[:40]}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1,
    )

    cv2.putText(
        frame,
        f"Motor L: {esquerda}   R: {direita}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Estado: {estado}",
        (10, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (200, 255, 200),
        1,
    )

    return frame


def main():
    if not MODELO.is_file():
        raise FileNotFoundError(f"Modelo em falta: {MODELO}")

    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELO)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    ultimo_mtime = None
    ultimo_instante = None
    ultimo_timestamp = -1
    ultimo_log = 0.0
    estado_anterior = None

    esquerda = 0
    direita = 0
    direcao = "PARAR / SEM IMAGEM"

    frames_recebidos = 0
    frames_processados = 0
    tempo_inferencia_total = 0.0
    tempo_inferencia_max = 0.0
    inicio = time.monotonic()

    # Imagem de espera, usada mesmo sem fotogramas novos
    imagem_atual = np.zeros((480, 640, 3), dtype=np.uint8)

    print("JOYSTICK VISUAL — MODO SIMULACAO")
    print("Nenhum comando sera enviado ao Thymio.")
    print("Prima Q ou ESC para terminar.")

    try:
        with mp.tasks.vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                agora = time.monotonic()
                frame_novo = None

                try:
                    stat = FRAME.stat()
                    mtime = stat.st_mtime_ns

                    if mtime != ultimo_mtime:
                        candidato = cv2.imread(str(FRAME))

                        if candidato is not None:
                            frame_novo = candidato
                            ultimo_mtime = mtime
                            ultimo_instante = time.monotonic()

                except OSError:
                    pass

                idade = (
                    time.monotonic() - ultimo_instante
                    if ultimo_instante is not None
                    else float("inf")
                )

                if frame_novo is not None:
                    estado = "FRAME_NOVO"

                    rgb = cv2.cvtColor(frame_novo, cv2.COLOR_BGR2RGB)

                    imagem_mp = mp.Image(
                        image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)
                    )

                    timestamp = max(
                        int((time.monotonic() - inicio) * 1000), ultimo_timestamp + 1
                    )
                    ultimo_timestamp = timestamp

                    frames_recebidos += 1

                    inicio_inferencia = time.monotonic()

                    resultado = detector.detect_for_video(imagem_mp, timestamp)

                    duracao_inferencia = time.monotonic() - inicio_inferencia

                    tempo_inferencia_total += duracao_inferencia
                    tempo_inferencia_max = max(tempo_inferencia_max, duracao_inferencia)

                    frames_processados += 1

                    esquerda = 0
                    direita = 0
                    direcao = "PARAR / SEM MAO"
                    if resultado.hand_landmarks:
                        pontos = resultado.hand_landmarks[0]

                        x, y = desenhar_ma(frame_novo, pontos)

                        esquerda, direita, direcao = joystick(x, y)

                        if time.monotonic() - ultimo_log >= 1.0:
                            print(
                                f"POLEGAR: x={x:.3f}, y={y:.3f} | "
                                f"Direcao={direcao} | "
                                f"L={esquerda} R={direita}"
                            )

                    imagem_atual = frame_novo

                elif idade > IDADE_MAXIMA:
                    estado = "FRAME_DESATUALIZADO"

                    esquerda = 0
                    direita = 0
                    direcao = "PARAR / IMAGEM DESATUALIZADA"

                else:
                    estado = "AGUARDAR_PROXIMO_FRAME"

                # A janela continua visivel, mesmo sem frame novo
                imagem_visual = imagem_atual.copy()

                desenhar_interface(
                    imagem_visual,
                    direcao,
                    esquerda,
                    direita,
                    estado,
                )

                cv2.imshow("TP5 - Joystick Visual", imagem_visual)

                if estado != estado_anterior:
                    if estado == "FRAME_DESATUALIZADO":
                        print("AVISO: captura interrompida — comandos zero")

                    elif (
                        estado == "FRAME_NOVO"
                        and estado_anterior == "FRAME_DESATUALIZADO"
                    ):
                        print("Captura de vídeo restabelecida.")

                    estado_anterior = estado

                if agora - ultimo_log >= 2.0:
                    decorrido = max(time.monotonic() - inicio, 0.001)

                    fps = frames_processados / decorrido

                    media_inferencia = (
                        tempo_inferencia_total / frames_processados
                        if frames_processados > 0
                        else 0
                    )

                    print(
                        f"Estado={estado} | "
                        f"Recebidos={frames_recebidos} | "
                        f"Processados={frames_processados} | "
                        f"FPS={fps:.2f} | "
                        f"Inferencia media={media_inferencia * 1000:.1f}ms | "
                        f"Inferencia maxima={tempo_inferencia_max * 1000:.1f}ms | "
                        f"Idade={idade:.2f}s"
                    )

                    ultimo_log = agora

                tecla = cv2.waitKey(1) & 0xFF

                if tecla in (ord("q"), 27):
                    break

                time.sleep(INTERVALO_LOOP)

    finally:
        cv2.destroyAllWindows()
        print("Simulacao terminada.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupcao solicitada pelo utilizador.")
