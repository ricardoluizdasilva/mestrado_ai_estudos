"""TP6 - Duas rotações relativas simuladas, sem movimento."""

import json
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("aseba/teste_relativo_v33.aesl")
SAIDA = Path("resultados/duas_rotacoes_v33.json")

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
                "ctl_state",
                "ctl_request",
                "ctl_mode",
                "ctl_active_mode",
                "ctl_angle_b",
                "ctl_ticks",
                "odo_theta_b",
                "odo_turns",
            })

            await client.sleep(0.3)

            if int(node.v.ctl_state) != 0:
                raise RuntimeError("Controlador não está pronto")

            await node.set_variables({
                "ctl_mode": [0],
                "ctl_abort": [0],
            })

            resultados = []

            for numero in (1, 2):
                print(
                    f"\n=== MANOBRA SIMULADA {numero} ===",
                    flush=True,
                )

                await node.set_variables({
                    "ctl_request": [1],
                })

                inicio = time.monotonic()
                atividade_observada = False

                while time.monotonic() - inicio < 9:
                    await client.sleep(0.15)

                    estado = int(node.v.ctl_state)

                    if estado in (1, 2):
                        atividade_observada = True

                    if estado == 4:
                        raise RuntimeError(
                            "Controlador abortou a manobra"
                        )

                    if estado == 3 and atividade_observada:
                        break
                else:
                    raise TimeoutError(
                        f"Manobra {numero} não terminou"
                    )

                await client.sleep(0.4)

                theta_rel = int(node.v.ctl_angle_b) * ESCALA
                turns = int(node.v.odo_turns)
                theta_global = (
                    int(node.v.odo_theta_b) + 65536 * turns
                ) * ESCALA

                resultado = {
                    "manobra": numero,
                    "estado": int(node.v.ctl_state),
                    "ciclos": int(node.v.ctl_ticks),
                    "theta_rel_graus": theta_rel,
                    "theta_global_graus": theta_global,
                    "turns": turns,
                }
                resultados.append(resultado)

                print(resultado, flush=True)

                if resultado["estado"] != 3:
                    raise AssertionError("Estado final incorreto")

                if abs(theta_rel - 90) > 3:
                    raise AssertionError(
                        "Ângulo relativo incorreto"
                    )

                if abs(theta_global - 90 * numero) > 3:
                    raise AssertionError(
                        "Orientação global incorreta"
                    )

            SAIDA.parent.mkdir(parents=True, exist_ok=True)
            SAIDA.write_text(
                json.dumps(
                    resultados,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            print("\nDUAS ROTAÇÕES RELATIVAS: OK")
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
                    print("Programa parado e nó desbloqueado.")

    client.run_async_program(executar)
