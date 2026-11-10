"""TP6 - Teste da máquina de estados V3.2 sem movimento."""

import json
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v32.aesl")
SAIDA = Path("resultados/simulacao_angular_v32.json")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

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

        async def parar_motores():
            await node.set_variables({
                "motor.left.target": [0],
                "motor.right.target": [0],
            })

        try:
            await parar_motores()

            erro = await node.compile(codigo)
            if erro is not None:
                raise RuntimeError(f"Compilação: {erro}")

            await node.watch(variables=True)

            iniciado = True
            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            await node.wait_for_variables({
                "ctl_state",
                "ctl_ticks",
                "ctl_angle_b",
                "ctl_stop_angle_b",
                "ctl_active_mode",
            })

            # Selecionar expressamente o modo de simulação.
            await node.set_variables({
                "ctl_mode": [0],
                "ctl_abort": [0],
            })

            await node.set_variables({
                "ctl_request": [1],
            })

            print("Simulação iniciada.", flush=True)

            registos = []

            for i in range(35):
                await client.sleep(0.2)

                estado = int(node.v.ctl_state)
                ticks = int(node.v.ctl_ticks)
                angulo_b = int(node.v.ctl_angle_b)
                paragem_b = int(node.v.ctl_stop_angle_b)
                modo = int(node.v.ctl_active_mode)

                registo = {
                    "amostra": i,
                    "estado": estado,
                    "ticks": ticks,
                    "angulo_graus": angulo_b * 180 / 32768,
                    "paragem_graus": paragem_b * 180 / 32768,
                    "modo": modo,
                }

                registos.append(registo)

                print(registo, flush=True)

                if modo != 0:
                    raise RuntimeError(
                        "Modo de simulação não confirmado"
                    )

                if estado in (3, 4):
                    break

            SAIDA.parent.mkdir(parents=True, exist_ok=True)
            SAIDA.write_text(
                json.dumps(registos, indent=2),
                encoding="utf-8",
            )

            final = registos[-1]

            print("\n=== RESULTADO ===")
            print("Estado final:", final["estado"])
            print("Ciclos:", final["ticks"])
            print(
                "Ângulo de paragem:",
                final["paragem_graus"]
            )
            print("Ficheiro:", SAIDA)

            if final["estado"] != 3:
                raise RuntimeError(
                    "Controlador não terminou corretamente"
                )

            if final["ticks"] != 14:
                raise RuntimeError(
                    "Número de ciclos inesperado"
                )

            if final["paragem_graus"] != 39.375:
                raise RuntimeError(
                    "Limiar de paragem inesperado"
                )

            print("SIMULAÇÃO V3.2: OK", flush=True)

        finally:
            try:
                await parar_motores()
                if iniciado:
                    await node.stop()
            finally:
                try:
                    await node.watch(variables=False)
                finally:
                    await node.unlock()
                    print(
                        "Paragem solicitada. Nó desbloqueado.",
                        flush=True,
                    )

    client.run_async_program(testar)
