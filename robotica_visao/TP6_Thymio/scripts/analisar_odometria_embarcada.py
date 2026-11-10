"""TP6 - Análise dos resultados da odometria embarcada."""

import csv
import math
from pathlib import Path

ficheiro = Path("resultados/odometria_dinamica_tdm.csv")

with ficheiro.open(newline="", encoding="utf-8") as f:
    dados = list(csv.DictReader(f))

if not dados:
    raise ValueError("CSV vazio")

def valor(linha, campo):
    return float(linha[campo])

primeiro = dados[0]
ultimo = dados[-1]

x = valor(ultimo, "x_01mm") / 100
y = valor(ultimo, "y_01mm") / 100

theta = valor(ultimo, "theta_b") * 180 / 32768

distancia_reta = math.hypot(x, y)

ticks = int(ultimo["ticks"]) - int(primeiro["ticks"])

print("=== TP6 - ODOMETRIA EMBARCADA ===")
print(f"Amostras: {len(dados)}")
print(f"Ticks registados: {ticks}")
print(f"X final: {x:.4f} cm")
print(f"Y final: {y:.4f} cm")
print(f"Orientação final: {theta:.4f} graus")
print(f"Distância em linha reta à origem: {distancia_reta:.4f} cm")

inconsistencias = []

for anterior, atual in zip(dados, dados[1:]):
    tick_anterior = int(anterior["ticks"])
    tick_atual = int(atual["ticks"])

    pose_anterior = tuple(
        anterior[c] for c in ("x_01mm", "y_01mm", "theta_b")
    )
    pose_atual = tuple(
        atual[c] for c in ("x_01mm", "y_01mm", "theta_b")
    )

    if tick_atual == tick_anterior and pose_atual != pose_anterior:
        inconsistencias.append(atual["tempo_s"])

print("\n=== CONSISTÊNCIA DAS LEITURAS ===")
print("Alterações da pose sem alteração do tick:", len(inconsistencias))
print("Instantes:", inconsistencias)

ultimas = dados[-5:]
estavel = all(
    tuple(r[c] for c in ("x_01mm", "y_01mm", "theta_b"))
    == tuple(ultimo[c] for c in ("x_01mm", "y_01mm", "theta_b"))
    for r in ultimas
)

print("Pose estável nas últimas 5 amostras:", estavel)

if inconsistencias:
    print(
        "Nota: podem existir leituras não sincronizadas "
        "ou atualizações incompletas pelo TDM."
    )

print("\nAnálise concluída.")
