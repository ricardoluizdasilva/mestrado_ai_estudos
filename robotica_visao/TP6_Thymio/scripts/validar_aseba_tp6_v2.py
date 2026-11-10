"""TP6 - Validar a compilação Aseba sem carregar o programa."""

from pathlib import Path
from thymiodirect import Thymio
from thymiodirect.assembler import Assembler
from thymio_shutdown import encerrar

PORTA = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

PROGRAMA = Path(
    "resultados/odometria_embarcada_sem_comentarios.aesl"
)

NODE_ESPERADO = 58360


def main():
    th = None
    node_id = None

    try:
        print("=== TP6 - VALIDAÇÃO ASEBA ===", flush=True)

        codigo = PROGRAMA.read_text(encoding="utf-8")

        if "__KD_MILLI__" in codigo:
            raise ValueError("Coeficiente Kd não substituído.")

        print("Programa:", PROGRAMA, flush=True)

        th = Thymio(
            serial_port=PORTA,
            refreshing_rate=0.2,
            refreshing_coverage={"motor.left.speed"},
        )

        print("A estabelecer comunicação...", flush=True)

        th.connect()

        node_id = th.first_node()
        print("Thymio identificado:", node_id, flush=True)

        if node_id != NODE_ESPERADO:
            raise RuntimeError(
                f"ID inesperado: {node_id}"
            )

        connection = th.thymio_proxy.connection
        remote_node = connection.remote_nodes[node_id]

        print("\nA compilar código Aseba...", flush=True)

        assembler = Assembler(remote_node, codigo)
        bytecode = assembler.assemble()

        print("Compilação concluída.", flush=True)
        print("Instruções de bytecode:", len(bytecode), flush=True)

        print("\nVALIDAÇÃO: OK", flush=True)
        print("Bytecode não enviado ao robô.", flush=True)
        print("Programa Aseba não executado.", flush=True)

    finally:
        if th is not None:
            print("\nA encerrar comunicação...", flush=True)
            encerrar(th, node_id)


if __name__ == "__main__":
    main()
