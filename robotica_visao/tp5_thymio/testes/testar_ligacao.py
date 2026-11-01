import time, asyncio
from thymiodirect import Thymio

PORTA = "/dev/ttyACM0"

print(f"A ligar ao Thymio em {PORTA}...")

th = Thymio(
    serial_port=PORTA,
    on_connect=lambda node_id: print(f"Thymio ligado: {node_id}"),
)

try:
    th.connect()

    node_id = None
    for _ in range(30):
        node_id = th.first_node()
        if node_id is not None:
            break
        time.sleep(0.1)

    if node_id is None:
        raise RuntimeError("Thymio não detetado.")

    # Paragem preventiva
    th[node_id]["motor.left.target"] = 0
    th[node_id]["motor.right.target"] = 0

    print("ID:", node_id)
    print("Sensores de proximidade:", th[node_id]["prox.horizontal"])
    print("Comunicação validada.")

finally:
    if node_id is not None:
        th[node_id]["motor.left.target"] = 0
        th[node_id]["motor.right.target"] = 0
        time.sleep(0.5)

    if th.thymio_proxy is not None:
        proxy = th.thymio_proxy
        conn = proxy.connection

        if conn is not None:
            loop = proxy.loop

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
                    await asyncio.gather(*tarefas, return_exceptions=True)

                return len(tarefas)

            if loop.is_running():
                futuro = asyncio.run_coroutine_threadsafe(cancelar_descoberta(), loop)

                try:
                    numero = futuro.result(timeout=3)
                    print(f"Tarefas de descoberta canceladas: {numero}")
                except TimeoutError:
                    print("Aviso: cancelamento excedeu o tempo limite.")

            conn.shutdown()
            conn.input_thread.join(timeout=5)
            th.thread.join(timeout=7)

            if th.thread.is_alive():
                print("AVISO: thread principal ainda ativa.")
            else:
                print("Thread principal terminada.")

    print("Procedimento de encerramento concluído.")
