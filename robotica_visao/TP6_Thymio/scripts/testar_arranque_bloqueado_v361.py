
"""TP6 — Bloqueio de arranque por obstáculo, sem movimento."""

from pathlib import Path
from tdmclient import ClientAsync

SRC = Path("aseba/diagnostico_arranque_v361.aesl")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"


with ClientAsync(tdm_addr="127.0.0.1", tdm_port=8596) as client:

    async def testar():
        node = await client.wait_for_node()

        if node.id_str != ID:
            raise RuntimeError("Thymio inesperado")

        await node.lock()
        iniciado = False

        async def parar():
            await node.set_variables({
                "motor.left.target": [0],
                "motor.right.target": [0],
            })

        try:
            await parar()

            erro = await node.compile(
                SRC.read_text(encoding="utf-8")
            )
            if erro is not None:
                raise RuntimeError(f"Compilação: {erro}")

            await node.watch(variables=True)

            iniciado = True
            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            await node.wait_for_variables({
                "seq_state",
                "seq_arm",
                "seq_request",
                "seq_fault",
                "seq_line_ticks",
                "diag_obstaculo",
                "motor.left.target",
                "motor.right.target",
            })

            await client.sleep(0.3)

            assert int(node.v.seq_state) == 0

            # Primeiro colocar o obstáculo.
            await node.set_variables({"diag_obstaculo": [1]})
            await client.sleep(0.3)

            assert int(node.v.diag_obstaculo) == 1

            # Só depois pedir o arranque.
            await node.set_variables({
                "seq_arm": [1],
                "seq_request": [1],
            })

            for _ in range(20):
                await client.sleep(0.15)
                if int(node.v.seq_state) == 6:
                    break

            await client.sleep(0.3)

            resultado = {
                "estado": int(node.v.seq_state),
                "falha": int(node.v.seq_fault),
                "arm": int(node.v.seq_arm),
                "request": int(node.v.seq_request),
                "ciclos_reta": int(node.v.seq_line_ticks),
                "motor_esquerdo": int(node.v.motor.left.target),
                "motor_direito": int(node.v.motor.right.target),
            }

            print("=== BLOQUEIO DE ARRANQUE V3.6.1 ===")
            for chave, valor in resultado.items():
                print(f"{chave}: {valor}", flush=True)

            assert resultado == {
                "estado": 6,
                "falha": 1,
                "arm": 0,
                "request": 0,
                "ciclos_reta": 0,
                "motor_esquerdo": 0,
                "motor_direito": 0,
            }

            print("BLOQUEIO DE ARRANQUE: OK", flush=True)

        finally:
            try:
                await node.set_variables({"seq_abort": [1]})
                await parar()
                if iniciado:
                    await node.stop()
            finally:
                try:
                    await node.watch(variables=False)
                finally:
                    await node.unlock()
                    print("Programa parado. Nó desbloqueado.")

    client.run_async_program(testar)

