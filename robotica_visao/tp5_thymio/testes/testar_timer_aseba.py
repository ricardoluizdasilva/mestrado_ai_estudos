import asyncio
import time
from pathlib import Path

from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
ASM = BASE / "src" / "aseba" / "teste_timer.asm"

PORTA = "/dev/ttyACM0"


def encerrar(th, node_id):
    if node_id is not None:
        try:
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
            time.sleep(0.5)
        except Exception as exc:
            print("AVISO ao parar motores:", exc)

    proxy = th.thymio_proxy
    if proxy is None or proxy.connection is None:
        return

    conn = proxy.connection

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

    try:
        if proxy.loop.is_running():
            futuro = asyncio.run_coroutine_threadsafe(cancelar_descoberta(), proxy.loop)
            futuro.result(timeout=3)
    finally:
        conn.shutdown()
        conn.input_thread.join(timeout=5)
        th.thread.join(timeout=7)


def main():
    if not ASM.is_file():
        raise FileNotFoundError(ASM)

    th = Thymio(serial_port=PORTA)
    node_id = None

    try:
        print("A ligar ao Thymio...")
        th.connect()

        node_id = th.first_node()
        if node_id is None:
            raise RuntimeError("Thymio não encontrado.")

        robot = th[node_id]

        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0
        time.sleep(0.3)

        eventos = th.events(node_id)
        print("Eventos disponíveis:", eventos)

        if "timer0" not in eventos:
            raise RuntimeError("Evento timer0 indisponível.")

        print("A carregar teste Aseba...")

        programa = ASM.read_text(encoding="utf-8")
        th.run_asm(node_id, programa)

        time.sleep(1.0)

        print("timer.period:", robot["timer.period"])
        print("motor.left.target:", robot["motor.left.target"])
        print("motor.right.target:", robot["motor.right.target"])

        periodo = robot["timer.period"][0]
        esquerda = robot["motor.left.target"]
        direita = robot["motor.right.target"]

        if periodo != 100 or esquerda != 0 or direita != 0:
            raise RuntimeError("Valores inesperados após carregar o programa.")

        print("TESTE INICIAL DO TIMER: OK")
        print("Nota: execução periódica ainda não medida.")

    finally:
        encerrar(th, node_id)
        print("Comunicação encerrada.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Teste interrompido.")
