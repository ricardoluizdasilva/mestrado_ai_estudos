"""TP6 - Teste estático do snapshot de odometria."""

import csv
import json
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_buffer.aesl")
SAIDA = Path("resultados/odometria_buffer_dinamica.csv")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def testar():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
                raise RuntimeError("Nó TDM inesperado")

            print("Thymio identificado:", node.id_str, flush=True)

            await node.lock()
            execucao_solicitada = False

            try:
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

                erro = await node.compile(codigo)
                if erro is not None:
                    raise RuntimeError(f"Compilação: {erro}")

                print("Compilação e carregamento: OK", flush=True)

                await node.watch(variables=True)

                execucao_solicitada = True
                erro = await node.run()
                if erro is not None:
                    raise RuntimeError(f"Execução: {erro}")

                await node.wait_for_variables({"odo_snapshot"})
                print("Leitura do snapshot iniciada.", flush=True)

                linhas = []

                print("Movimento 80/120 iniciado.", flush=True)
                await node.set_variables({
                    "motor.left.target": [80],
                    "motor.right.target": [120],
                })

                for i in range(21):
                    await client.sleep(0.2)

                    if i == 9:
                        await node.set_variables({
                            "motor.left.target": [0],
                            "motor.right.target": [0],
                        })
                        print("Comando de paragem enviado.", flush=True)

                    snapshot = list(node.v.odo_snapshot)

                    if len(snapshot) != 6:
                        raise RuntimeError(
                            f"Snapshot inválido: {snapshot}"
                        )

                    ticks, x, y, theta, ve, vd = map(int, snapshot)

                    linha = {
                        "amostra": i,
                        "ticks": ticks,
                        "x_01mm": x,
                        "y_01mm": y,
                        "theta_b": theta,
                        "vel_esq": ve,
                        "vel_dir": vd,
                    }
                    linhas.append(linha)
                    print(linha, flush=True)


                await node.wait_for_variables({
                    "odo_record_n",
                    "odo_dl_log",
                    "odo_dr_log",
                    "odo_pose_log",
                })

                n = int(node.v.odo_record_n)
                dl = list(map(int, node.v.odo_dl_log))
                dr = list(map(int, node.v.odo_dr_log))
                pose = list(map(int, node.v.odo_pose_log))

                if n != 40 or len(dl) != 40 or len(dr) != 40:
                    raise RuntimeError(
                        f"Buffer incompleto: n={n}, "
                        f"dl={len(dl)}, dr={len(dr)}"
                    )

                dados_buffer = {
                    "periodo_s": 0.1,
                    "n": n,
                    "dl_01mm": dl[:n],
                    "dr_01mm": dr[:n],
                    "pose_aseba": pose,
                }

                destino_json = Path(
                    "resultados/odometria_buffer_40ciclos.json"
                )

                destino_json.write_text(
                    json.dumps(dados_buffer, indent=2),
                    encoding="utf-8"
                )

                print("\\n=== BUFFER ASEBA ===", flush=True)
                print("Ciclos guardados:", n, flush=True)
                print("Soma dl:", sum(dl[:n]), flush=True)
                print("Soma dr:", sum(dr[:n]), flush=True)
                print("Pose Aseba:", pose, flush=True)
                print("JSON:", destino_json, flush=True)

                SAIDA.parent.mkdir(parents=True, exist_ok=True)

                with SAIDA.open(
                    "w", newline="", encoding="utf-8"
                ) as f:
                    writer = csv.DictWriter(
                        f, fieldnames=linhas[0].keys()
                    )
                    writer.writeheader()
                    writer.writerows(linhas)

                print("\n=== RESULTADOS ===")
                print("Incremento de ticks:",
                      linhas[-1]["ticks"] - linhas[0]["ticks"])

                estavel = all(
                    r["x_01mm"] == 0
                    and r["y_01mm"] == 0
                    and r["theta_b"] == 0
                    for r in linhas
                )

                print("Pose permaneceu em zero:", estavel)
                print("CSV:", SAIDA)

            finally:
                try:
                    await node.set_variables({
                        "motor.left.target": [0],
                        "motor.right.target": [0],
                    })
                    if execucao_solicitada:
                        await node.stop()
                    print("Paragem solicitada.", flush=True)
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print("Nó desbloqueado.", flush=True)

        client.run_async_program(testar)


if __name__ == "__main__":
    main()
