import json
from pathlib import Path
from itertools import zip_longest
from collections import Counter

base = Path("diagnostico")

def carregar(nome):
    with (base / nome).open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def filtrar(registos, direcao):
    return [r for r in registos if r["direction"] == direcao]

wsl = carregar("aseba_trace_wsl.jsonl")
pi5 = carregar("aseba_trace_pi5.jsonl")

for direcao in ("RX", "TX"):
    a = filtrar(wsl, direcao)
    b = filtrar(pi5, direcao)

    print(f"\n=== COMPARAÇÃO {direcao} ===")
    print("WSL2:", len(a), "operações")
    print("PI5 :", len(b), "operações")

    diferencas = []

    for i, (x, y) in enumerate(zip_longest(a, b)):
        if x is None or y is None:
            print("Fim de uma captura no índice:", i)
            break

        # Não comparar timestamps ou números de sequência
        if (x["length"], x["hex"], x["truncated"]) != (
            y["length"], y["hex"], y["truncated"]
        ):
            diferencas.append(i)

    print("Primeiras diferenças:", diferencas[:10])

    if diferencas:
        i = diferencas[0]
        print("\nContexto da primeira diferença:")

        for j in range(max(0, i - 3), min(len(a), len(b), i + 4)):
            print(f"\nÍndice {j}")
            print("WSL2:", a[j])
            print("PI5 :", b[j])

    print("\nTamanhos mais frequentes:")
    print("WSL2:", Counter(x["length"] for x in a).most_common(8))
    print("PI5 :", Counter(x["length"] for x in b).most_common(8))

print("\n=== OPERAÇÕES TRUNCADAS ===")
for nome, registos in (("WSL2", wsl), ("PI5", pi5)):
    truncados = [r for r in registos if r["truncated"]]
    print(nome, "total:", len(truncados))
    print("Primeiros:", [
        (r["seq"], r["length"], r["direction"])
        for r in truncados[:10]
    ])
