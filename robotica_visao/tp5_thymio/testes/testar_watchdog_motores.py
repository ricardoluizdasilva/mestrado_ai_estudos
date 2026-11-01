import sys
import time
from pathlib import Path

from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "testes"))

from testar_timer_contador import encerrar

ASM = BASE / "src" / "aseba" / "watchdog_motores.asm"
PORTA = "/dev/ttyACM0"


def verificar_paragem(robot):
    esquerda = int(robot["motor.left.target"])
    direita = int(robot["motor.right.target"])

    if esquerda != 0 or direita != 0:
        raise RuntimeError(f"Comandos inesperados: L={esquerda}, R={direita}")

    return esquerda, direita


def main():
    if not ASM.is_file():
        raise FileNotFoundError(ASM)

    th = Thymio(
        serial_port=PORTA,
        refreshing_rate=0.1,
        refreshing_coverage={
            "leds.top",
            "timer.period",
            "motor.left.target",
            "motor.right.target",
        },
    )

    node_id = None

    try:
        print("=== TESTE DO WATCHDOG SEM MOVIMENTO ===")

        th.connect()
        node_id = th.first_node()

        if node_id is None:
            raise RuntimeError("Thymio nao encontrado.")

        robot = th[node_id]
        conn = th.thymio_proxy.connection
        node = conn.remote_nodes[node_id]

        offset = node.var_total_size

        if offset + 6 > node.max_var_size:
            raise RuntimeError("Memoria Aseba insuficiente.")

        # Paragem preventiva
        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0
        time.sleep(0.5)

        print("Thymio:", node_id)
        print("Offset de memoria:", offset)

        # Carregar o watchdog experimental
        programa = ASM.read_text(encoding="utf-8")
        th.run_asm(node_id, programa)

        time.sleep(0.5)

        verificar_paragem(robot)

        periodo = robot["timer.period"]
        print("Timer:", periodo)

        if int(periodo[0]) != 100:
            raise RuntimeError("Timer incorreto.")

        print("\n=== FASE 1: HEARTBEATS ===")

        for numero in range(1, 9):
            # Escrever apenas o numero de sequencia.
            # Os comandos dos motores continuam em zero.
            conn.set_variables(node_id, offset, [numero])

            time.sleep(0.15)

            verificar_paragem(robot)
            auth = int(robot["leds.top"][1])

            print(f"Heartbeat={numero:02d} | Autorizacao={auth} | L=0 R=0")

        print("\n=== FASE 2: EXPIRACAO ===")

        # Deixar de enviar heartbeats.
        for i in range(10):
            time.sleep(0.1)

            verificar_paragem(robot)
            auth = int(robot["leds.top"][1])

            print(f"t={(i + 1) * 0.1:.1f}s | Autorizacao={auth} | L=0 R=0")

        if int(robot["leds.top"][1]) != 0:
            raise RuntimeError("O watchdog nao retirou a autorizacao.")

        print("\nWATCHDOG SEM MOVIMENTO: OK")

    finally:
        encerrar(th, node_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Teste interrompido.")
