
"""TP6 - Exercicio 9: seguranca da correcao V4.2.

Comprova que a correcao e rejeitada no estado inicial.
Nao autoriza o movimento do robot.
"""

import time
from pathlib import Path

from tdmclient import ClientAsync

PROGRAMA = Path(
    "aseba/odometria_embarcada_v42_correcao.aesl"
)
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"


def valor(node, nome):
    dado = getattr(node.v, nome)

    if not isinstance(dado, (int, float)):
        raise RuntimeError(
            f"Variavel ainda indisponivel: {nome}"
        )

    return int(dado)


def variavel_disponivel(node, nome):
    dado = getattr(node.v, nome)
    return isinstance(dado, (int, float))

async def aguardar(client, condicao, descricao, segundos=5):
    limite = time.monotonic() + segundos

    while time.monotonic() < limite:
        await client.sleep(0.1)
        if condicao():
            return

    raise TimeoutError(descricao)


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
            iniciou = False

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
                        f"Erro de compilacao: {erro}"
                    )

                await node.watch(variables=True)

                # Garantir que nao existe autorizacao
                # para iniciar a trajetoria.
                await node.set_variables({
                    "seq_arm": [0],
                    "seq_request": [0],
                    "seq_abort": [0],
                    "corr_request": [0],
                })

                # Limpar pedidos antes de iniciar.
                await node.set_variables({
                    "seq_arm": [0],
                    "seq_request": [0],
                    "seq_abort": [0],
                    "corr_request": [0],
                })

                # Iniciar a V4.2.
                iniciou = True
                erro = await node.run()

                if erro is not None:
                    raise RuntimeError(f"Erro de execucao: {erro}")

                # Solicitar as variaveis.
                await node.wait_for_variables({
                    "seq_state",
                    "seq_fault",
                    "seq_arm",
                    "seq_request",
                    "corr_request",
                    "corr_applied",
                    "corr_rejected",
                    "corr_status",
                    "motor.left.target",
                    "motor.right.target",
                    "odo_x_coarse",
                    "odo_y_coarse",
                })

                # Confirmar que os valores ja estao acessiveis.
                await aguardar(
                    client,
                    lambda: all(
                        variavel_disponivel(node, nome)
                        for nome in (
                            "seq_state",
                            "seq_arm",
                            "seq_request",
                            "corr_applied",
                            "corr_rejected",
                        )
                    ),
                    "Variaveis Aseba nao recebidas",
                )

                # Verificar o estado inicial.
                assert valor(node, "seq_state") == 0
                assert valor(node, "seq_arm") == 0
                assert valor(node, "seq_request") == 0

                await aguardar(
                    client,
                    lambda: (
                        valor(node, "seq_arm") == 0
                        and valor(node, "seq_request") == 0
                    ),
                    "Autorizacao de movimento nao limpa",
                )

                iniciou = True
                erro = await node.run()

                if erro is not None:
                    raise RuntimeError(
                        f"Erro de execucao: {erro}"
                    )


                await aguardar(
                    client,
                    lambda: (
                        valor(node, "seq_arm") == 0
                        and valor(node, "seq_request") == 0
                    ),
                    "Autorizacao de movimento nao limpa",
                )
                   

                await client.sleep(0.3)

                if valor(node, "seq_state") != 0:
                    raise RuntimeError(
                        "Estado inicial inesperado"
                    )

                if valor(node, "seq_arm") != 0:
                    raise RuntimeError(
                        "Controlador armado indevidamente"
                    )

                if valor(node, "seq_request") != 0:
                    raise RuntimeError(
                        "Pedido de movimento inesperado"
                    )

                print("=== SEGURANCA V4.2 ===", flush=True)
                print("Estado inicial: 0", flush=True)

                aplicadas = valor(node, "corr_applied")
                rejeitadas = valor(node, "corr_rejected")

                # Referencia deliberadamente diferente
                # da origem para detetar aplicacao indevida.
                await node.set_variables({
                    "corr_ref_x_coarse": [1000],
                    "corr_ref_x_rem": [0],
                    "corr_ref_y_coarse": [500],
                    "corr_ref_y_rem": [0],
                    "corr_ref_theta_b": [16384],
                    "corr_ref_turns": [0],
                })

                await node.set_variables({
                    "corr_request": [1]
                })

                await aguardar(
                    client,
                    lambda: (
                        valor(node, "corr_rejected")
                        == rejeitadas + 1
                        and valor(node, "corr_request") == 0
                    ),
                    "Pedido nao foi rejeitado",
                )

                await client.sleep(0.2)

                assert valor(node, "corr_applied") == aplicadas
                assert valor(node, "corr_status") == -1
                assert valor(node, "seq_state") == 0
                assert valor(node, "seq_fault") == 0
                assert valor(node, "odo_x_coarse") == 0
                assert valor(node, "odo_y_coarse") == 0

                motores = (
                    valor(node, "motor.left.target"),
                    valor(node, "motor.right.target"),
                )

                assert motores == (0, 0), motores

                print(
                    "Pedido de correcao: REJEITADO",
                    flush=True,
                )
                print(
                    "Correcoes aplicadas:",
                    valor(node, "corr_applied"),
                    flush=True,
                )
                print(
                    "Correcoes rejeitadas:",
                    valor(node, "corr_rejected"),
                    flush=True,
                )
                print(
                    "Estado:",
                    valor(node, "seq_state"),
                    flush=True,
                )
                print(
                    "Motores:",
                    motores,
                    flush=True,
                )

                print(
                    "\nSEGURANCA V4.2: OK",
                    flush=True,
                )

            finally:
                try:
                    await parar()

                    if iniciou:
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
