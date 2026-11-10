
"""TP6 — Teste de sequência V3.6 sem movimento físico."""

import json
import time
from pathlib import Path

from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v36_sim.aesl")
SAIDA = Path("resultados/sequencia_v36_sim.json")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"


def validar_programa(codigo):
    import re

    comandos = re.findall(
        r"(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$",
        codigo,
    )
    if not comandos or any(c.strip() != "0" for c in comandos):
        raise RuntimeError(
            "Programa contém comandos motores não permitidos."
        )


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")
    validar_programa(codigo)

    with ClientAsync(tdm_addr="127.0.0.1", tdm_port=8596) as client:

        async def testar():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
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
                    "seq_state",
                    "seq_progress",
                    "seq_angle",
                    "seq_line_ticks",
                    "seq_turn_ticks",
                    "seq_history",
                    "seq_history_n",
                    "seq_global_angle",
                })

                await client.sleep(0.3)

                if int(node.v.seq_state) != 0:
                    raise RuntimeError("Controlador não está pronto")

                await node.set_variables({"seq_request": [1]})
                print("Simulação V3.6 iniciada.", flush=True)

                inicio = time.monotonic()
                estado = 0

                while time.monotonic() - inicio < 16:
                    await client.sleep(0.25)

                    estado = int(node.v.seq_state)

                    if estado in (5, 6):
                        break

                await client.sleep(0.3)

                n = int(node.v.seq_history_n)
                historico = list(
                    map(int, node.v.seq_history)
                )[:n]

                resultado = {
                    "estado": int(node.v.seq_state),
                    "historico": historico,
                    "ciclos_reta": int(node.v.seq_line_ticks),
                    "ciclos_rotacao": int(node.v.seq_turn_ticks),
                    "distancia_cm": int(node.v.seq_progress) / 1000,
                    "angulo_graus":
                        int(node.v.seq_angle) * 180 / 32768,
                    "orientacao_global_simulada_graus":
                        int(node.v.seq_global_angle) * 180 / 32768,
                }

                print("\n=== RESULTADO V3.6 ===")
                for campo, valor in resultado.items():
                    print(f"{campo}: {valor}", flush=True)

                if resultado["estado"] != 5:
                    raise RuntimeError(
                        "Sequência não terminou corretamente."
                    )

                assert historico == [1, 2, 3, 4, 5]
                assert resultado["ciclos_reta"] == 39
                assert resultado["ciclos_rotacao"] == 32
                assert resultado["distancia_cm"] == 9.75
                assert resultado["angulo_graus"] == 90.0

                SAIDA.parent.mkdir(parents=True, exist_ok=True)
                SAIDA.write_text(
                    json.dumps(
                        resultado,
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                print("\nSEQUENCIA V3.6: OK")
                print("Resultados:", SAIDA)

            finally:
                try:
                    await parar()
                    if iniciado:
                        await node.stop()
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print(
                            "Programa parado. No desbloqueado.",
                            flush=True,
                        )

        client.run_async_program(testar)


if __name__ == "__main__":
    main()
