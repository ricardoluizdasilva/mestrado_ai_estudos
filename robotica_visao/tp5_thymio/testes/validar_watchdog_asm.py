
import sys
import time
from pathlib import Path

from thymiodirect import Thymio
from thymiodirect.assembler import Assembler

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "testes"))

from testar_timer_contador import encerrar

ASM = BASE / "src" / "aseba" / "watchdog_motores.asm"
PORTA = "/dev/ttyACM0"


def main():
    if not ASM.is_file():
        raise FileNotFoundError(ASM)

    th = Thymio(serial_port=PORTA)
    node_id = None

    try:
        print("=== VALIDACAO DO WATCHDOG ASEBA ===")
        print("A ligar ao Thymio para obter os metadados...")

        th.connect()
        node_id = th.first_node()

        if node_id is None:
            raise RuntimeError("Thymio nao encontrado.")

        print("Thymio:", node_id)

        # Obter a descricao da memoria e dos eventos.
        conn = th.thymio_proxy.connection
        node = conn.remote_nodes[node_id]

        print("Variaveis existentes:", node.var_total_size)
        print("Capacidade de variaveis:", node.max_var_size)

        offset = node.var_total_size

        # O programa usa seis palavras de memoria.
        if offset + 6 > node.max_var_size:
            raise RuntimeError("Memoria insuficiente.")

        print("Memoria reservada:", offset, "a", offset + 5)

        programa = ASM.read_text(encoding="utf-8")

        # Compilar localmente, sem carregar no Thymio.
        assembler = Assembler(node, programa)
        bytecode = assembler.assemble()

        if not bytecode:
            raise RuntimeError("Bytecode vazio.")

        print("Palavras de bytecode:", len(bytecode))
        print("Primeiras palavras:", bytecode[:12])

        print("\nASSEMBLY: COMPILACAO OK")
        print("Nenhum programa foi carregado no robo.")
        print("Nenhum comando de movimento foi enviado.")

    finally:
        encerrar(th, node_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Validacao interrompida.")
    except Exception as exc:
        print("ERRO:", repr(exc))
        raise
