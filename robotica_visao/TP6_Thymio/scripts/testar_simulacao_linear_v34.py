"""TP6 - Teste embarcado do controlador linear V3.4."""

import json
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v34.aesl")
SAIDA = Path("resultados/simulacao_linear_v34.json")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

codigo = PROGRAMA.read_text(encoding="utf-8")

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

            erro = await node.compile(codigo)
            if erro is not None:
                raise RuntimeError(f"Compilação: {erro}")

            await node.watch(variables=True)

            iniciado = True
            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            await node.wait_for_variables({
                "lin_state",
                "lin_mode",
                "lin_active_mode",
                "lin_ticks",
                "lin_progress_001mm",
                "lin_stop_001mm",
                "odo_snapshot",
            })

            await node.set_variables({
                "lin_mode": [0],
                "lin_abort": [0],
            })

            await client.sleep(0.3)

            if int(node.v.lin_state) != 0:
                raise RuntimeError("Controlador não está pronto")

            await node.set_variables({"lin_request": [1]})

            print("Simulação linear iniciada.", flush=True)

            registos = []
            inicio = time.monotonic()

            while time.monotonic() - inicio < 9:
                await client.sleep(0.2)

                estado = int(node.v.lin_state)
                ticks = int(node.v.lin_ticks)
                modo = int(node.v.lin_active_mode)
                progresso = int(node.v.lin_progress_001mm)
                paragem = int(node.v.lin_stop_001mm)

                snapshot = list(map(int, node.v.odo_snapshot))
                ve, vd = snapshot[4], snapshot[5]

                registo = {
                    "estado": estado,
                    "ticks": ticks,
                    "distancia_cm": progresso / 1000,
                    "paragem_cm": paragem / 1000,
                    "modo": modo,
                    "vel_esq": ve,
                    "vel_dir": vd,
                }

                registos.append(registo)
                print(registo, flush=True)

                if modo != 0:
                    raise RuntimeError("Modo real ativado inesperadamente")

                if estado in (3, 4):
                    break

            if not registos:
                raise RuntimeError("Sem registos")

            final = registos[-1]

            SAIDA.parent.mkdir(parents=True, exist_ok=True)
            SAIDA.write_text(
                json.dumps(registos, indent=2),
                encoding="utf-8",
            )

            print("\n=== RESULTADO V3.4 ===")
            print("Estado final:", final["estado"])
            print("Ciclos:", final["ticks"])
            print("Distância simulada:", final["distancia_cm"], "cm")
            print("Distância no limiar:", final["paragem_cm"], "cm")

            assert final["estado"] == 3
            assert final["ticks"] == 38
            assert final["distancia_cm"] == 9.5
            assert final["paragem_cm"] == 9.5
            assert all(r["modo"] == 0 for r in registos)
            assert all(r["vel_esq"] == 0 and r["vel_dir"] == 0
                       for r in registos)

            print("SIMULAÇÃO LINEAR V3.4: OK")
            print("Resultados:", SAIDA)

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
