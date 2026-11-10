"""TP6 - Teste estático da odometria embarcada via TDM."""

import csv
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_teste.aesl")
SAIDA = Path("resultados/odometria_estatica_tdm.csv")

NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"
DURACAO_S = 5
INTERVALO_S = 0.5

VARIAVEIS = {
    "odo_ticks",
    "odo_x_01mm",
    "odo_y_01mm",
    "odo_theta_b",
    "motor.left.speed",
    "motor.right.speed",
}


def verificar_resultado(resultado, operacao):
    if resultado is not None:
        raise RuntimeError(f"{operacao}: {resultado}")


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")
    assert "var odo_ticks = 0" in codigo

    print("=== TESTE ESTÁTICO TP6 ===", flush=True)

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def tarefa():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
                raise RuntimeError("Thymio inesperado")

            print("Thymio:", node.id_str, flush=True)

            await node.lock()
            iniciado = False

            try:
                parar_motores = {
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                }

                await node.set_variables(parar_motores)

                erro = await node.compile(codigo)
                verificar_resultado(erro, "Compilação")

                print("Compilação: OK", flush=True)

                await node.watch(variables=True)

                erro = await node.run()
                verificar_resultado(erro, "Execução")
                iniciado = True

                print("Programa iniciado.", flush=True)

                await node.wait_for_variables(VARIAVEIS)

                linhas = []

                for i in range(int(DURACAO_S / INTERVALO_S) + 1):
                    await client.sleep(0.1 if i == 0 else INTERVALO_S)

                    linha = {
                        "tempo_s": round(i * INTERVALO_S, 2),
                        "ticks": int(node.v.odo_ticks),
                        "x_01mm": int(node.v.odo_x_01mm),
                        "y_01mm": int(node.v.odo_y_01mm),
                        "theta_b": int(node.v.odo_theta_b),
                        "vel_esq": int(node.v.motor.left.speed),
                        "vel_dir": int(node.v.motor.right.speed),
                    }

                    linhas.append(linha)
                    print(linha, flush=True)

                SAIDA.parent.mkdir(parents=True, exist_ok=True)

                with SAIDA.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(
                        f, fieldnames=list(linhas[0])
                    )
                    writer.writeheader()
                    writer.writerows(linhas)

                delta_ticks = linhas[-1]["ticks"] - linhas[0]["ticks"]

                print("\n=== RESULTADOS ===")
                print("Incremento do contador:", delta_ticks)
                print("CSV:", SAIDA)

                if delta_ticks <= 0:
                    print("ALERTA: temporizador sem incremento!")

                if any(
                    (r["x_01mm"], r["y_01mm"], r["theta_b"])
                    != (0, 0, 0)
                    for r in linhas
                ):
                    print("ALERTA: pose diferente de zero!")
                else:
                    print("Pose permaneceu em zero.")

            finally:
                try:
                    if iniciado:
                        await node.stop()
                        print("Programa parado.", flush=True)
                finally:
                    try:
                        await node.set_variables({
                            "motor.left.target": [0],
                            "motor.right.target": [0],
                        })
                        print("Motores: paragem solicitada.", flush=True)
                    finally:
                        try:
                            await node.watch(variables=False)
                        finally:
                            await node.unlock()
                            print("Nó desbloqueado.", flush=True)

        client.run_async_program(tarefa)


if __name__ == "__main__":
    main()
