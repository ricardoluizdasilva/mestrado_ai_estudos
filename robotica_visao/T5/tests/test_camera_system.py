from picamera2 import Picamera2
from pathlib import Path
import time

output = Path(
    "/dados/projetos/mestrado_ai_estudos/"
    "robotica_visao/T5/data/camera/test_capture.jpg"
)

camera = Picamera2()

config = camera.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

try:
    camera.configure(config)
    camera.start()

    time.sleep(2)

    camera.capture_file(str(output))

    print("Captura concluída")
    print("Ficheiro:", output)
    print("Tamanho:", output.stat().st_size, "bytes")
finally:
    camera.stop()
    camera.close()
