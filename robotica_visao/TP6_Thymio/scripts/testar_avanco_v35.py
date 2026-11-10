
"""TP6 - Teste embarcado do controlador linear V3.4."""

import json
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v35.aesl")
SAIDA = Path("resultados/avanco_linear_v35.json")
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
                "lin_mode": [1],
                "lin_abort": [0],
            })

            await client.sleep(0.3)

            if int(node.v.lin_state) != 0:
                raise RuntimeError("Controlador não está pronto")

            await node.set_variables({"lin_request": [1]})

            print("AVANÇO FÍSICO INICIADO.", flush=True)

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

                # No estado 0, o pedido pode ainda estar pendente.
                if estado == 0:
                    if modo != 0:
                        raise RuntimeError(
                            "Modo inesperado durante o arranque"
                        )
                elif estado in (1, 2, 3, 4):
                    if modo != 1:
                        raise RuntimeError(
                            "Modo real nao confirmado"
                        )
                else:
                    raise RuntimeError(
                        f"Estado desconhecido: {estado}"
                    )

                if estado == 0 and time.monotonic() - inicio > 2.0:
                    raise RuntimeError(
                        "Controlador nao iniciou em 2 segundos"
                    )

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
            print("Distância de controlo:", final["distancia_cm"], "cm")
            print("Distância no limiar:", final["paragem_cm"], "cm")

            assert final["estado"] == 3
            assert final["modo"] == 1
            assert final["ticks"] <= 60

            await node.wait_for_variables({
                "odo_x_coarse",
                "odo_x_rem",
                "odo_y_coarse",
                "odo_y_rem",
            })
            await client.sleep(0.3)

            xc = int(node.v.odo_x_coarse)
            xr = int(node.v.odo_x_rem)
            yc = int(node.v.odo_y_coarse)
            yr = int(node.v.odo_y_rem)
            x = (10 * xc + xr) / 1000
            y = (10 * yc + yr) / 1000

            print(f"X final estimado: {x:.4f} cm")
            print(f"Y final estimado: {y:.4f} cm")
            print(
                "Deslocamento estimado:",
                f"{(x*x + y*y)**0.5:.4f} cm"
            )
            print("TESTE FÍSICO V3.4 CONCLUÍDO")
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
