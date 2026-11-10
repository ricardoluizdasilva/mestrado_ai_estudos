"""TP6 - Compilar e carregar Aseba, sem executar o programa."""

from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path(
    "resultados/odometria_embarcada_calibrada.aesl"
)

NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")

    if "__KD_MILLI__" in codigo:
        raise ValueError("O ganho Kd não foi substituído.")

    print("=== TP6 — COMPILAÇÃO ASEBA COM TDM ===", flush=True)
    print("Programa:", PROGRAMA, flush=True)

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def tarefa():
            print("A procurar o Thymio...", flush=True)

            node = await client.wait_for_node()

            print("Nó encontrado:", node.id_str, flush=True)
            print("Nome:", node.props.get("name"), flush=True)

            if node.id_str != NODE_ID:
                raise RuntimeError("Nó diferente do esperado.")

            if node.props.get("name") != "Thymio-II Wireless":
                raise RuntimeError("Dispositivo inesperado.")

            print("A solicitar acesso exclusivo...", flush=True)

            await node.lock()
            print("Bloqueio do nó: OK", flush=True)

            try:
                print("A compilar e carregar Aseba...", flush=True)

                erro = await node.compile(codigo)

                if erro is not None:
                    raise RuntimeError(
                        f"Erro de compilação Aseba: {erro}"
                    )

                print("Compilação: OK", flush=True)
                print("Programa carregado.", flush=True)
                print("Programa NÃO executado.", flush=True)

            finally:
                await node.unlock()
                print("Nó desbloqueado.", flush=True)

        client.run_async_program(tarefa)


if __name__ == "__main__":
    main()
