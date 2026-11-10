from thymiodirect import Thymio

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_00124B001DF456B0-if00"
)

print("Teste Wireless com atualização reduzida", flush=True)

robot = Thymio(
    serial_port=PORT,
    refreshing_rate=0.2,
    refreshing_coverage={"prox.horizontal"},
    on_connect=lambda node_id: print(
        f"Thymio conectado: {node_id}",
        flush=True
    ),
)

robot.connect()

print("ID:", robot.first_node(), flush=True)
