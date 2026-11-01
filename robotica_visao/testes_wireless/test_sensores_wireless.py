import csv
import time
from datetime import datetime, timezone
from pathlib import Path
from thymiodirect import Thymio

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

OUTPUT = Path("sensores_wireless.csv")
DURATION = 10

robot = Thymio(
    serial_port=PORT,
    refreshing_rate=0.2,
    refreshing_coverage={"prox.horizontal"},
    on_connect=lambda node_id: print(
        f"Thymio conectado: {node_id}", flush=True
    ),
)

print("A estabelecer comunicação...", flush=True)
robot.connect()

node_id = robot.first_node()
print("ID:", node_id, flush=True)

samples = []
start = time.monotonic()

def observer(updated_node_id):
    if updated_node_id != node_id:
        return

    elapsed = time.monotonic() - start

    if elapsed > DURATION:
        return

    try:
        values = list(robot[node_id]["prox.horizontal"])

        if len(values) == 7:
            samples.append([
                datetime.now(timezone.utc).isoformat(),
                round(elapsed, 4),
                *values
            ])

            print(
                f"{elapsed:.2f}s: {values}",
                flush=True
            )
    except (KeyError, TypeError, ValueError) as exc:
        print("Erro de leitura:", exc, flush=True)

robot.set_variable_observer(node_id, observer)

print("A recolher sensores durante 10 segundos...", flush=True)

try:
    time.sleep(DURATION)
finally:
    with OUTPUT.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["timestamp_utc", "elapsed_s"] +
            [f"prox_{i}" for i in range(7)]
        )
        writer.writerows(samples)

    print("Amostras:", len(samples), flush=True)
    print("Ficheiro:", OUTPUT, flush=True)
