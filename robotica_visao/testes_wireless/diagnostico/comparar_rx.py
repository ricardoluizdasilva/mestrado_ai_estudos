import json
from pathlib import Path
from itertools import zip_longest

BASE = Path("diagnostico")


def carregar(nome):
    caminho = BASE / nome

    with caminho.open(encoding="utf-8") as f:
        registos = [json.loads(l) for l in f if l.strip()]

    # Preservar apenas operações de leitura
    return [
        r for r in registos
        if r["direction"] == "RX"
    ]


def reconstruir_mensagens(registos):
    """
    Agrupa as operações RX no formato de leitura
    utilizado pelo thymiodirect:
    comprimento, nó de origem, ID e payload.

    Verifica apenas a estrutura, não a validade
    semântica dos tipos de mensagens.
    """
    mensagens = []
    erros = []
    i = 0

    while i < len(registos):
        inicio = i

        if i + 3 > len(registos):
            erros.append((inicio, "Cabeçalho incompleto"))
            break

        a, b, c = registos[i:i + 3]
        i += 3

        if (a["length"], b["length"], c["length"]) != (2, 2, 2):
            erros.append((
                inicio,
                "Comprimentos inesperados no cabeçalho"
            ))
            break

        tamanho = int.from_bytes(bytes.fromhex(a["hex"]), "little")
        origem = int.from_bytes(bytes.fromhex(b["hex"]), "little")
        tipo = int.from_bytes(bytes.fromhex(c["hex"]), "little")

        payload = b""

        if tamanho:
            if i >= len(registos):
                erros.append((inicio, "Payload ausente"))
                break

            r = registos[i]
            i += 1

            if r["truncated"]:
                erros.append((inicio, "Payload truncado no log"))
                break

            payload = bytes.fromhex(r["hex"])

            if len(payload) != tamanho:
                erros.append((
                    inicio,
                    f"Payload: esperado {tamanho}, recebido {len(payload)}"
                ))
                break

        mensagens.append({
            "seq": a["seq"],
            "elapsed_s": a["elapsed_s"],
            "tamanho": tamanho,
            "origem": origem,
            "tipo": tipo,
            "payload": payload.hex(),
        })

    return mensagens, erros


ficheiros = {
    "WSL2": "aseba_trace_wsl.jsonl",
    "PI5": "aseba_trace_pi5.jsonl",
}

resultados = {}

for nome, ficheiro in ficheiros.items():
    registos = carregar(ficheiro)
    mensagens, erros = reconstruir_mensagens(registos)
    resultados[nome] = mensagens

    print(f"\n=== {nome} ===")
    print("Operações RX:", len(registos))
    print("Mensagens reconstruídas:", len(mensagens))
    print("Erros estruturais:", erros[:5])

    print("\nPrimeiras mensagens:")
    for m in mensagens[:10]:
        print(
            f"seq={m['seq']:4} "
            f"origem={m['origem']:5} "
            f"tipo=0x{m['tipo']:04X} "
            f"payload={m['payload'][:32]}"
        )

print("\n=== PRIMEIRA DIFERENÇA ===")

wsl = resultados["WSL2"]
pi5 = resultados["PI5"]

for indice, (a, b) in enumerate(zip_longest(wsl, pi5)):
    if a is None or b is None:
        print("Uma das capturas terminou no índice:", indice)
        break

    assinatura_a = (a["origem"], a["tipo"], a["payload"])
    assinatura_b = (b["origem"], b["tipo"], b["payload"])

    if assinatura_a != assinatura_b:
        print("Índice:", indice)
        print("WSL2:", a)
        print("PI5 :", b)
        break
else:
    print("Não foram encontradas diferenças.")
