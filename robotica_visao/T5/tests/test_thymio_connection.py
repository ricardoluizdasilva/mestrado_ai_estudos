import csv
import time
from datetime import datetime, timezone
from pathlib import Path

from thymiodirect import Thymio

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_00124B001DF456B0-if00"
)

OUTPUT = Path("data/thymio/connection_test.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

robot = Thymio(
    serial_port=PORT,
    on_connect=lambda node_id: print(
        f"Thymio ligado: {node_id}"
    ),
)

print("A estabelecer ligação...")

robot.connect()

try:
    deadline = time.monotonic() + 10
    node_id = robot.first_node()

    while node_id is None and time.monotonic() < deadline:
        time.sleep(0.2)
        node_id = robot.first_node()

    if node_id is None:
        raise RuntimeError(
            "Não foi detetado um Thymio em 10 segundos."
        )

    print("Identificador:", node_id)

    with OUTPUT.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "timestamp_utc",
            "elapsed_s",
            "prox_0",
            "prox_1",
            "prox_2",
            "prox_3",
            "prox_4",
            "prox_5",
            "prox_6",
        ])

        start = time.monotonic()

        for i in range(30):
            values = list(robot[node_id]["prox.horizontal"])

            if len(values) != 7:
                raise RuntimeError(
                    f"Leitura inválida: {values}"
                )

            elapsed = time.monotonic() - start

            writer.writerow([
                datetime.now(timezone.utc).isoformat(),
                round(elapsed, 3),
                *values,
            ])

            print(f"{i + 1:02d}: {values}")
            time.sleep(0.2)

    print("Dados guardados em:", OUTPUT)

finally:
    print("Teste terminado.")
