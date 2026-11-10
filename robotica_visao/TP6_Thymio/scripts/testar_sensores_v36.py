"""TP6 - Verificação estática da V3.6 física."""

import json
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path(
    "resultados/odometria_embarcada_v36_fisica.aesl"
)
SAIDA = Path("resultados/sensores_v36.json")
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
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            execucao_solicitada = False
            amostras = []

            async def parar():
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

            try:
                await parar()

                erro = await node.compile(codigo)
                if erro is not None:
                    raise RuntimeError(
                        f"Compilação Aseba: {erro}"
                    )

                await node.watch(variables=True)

                execucao_solicitada = True
                erro = await node.run()
                if erro is not None:
                    raise RuntimeError(
                        f"Execução Aseba: {erro}"
                    )

                await node.wait_for_variables({
                    "seq_state",
                    "seq_arm",
                    "seq_request",
                    "seq_fault",
                    "odo_ticks",
                    "motor.left.target",
                    "motor.right.target",
                    "prox.horizontal",
                })

                print("=== TESTE DE SEGURANÇA V3.6 ===")
                print("Programa iniciado sem pedido de movimento.")

                for i in range(21):
                    await client.sleep(0.5)

                    dados = {
                        "amostra": i,
                        "ticks": int(node.v.odo_ticks),
                        "state": int(node.v.seq_state),
                        "arm": int(node.v.seq_arm),
                        "request": int(node.v.seq_request),
                        "fault": int(node.v.seq_fault),
                        "motor_left": int(
                            node.v.motor.left.target
                        ),
                        "motor_right": int(
                            node.v.motor.right.target
                        ),
                        "proximidade": list(
                            map(int, node.v.prox.horizontal)
                        ),
                    }

                    amostras.append(dados)
                    print(dados, flush=True)

                    if any((
                        dados["state"] != 0,
                        dados["arm"] != 0,
                        dados["request"] != 0,
                        dados["fault"] != 0,
                        dados["motor_left"] != 0,
                        dados["motor_right"] != 0,
                    )):
                        raise RuntimeError(
                            "Estado inesperado: teste interrompido"
                        )

                incremento = (
                    amostras[-1]["ticks"]
                    - amostras[0]["ticks"]
                )

                print("\n=== RESULTADO ===")
                print("Incremento do temporizador:", incremento)
                print("Estados e motores: OK")

                if incremento < 35:
                    raise RuntimeError(
                        "Temporizador com incremento insuficiente"
                    )

                SAIDA.parent.mkdir(
                    parents=True, exist_ok=True
                )
                SAIDA.write_text(
                    json.dumps(
                        amostras,
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                print("TESTE DE SENSORES V3.6: OK")
                print("Resultados:", SAIDA)

            finally:
                try:
                    await parar()
                    if execucao_solicitada:
                        await node.stop()
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print(
                            "Paragem solicitada. Nó desbloqueado."
                        )

        client.run_async_program(testar)


if __name__ == "__main__":
    main()
