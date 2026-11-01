import cv2

print("OpenCV:", cv2.__version__)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

try:
    if not cap.isOpened():
        print("ERRO: webcam não disponível no WSL2.")
        raise SystemExit(1)

    ok, frame = cap.read()

    if not ok or frame is None:
        print("ERRO: não foi possível capturar uma imagem.")
        raise SystemExit(1)

    print("Webcam OK")
    print("Resolução:", frame.shape[1], "x", frame.shape[0])

    caminho = "testes/webcam_teste.jpg"
    cv2.imwrite(caminho, frame)
    print("Imagem guardada:", caminho)

finally:
    cap.release()
