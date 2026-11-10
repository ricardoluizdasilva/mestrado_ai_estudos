"""TP6 — Trajetória estimada do quadrado V3.8."""

import csv
from pathlib import Path
import matplotlib.pyplot as plt

origem = Path("resultados/sequencia_v38_trajetoria.csv")
saida = Path("resultados/grafico_quadrado_v38.png")

with origem.open(encoding="utf-8", newline="") as f:
    dados = list(csv.DictReader(f))

if not dados:
    raise ValueError("CSV vazio")

necessarias = {"x_cm", "y_cm", "estado"}
if not necessarias.issubset(dados[0]):
    raise ValueError(
        f"Colunas em falta: {necessarias - set(dados[0])}"
    )

x = [0.0] + [float(r["x_cm"]) for r in dados]
y = [0.0] + [float(r["y_cm"]) for r in dados]

# Quadrado nominal: início orientado no eixo X positivo.
ideal_x = [0, 10, 10, 0, 0]
ideal_y = [0, 0, 10, 10, 0]

fig, ax = plt.subplots(figsize=(8, 7))

ax.plot(
    ideal_x, ideal_y, "--",
    linewidth=1.8, label="Quadrado ideal"
)

ax.plot(
    x, y, linewidth=2,
    label="Odometria V3.8"
)

ax.scatter([0], [0], s=65, marker="o", label="Origem")
ax.scatter(
    [x[-1]], [y[-1]], s=90, marker="x",
    label="Posição final registada"
)

ax.set_title("TP6 — Exercício 8: trajetória quadrada")
ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.axis("equal")
ax.grid(True, alpha=0.3)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=2,
    frameon=False
)

ax.annotate(
    "Início (0, 0)",
    xy=(0, 0),
    xytext=(1.8, 2.0),
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=-0.15"
    ),
    fontsize=10
)

ax.annotate(
    "Fim (-0,266; 0,079 cm)",
    xy=(x[-1], y[-1]),
    xytext=(-2.3, 1.4),
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=0.15"
    ),
    fontsize=10
)

ax.text(
    5, 5,
    "Odometria V3.8\n"
    "Erro de fecho: 2,77 mm\n"
    "Erro angular: −0,324°",
    ha="center",
    va="center",
    fontsize=10,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="gray",
        alpha=0.9
    )
)

# Ajustar os limites dos eixos
ax.set_xlim(-1.5, 11)
ax.set_ylim(-1.3, 11)

# Ajustar e guardar o gráfico
fig.tight_layout()
fig.savefig(saida, dpi=180, bbox_inches="tight")
plt.close(fig)

print("Amostras:", len(dados))
print(f"Última amostra: ({x[-1]:+.4f}, {y[-1]:+.4f}) cm")
print("Gráfico:", saida)
