
"""TP6 - Exercicio 9: testar correcao embarcada de pose V3.9."""

import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("aseba/correcao_pose_v39.aesl")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

VARIAVEIS = {
    "odo_x_coarse", "odo_x_rem",
    "odo_y_coarse", "odo_y_rem",
    "odo_x_01mm", "odo_y_01mm",
    "odo_theta_b", "odo_turns",
    "corr_request", "corr_applied",
    "motor.left.target", "motor.right.target",
}


def pose(node):
    xc = int(node.v.odo_x_coarse)
    xr = int(node.v.odo_x_rem)
    yc = int(node.v.odo_y_coarse)
    yr = int(node.v.odo_y_rem)
    theta_b = int(node.v.odo_theta_b)
    turns = int(node.v.odo_turns)

    return {
        "x_cm": (10 * xc + xr) / 1000,
        "y_cm": (10 * yc + yr) / 1000,
        "theta_graus": (
            theta_b + 65536 * turns
        ) * 180 / 32768,
    }


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def testar():
            node = await client.wait_for_node()

            if node.id_str != ID:
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            iniciado = False

            try:
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

                erro = await node.compile(codigo)
                if erro is not None:
                    raise RuntimeError(f"Compilacao: {erro}")

                await node.watch(variables=True)

                erro = await node.run()
                if erro is not None:
                    raise RuntimeError(f"Execucao: {erro}")

                iniciado = True
                await node.wait_for_variables(VARIAVEIS)

                # Injetar a pose artificial do segundo quadrado.
                # -0,266 cm = -26 * 0,1 mm - 6 * 0,01 mm.
                await node.set_variables({
                    "odo_x_coarse": [-26],
                    "odo_x_rem": [-6],
                    "odo_y_coarse": [7],
                    "odo_y_rem": [9],
                    "odo_x_01mm": [-26],
                    "odo_y_01mm": [7],
                    "odo_theta_b": [-59],
                    "odo_turns": [1],
                })

                prazo = time.monotonic() + 3.0

                while time.monotonic() < prazo:
                    await client.sleep(0.1)
                    antes = pose(node)

                    if (
                        abs(antes["x_cm"] + 0.266) < 0.0001
                        and abs(antes["y_cm"] - 0.079) < 0.0001
                        and int(node.v.odo_turns) == 1
                    ):
                        break
                else:
                    raise RuntimeError(
                        "Pose artificial nao confirmada pelo TDM"
                    )

                print("=== POSE ANTES DA CORRECAO ===")
                print(antes, flush=True)

                if (
                    int(node.v.motor.left.target) != 0
                    or int(node.v.motor.right.target) != 0
                ):
                    raise RuntimeError("Motores nao estao parados")

                aplicacoes_iniciais = int(node.v.corr_applied)

                await node.set_variables({"corr_request": [1]})

                prazo = time.monotonic() + 3.0

                while time.monotonic() < prazo:
                    await client.sleep(0.1)

                    if (
                        int(node.v.corr_applied)
                        > aplicacoes_iniciais
                    ):
                        break
                else:
                    raise RuntimeError(
                        "Pedido de correcao nao confirmado"
                    )

                # Permitir atualizar as restantes variaveis.
                await client.sleep(0.4)
                depois = pose(node)

                print("\n=== POSE DEPOIS DA CORRECAO ===")
                print(depois, flush=True)
                print(
                    "Correcoes aplicadas:",
                    int(node.v.corr_applied),
                    flush=True,
                )
                print(
                    "Pedido pendente:",
                    int(node.v.corr_request),
                    flush=True,
                )

                assert abs(depois["x_cm"]) < 0.0001
                assert abs(depois["y_cm"]) < 0.0001
                assert abs(depois["theta_graus"] - 360) < 0.01
                assert int(node.v.corr_request) == 0
                assert int(node.v.corr_applied) == (
                    aplicacoes_iniciais + 1
                )

                print("\nCORRECAO EMBARCADA V3.9: OK")

            finally:
                try:
                    await node.set_variables({
                        "motor.left.target": [0],
                        "motor.right.target": [0],
                    })
                    if iniciado:
                        await node.stop()
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print(
                            "Programa parado. No desbloqueado."
                        )

        client.run_async_program(testar)


if __name__ == "__main__":
    main()
