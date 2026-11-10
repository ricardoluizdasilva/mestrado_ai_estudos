import json
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("aseba/teste_angular_integrado_v31.aesl")
SAIDA = Path("resultados/teste_angular_integrado_v31.json")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

ESPERADO_THETA = [
    16384, -32768, -16384, 0,
    -16384, -32768, 16384, 0
]
ESPERADO_MID = [
    8192, 24576, -24576, -8192,
    -8192, -24576, 24576, 8192
]
ESPERADO_TURNS = [0, 1, 1, 1, 1, 1, 0, 0]

codigo = PROGRAMA.read_text(encoding="utf-8")

with ClientAsync(tdm_addr="127.0.0.1", tdm_port=8596) as client:

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
                raise RuntimeError(f"Compilação: {erro}")

            await node.watch(variables=True)
            iniciado = True
            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            await node.wait_for_variables({
                "test_theta_log", "test_mid_log",
                "test_turns_log", "odo_ticks"
            })

            for _ in range(30):
                await client.sleep(0.1)
                if int(node.v.odo_ticks) >= 10:
                    break

            await client.sleep(0.3)

            theta = list(map(int, node.v.test_theta_log))
            mid = list(map(int, node.v.test_mid_log))
            turns = list(map(int, node.v.test_turns_log))

            print("Theta:", theta)
            print("Mid:  ", mid)
            print("Turns:", turns)

            resultado = {
                "theta": theta,
                "theta_mid": mid,
                "turns": turns
            }
            SAIDA.write_text(
                json.dumps(resultado, indent=2),
                encoding="utf-8"
            )

            assert theta == ESPERADO_THETA, "Erro theta"
            assert mid == ESPERADO_MID, "Erro theta_mid"
            assert turns == ESPERADO_TURNS, "Erro turns"

            print("TESTE ANGULAR INTEGRADO V3.1: OK")
            print("Resultados:", SAIDA)

        finally:
            try:
                if iniciado:
                    await node.stop()
            finally:
                try:
                    await node.set_variables({
                        "motor.left.target": [0],
                        "motor.right.target": [0],
                    })
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print("Paragem solicitada. Nó desbloqueado.")

    client.run_async_program(testar)
