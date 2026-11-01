import sys
from thymiodirect import Thymio

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

print("=== TESTE THYMIO WIRELESS WSL2 ===", flush=True)
print("Python:", sys.version.split()[0], flush=True)
print("Porta:", PORT, flush=True)

robot = Thymio(
    serial_port=PORT,
    refreshing_rate=0.2,
    refreshing_coverage={"prox.horizontal"},
    on_connect=lambda node_id: print(
        f"Thymio conectado: {node_id}",
        flush=True
    )
)

print("A estabelecer ligação...", flush=True)

robot.connect()

print("ID:", robot.first_node(), flush=True)
print("Comunicação estabelecida.", flush=True)
