import asyncio
import time
from thymiodirect import Thymio

PORTA = "/dev/ttyACM0"
VELOCIDADE = 50
DURACAO = 3.0

th = Thymio(serial_port=PORTA)
node_id = None

try:
    th.connect()

    for _ in range(30):
        node_id = th.first_node()
        if node_id is not None:
            break
        time.sleep(0.1)

    if node_id is None:
        raise RuntimeError("Thymio não encontrado.")

    robot = th[node_id]

    robot["motor.left.target"] = 0
    robot["motor.right.target"] = 0

    time.sleep(0.5)

    print("Velocidades iniciais:")
    print("Esquerda:", robot["motor.left.speed"])
    print("Direita:", robot["motor.right.speed"])

    print("\nA iniciar teste dos motores...")

    robot["motor.left.target"] = VELOCIDADE
    robot["motor.right.target"] = VELOCIDADE

    inicio = time.monotonic()

    while time.monotonic() - inicio < DURACAO:
        esquerda = robot["motor.left.speed"]
        direita = robot["motor.right.speed"]

        print(
            f"Esquerda: {esquerda:>5} | "
            f"Direita: {direita:>5}"
        )

        time.sleep(0.2)

finally:
    if node_id is not None:
        robot = th[node_id]
        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0
        time.sleep(0.5)

    if th.thymio_proxy is not None:
        proxy = th.thymio_proxy
        conn = proxy.connection

        if conn is not None:
            async def cancelar_descoberta():
                tarefas = [
                    tarefa
                    for tarefa in asyncio.all_tasks()
                    if tarefa is not asyncio.current_task()
                    and not tarefa.done()
                    and "discover" in tarefa.get_coro().__qualname__
                ]

                for tarefa in tarefas:
                    tarefa.cancel()

                if tarefas:
                    await asyncio.gather(
                        *tarefas,
                        return_exceptions=True
                    )

            if proxy.loop.is_running():
                futuro = asyncio.run_coroutine_threadsafe(
                    cancelar_descoberta(),
                    proxy.loop
                )
                futuro.result(timeout=3)

            conn.shutdown()
            conn.input_thread.join(timeout=5)
            th.thread.join(timeout=7)

    print("\nMotores parados. Teste concluído.")
