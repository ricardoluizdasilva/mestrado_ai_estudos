from thymiodirect import Thymio

PORT = "/dev/ttyACM0"

print("A ligar ao Thymio...", flush=True)

robot = Thymio(
    serial_port=PORT,
    on_connect=lambda node_id: print(
        f"Thymio conectado: {node_id}",
        flush=True
    )
)

robot.connect()

print("ID:", robot.first_node(), flush=True)
print("Teste concluído.", flush=True)
