"""TP6 - Teste físico de rotação controlada em Aseba V3.2."""

import csv
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v32.aesl")
SAIDA = Path("resultados/rotacao_embarcada_v32_45.csv")

NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"
ESCALA = 180 / 32768

codigo = PROGRAMA.read_text(encoding="utf-8")

with ClientAsync(
    tdm_addr="127.0.0.1",
    tdm_port=8596,
) as client:

    async def executar():
        node = await client.wait_for_node()

        if node.id_str != NODE_ID:
            raise RuntimeError("Thymio inesperado")

        await node.lock()
        iniciado = False
        registos = []

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

            erro = await node.run()
            if erro is not None:
                raise RuntimeError(f"Execução: {erro}")

            iniciado = True

            await node.wait_for_variables({
                "ctl_state",
                "ctl_mode",
                "ctl_active_mode",
                "ctl_ticks",
                "ctl_angle_b",
                "ctl_stop_angle_b",
                "odo_snapshot",
                "odo_turns",
            })

            # Configurar explicitamente o modo real.
            await node.set_variables({
                "ctl_mode": [1],
                "ctl_abort": [0],
            })

            await client.sleep(0.3)

            if int(node.v.ctl_state) != 0:
                raise RuntimeError("Controlador não está pronto")

            print("Modo real configurado.", flush=True)
            print("Alvo físico pretendido: 45 graus", flush=True)
            print("Limiar embarcado: ~37 graus", flush=True)

            await node.set_variables({"ctl_request": [1]})
            inicio = time.monotonic()

            estado_final = None

            for _ in range(80):
                await client.sleep(0.15)

                tempo = time.monotonic() - inicio
                estado = int(node.v.ctl_state)
                modo = int(node.v.ctl_active_mode)
                ticks = int(node.v.ctl_ticks)
                theta = int(node.v.ctl_angle_b) * ESCALA

                s = list(map(int, node.v.odo_snapshot))
                ve, vd = s[4], s[5]

                registo = {
                    "tempo_s": round(tempo, 3),
                    "estado": estado,
                    "modo": modo,
                    "ticks": ticks,
                    "theta_graus": round(theta, 4),
                    "vel_esq": ve,
                    "vel_dir": vd,
                }
                registos.append(registo)

                print(registo, flush=True)

                if estado == 4:
                    estado_final = estado
                    break

                if estado == 3:
                    estado_final = estado
                    break

                if tempo > 9:
                    break

            # Solicitar sempre a paragem antes da leitura final.
            await parar()
            await client.sleep(0.5)

            snapshot = list(map(int, node.v.odo_snapshot))
            turns = int(node.v.odo_turns)

            theta_final = (
                snapshot[3] + 65536 * turns
            ) * ESCALA

            theta_paragem = int(node.v.ctl_stop_angle_b) * ESCALA

            SAIDA.parent.mkdir(parents=True, exist_ok=True)

            with SAIDA.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=registos[0].keys()
                )
                writer.writeheader()
                writer.writerows(registos)

            print("\n=== RESULTADO V3.2 ===", flush=True)
            print("Estado final:", estado_final, flush=True)
            print("Modo ativo:", int(node.v.ctl_active_mode))
            print(f"Ângulo no limiar: {theta_paragem:.3f}°")
            print(f"Ângulo final estimado: {theta_final:.3f}°")
            print(f"Rotação residual: {theta_final-theta_paragem:+.3f}°")
            print(f"Desvio para 45°: {theta_final-45:+.3f}°")
            print("CSV:", SAIDA)

            if estado_final != 3:
                raise RuntimeError(
                    "O controlador não terminou no estado 3."
                )

            if int(node.v.ctl_active_mode) != 1:
                raise RuntimeError("Modo real não confirmado.")

        finally:
            try:
                await node.set_variables({"ctl_abort": [1]})
                await parar()
                print("Paragem de segurança solicitada.")
            finally:
                try:
                    if iniciado:
                        await node.stop()
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print("Nó desbloqueado.")

    client.run_async_program(executar)
