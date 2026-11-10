from pathlib import Path
from tdmclient import ClientAsync

CODIGO = Path("aseba/teste_angular_v3.aesl").read_text()
ESPERADO = [
    16384, -32768, -16384, 0,
    -16384, -32768, 16384, 0
]

with ClientAsync(tdm_addr="127.0.0.1", tdm_port=8596) as client:

    async def testar():
        node = await client.wait_for_node()
        if node.props.get("name") != "Thymio-II Wireless":
            raise RuntimeError("Dispositivo inesperado")

        await node.lock()
        try:
            await node.set_variables({
                "motor.left.target": [0],
                "motor.right.target": [0],
            })

            erro = await node.compile(CODIGO)
            if erro is not None:
                raise RuntimeError(f"Compilação: {erro}")

            await node.watch(variables=True)

            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            await node.wait_for_variables({
                "test_step", "test_results"
            })

            for _ in range(30):
                await client.sleep(0.1)
                if int(node.v.test_step) >= 8:
                    break

            # Permitir a atualização remota das variáveis
            await client.sleep(0.3)

            passos = int(node.v.test_step)
            valores = list(map(int, node.v.test_results))

            print("Passos executados:", passos)
            print("Obtido:  ", valores)
            print("Esperado:", ESPERADO)

            if passos != 8 or valores != ESPERADO:
                raise AssertionError(
                    "Normalização angular incorreta"
                )

            print("TESTE ANGULAR EMBARCADO: OK")

        finally:
            try:
                await node.stop()
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })
            finally:
                try:
                    await node.watch(variables=False)
                finally:
                    await node.unlock()
                    print("Programa parado e nó desbloqueado.")

    client.run_async_program(testar)
