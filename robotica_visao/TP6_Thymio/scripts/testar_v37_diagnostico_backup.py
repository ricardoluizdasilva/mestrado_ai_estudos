"""TP6 - Validar duas sequências simuladas da V3.7."""

import json
import re
import time
from pathlib import Path

from tdmclient import ClientAsync

P = Path("resultados/diagnostico_v37_2lados.aesl")
SAIDA = Path("resultados/diagnostico_v37_2lados.json")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

codigo = P.read_text(encoding="utf-8")

comandos = re.findall(
    r"(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$",
    codigo
)
assert comandos and all(c.strip() == "0" for c in comandos)

with ClientAsync(tdm_addr="127.0.0.1", tdm_port=8596) as client:

    async def executar():
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
                raise RuntimeError(erro)

            await node.watch(variables=True)
            iniciado = True

            erro = await node.run()
            if erro is not None:
                raise RuntimeError(erro)

            await node.wait_for_variables({
                "seq_state", "seq_side", "seq_goal_sides",
                "seq_history", "seq_history_n",
                "seq_progress", "seq_angle_b",
                "seq_fault", "odo_theta_b", "odo_turns",
            })

            await client.sleep(0.4)
            assert int(node.v.seq_state) == 0

            await node.set_variables({
                "seq_abort": [0],
                "seq_arm": [1],
            })

            # Aguardar confirmação do armamento pelo TDM.
            prazo = time.monotonic() + 2.0
            while time.monotonic() < prazo:
                await client.sleep(0.1)

                arm = int(node.v.seq_arm)
                estado = int(node.v.seq_state)
                falha = int(node.v.seq_fault)

                if estado != 0 or falha != 0:
                    raise RuntimeError(
                        f"Estado inesperado: "
                        f"state={estado}, fault={falha}"
                    )

                if arm == 1:
                    break
            else:
                raise RuntimeError(
                    "Armamento não confirmado em 2 segundos"
                )

            print("Armamento confirmado.", flush=True)

            await node.set_variables({"seq_request": [1]})

            inicio = time.monotonic()

            while time.monotonic() - inicio < 27:
                await client.sleep(0.25)
                if int(node.v.seq_state) in (5, 6):
                    break
            else:
                raise TimeoutError("Sequência sem conclusão")

            await client.sleep(0.3)

            n = int(node.v.seq_history_n)
            historico = list(map(int, node.v.seq_history))[:n]

            resultado = {
                "estado": int(node.v.seq_state),
                "falha": int(node.v.seq_fault),
                "lados": int(node.v.seq_side),
                "historico": historico,
                "distancia_ultimo_lado_cm":
                    int(node.v.seq_progress) / 1000,
                "angulo_ultima_curva_graus":
                    int(node.v.seq_angle_b) * 180 / 32768,
            }

            print("=== SIMULAÇÃO V3.7 ===")
            for chave, valor in resultado.items():
                print(f"{chave}: {valor}")

            assert resultado["estado"] == 5
            assert resultado["falha"] == 0
            assert resultado["lados"] == 2
            assert historico == [1, 2, 3, 4, 1, 2, 3, 4, 5]
            assert resultado["distancia_ultimo_lado_cm"] == 9.75
            assert resultado["angulo_ultima_curva_graus"] == 90.0

            SAIDA.write_text(
                json.dumps(resultado, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            theta_global = (
                int(node.v.odo_theta_b)
                + 65536 * int(node.v.odo_turns)
            ) * 180 / 32768

            print(
                "Orientação global acumulada:",
                theta_global,
                "graus"
            )
            assert abs(theta_global - 180) <= 1

            print("DIAGNÓSTICO V3.7: OK")

        finally:
            try:
                await node.set_variables({
                    "seq_abort": [1],
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })
                if iniciado:
                    await node.stop()
            finally:
                try:
                    await node.watch(variables=False)
                finally:
                    await node.unlock()
                    print("Programa parado. Nó desbloqueado.")

    client.run_async_program(executar)
