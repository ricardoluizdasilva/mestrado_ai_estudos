
import sys
import time
from pathlib import Path

from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "testes"))

from testar_timer_contador import encerrar

ASM = BASE / "src" / "aseba" / "watchdog_logico.asm"
PORTA = "/dev/ttyACM0"


def main():
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
        print("A ligar ao Thymio...")
        th.connect()

        node_id = th.first_node()

        if node_id is None:
            raise RuntimeError("Thymio nao encontrado.")

        robot = th[node_id]
        conn = th.thymio_proxy.connection

        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0
        time.sleep(0.5)

        # Validar espaco para quatro variaveis adicionais
        node = conn.remote_nodes[node_id]

        offset = node.var_total_size

        print("Offset da memoria:", offset)
        print("Capacidade:", node.max_var_size)

        if offset + 4 > node.max_var_size:
            raise RuntimeError(
                "Memoria Aseba insuficiente."
            )

        programa = ASM.read_text(encoding="utf-8")

        print("A carregar watchdog logico...")
        th.run_asm(node_id, programa)

        time.sleep(0.5)

        print("\n=== FASE 1: HEARTBEAT ATIVO ===")

        for numero in range(1, 11):
            # Atualizar sequencia
            conn.set_variables(
                node_id,
                offset,
                [numero],
            )

            time.sleep(0.15)

            leds = robot["leds.top"]

            print(
                f"Heartbeat={numero:02d} | "
                f"Contador={leds[0]} | "
                f"Autorizacao={leds[1]}"
            )

        print("\n=== FASE 2: SEM HEARTBEAT ===")
        print("Interromper sinais durante 1 segundo.")

        for i in range(10):
            time.sleep(0.1)

            leds = robot["leds.top"]

            esquerda = robot["motor.left.target"]
            direita = robot["motor.right.target"]

            print(
                f"t={(i + 1) * 0.1:.1f}s | "
                f"Contador={leds[0]} | "
                f"Autorizacao={leds[1]} | "
                f"L={esquerda} R={direita}"
            )

        if int(robot["leds.top"][1]) != 0:
            raise RuntimeError(
                "Watchdog nao expirou."
            )

        if (
            int(robot["motor.left.target"]) != 0
            or int(robot["motor.right.target"]) != 0
        ):
            raise RuntimeError(
                "Comandos dos motores nao estao a zero."
            )

        print("\nWATCHDOG LOGICO: TESTE CONCLUIDO")

    finally:
        encerrar(th, node_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Teste interrompido.")
