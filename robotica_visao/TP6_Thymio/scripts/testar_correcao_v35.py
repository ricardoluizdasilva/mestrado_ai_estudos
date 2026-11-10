from pathlib import Path
from tdmclient import ClientAsync

SRC = Path("aseba/diagnostico_correcao_v35.aesl")
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
            erro = await node.compile(SRC.read_text(encoding="utf-8"))
            if erro is not None:
                raise RuntimeError(f"Compilação: {erro}")

            await node.watch(variables=True)
            iniciado = True
            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            await node.wait_for_variables({
                "lin_state", "test_n",
                "test_heading", "test_correction",
            })

            # Modo real apenas para exercitar a lógica;
            # o programa de diagnóstico mantém os motores a zero.
            await node.set_variables({
                "lin_mode": [1],
                "lin_abort": [0],
                "lin_request": [1],
            })

            for _ in range(60):
                await client.sleep(0.15)
                if int(node.v.lin_state) in (3, 4):
                    break

            await client.sleep(0.3)

            n = int(node.v.test_n)
            headings = list(map(int, node.v.test_heading))[:n]
            corrections = list(map(int, node.v.test_correction))[:n]
            estado = int(node.v.lin_state)

            print("Estado final:", estado)
            print("Ciclos registados:", n)

            for i in range(n):
                if i % 5 == 0 or i == n - 1:
                    print(
                        f"Ciclo {i+1:02d}: "
                        f"heading={headings[i]:+6d}, "
                        f"correcao={corrections[i]:+3d}"
                    )

            assert estado == 3, "Manobra não concluída"
            assert n > 20, "Registo insuficiente"
            assert all(abs(c) <= 8 for c in corrections)
            assert any(c > 0 for c in corrections)
            assert all(
                c >= 0 for h, c in zip(headings, corrections)
                if h < 0
            )
            assert all(
                c <= 0 for h, c in zip(headings, corrections)
                if h > 0
            )

            print("CORREÇÃO ANGULAR V3.5: OK")

        finally:
            try:
                await node.set_variables({"lin_abort": [1]})
                await parar()
                if iniciado:
                    await node.stop()
            finally:
                try:
                    await node.watch(variables=False)
                finally:
                    await node.unlock()
                    print("Paragem solicitada. Nó desbloqueado.")

    client.run_async_program(testar)
