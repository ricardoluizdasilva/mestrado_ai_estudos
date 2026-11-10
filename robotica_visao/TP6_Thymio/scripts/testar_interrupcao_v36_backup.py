"""TP6 - Testar interrupcoes da V3.6 sem movimento."""

import argparse
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("aseba/diagnostico_obstaculo_v36.aesl")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--caso",
    choices=["abort", "obstaculo"],
    required=True,
)
args = parser.parse_args()

codigo = PROGRAMA.read_text(encoding="utf-8")

with ClientAsync(
    tdm_addr="127.0.0.1",
    tdm_port=8596,
) as client:

    async def testar():
        node = await client.wait_for_node()

        if node.id_str != NODE_ID:
            raise RuntimeError("Thymio inesperado")

        await node.lock()
        iniciado = False

        async def motores_parados():
            return (
                int(node.v.motor.left.target) == 0
                and int(node.v.motor.right.target) == 0
            )

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

            await node.wait_for_variables({
                "seq_state",
                "seq_arm",
                "seq_fault",
                "seq_request",
                "seq_abort",
                "diag_obstaculo",
                "motor.left.target",
                "motor.right.target",
            })

            await client.sleep(0.3)

            if int(node.v.seq_state) != 0:
                raise RuntimeError("Estado inicial inesperado")

            print("Diagnostico:", args.caso, flush=True)
            print("A iniciar manobra logica...", flush=True)

            await node.set_variables({
                "seq_arm": [1],
                "seq_request": [1],
            })

            # Aguardar entrada no estado ativo.
            ativo = False

            for _ in range(20):
                await client.sleep(0.15)

                if not await motores_parados():
                    raise RuntimeError("Comando motor inesperado")

                estado = int(node.v.seq_state)

                if estado == 1:
                    ativo = True
                    break

                if estado == 6:
                    raise RuntimeError(
                        "Manobra abortada antes da injecao"
                    )

            if not ativo:
                raise RuntimeError(
                    "Controlador nao entrou no estado 1"
                )

            print("Estado ativo confirmado: 1", flush=True)

            # Injetar uma das duas condicoes.
            if args.caso == "abort":
                await node.set_variables({"seq_abort": [1]})
                falha_esperada = 6
            else:
                await node.set_variables({
                    "diag_obstaculo": [1]
                })
                falha_esperada = 1

            for _ in range(20):
                await client.sleep(0.15)

                if not await motores_parados():
                    raise RuntimeError("Motores nao parados")

                if int(node.v.seq_state) == 6:
                    break

            await client.sleep(0.3)

            estado = int(node.v.seq_state)
            falha = int(node.v.seq_fault)

            print("Estado final:", estado, flush=True)
            print("Codigo de falha:", falha, flush=True)
            print(
                "Motores parados:",
                await motores_parados(),
                flush=True,
            )

            assert estado == 6
            assert falha == falha_esperada
            assert await motores_parados()

            print("TESTE DE INTERRUPCAO: OK", flush=True)

        finally:
            try:
                await node.set_variables({
                    "seq_abort": [1],
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
                        "Paragem solicitada. No desbloqueado.",
                        flush=True,
                    )

    client.run_async_program(testar)
