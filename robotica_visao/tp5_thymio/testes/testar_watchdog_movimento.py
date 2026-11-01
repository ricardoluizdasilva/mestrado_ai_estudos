import sys
import time
from pathlib import Path

from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "testes"))

from testar_timer_contador import encerrar

ASM = BASE / "src" / "aseba" / "watchdog_motores.asm"
PORTA = "/dev/ttyACM0"

VELOCIDADE = 15
DURACAO_HEARTBEAT = 1.0
INTERVALO_HEARTBEAT = 0.15
DURACAO_OBSERVACAO = 1.2


def ler_estado(robot):
    return {
        "L": int(robot["motor.left.target"]),
        "R": int(robot["motor.right.target"]),
        "speed_L": int(robot["motor.left.speed"]),
        "speed_R": int(robot["motor.right.speed"]),
        "auth": int(robot["leds.top"][1]),
    }


def mostrar(tempo, estado):
    print(
        f"t={tempo:.2f}s | "
        f"Auth={estado['auth']} | "
        f"Target L={estado['L']:3d} "
        f"R={estado['R']:3d} | "
        f"Speed L={estado['speed_L']:3d} "
        f"R={estado['speed_R']:3d}"
    )


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
            "motor.left.speed",
            "motor.right.speed",
        },
    )

    node_id = None

    try:
        print("=== TESTE WATCHDOG COM MOVIMENTO ===")
        print("ATENCAO: manter as rodas suspensas.")

        th.connect()
        node_id = th.first_node()

        if node_id is None:
            raise RuntimeError("Thymio nao encontrado.")

        robot = th[node_id]
        conn = th.thymio_proxy.connection
        node = conn.remote_nodes[node_id]

        offset = node.var_total_size

        if offset + 6 > node.max_var_size:
            raise RuntimeError("Memoria insuficiente.")

        # Paragem preventiva
        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0
        time.sleep(0.5)

        print("Thymio:", node_id)
        print("Offset:", offset)

        # Carregar o watchdog
        programa = ASM.read_text(encoding="utf-8")
        th.run_asm(node_id, programa)
        time.sleep(0.5)

        estado = ler_estado(robot)
        mostrar(0.0, estado)

        if estado["L"] != 0 or estado["R"] != 0:
            raise RuntimeError("Motores nao iniciaram parados.")

        if estado["auth"] != 0:
            raise RuntimeError("Autorizacao inicial inesperada.")

        # Enviar comandos supervisionados
        # _userdata+4 = motor esquerdo
        # _userdata+5 = motor direito
        conn.set_variables(
            node_id,
            offset + 4,
            [VELOCIDADE, VELOCIDADE],
        )

        print("\n=== FASE 1: MOVIMENTO AUTORIZADO ===")

        sequencia = 1
        inicio = time.monotonic()
        movimento_observado = False

        while time.monotonic() - inicio < DURACAO_HEARTBEAT:
            conn.set_variables(
                node_id,
                offset,
                [sequencia],
            )

            sequencia += 1
            time.sleep(INTERVALO_HEARTBEAT)

            estado = ler_estado(robot)
            mostrar(time.monotonic() - inicio, estado)

            if estado["L"] > 0 and estado["R"] > 0:
                movimento_observado = True

        print("\n=== FASE 2: INTERROMPER HEARTBEATS ===")
        print("Nenhum novo heartbeat sera enviado.")
        print("Nao sera enviado comando explicito de paragem.")

        inicio_observacao = time.monotonic()
        expiracao_observada = None

        while time.monotonic() - inicio_observacao < DURACAO_OBSERVACAO:
            tempo = time.monotonic() - inicio_observacao
            estado = ler_estado(robot)
            mostrar(tempo, estado)

            if (
                expiracao_observada is None
                and estado["auth"] == 0
                and estado["L"] == 0
                and estado["R"] == 0
            ):
                expiracao_observada = tempo

            time.sleep(0.1)

        print("\n=== RESULTADO ===")

        if not movimento_observado:
            raise RuntimeError("Nao foi observado comando de movimento.")

        if expiracao_observada is None:
            raise RuntimeError("Nao foi confirmada a paragem automatica.")

        print("Expiracao observada apos:", round(expiracao_observada, 3), "segundos")

        print("WATCHDOG: PARAGEM DOS COMANDOS VALIDADA")

        # A velocidade fisica tambem deve regressar
        # proximo de zero; verificar os valores impressos.

    finally:
        # Esta rotina envia zero apenas no final do teste.
        # A verificacao da expiracao ocorre antes.
        encerrar(th, node_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTeste interrompido.")
