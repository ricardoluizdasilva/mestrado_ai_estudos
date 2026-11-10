import csv
import statistics
from pathlib import Path

BASE = Path("resultados")
SAIDA = BASE / "comparacao_tp6.csv"

# Medições manuais em cm, transcritas dos ensaios.
# Ordem: esquerda, ponto médio do eixo, diagonal direita.

MEDIDAS = {
    "esquerda": [
        (5.6, 6.3, 12.7),
        (5.3, 6.5, 12.5),
        (5.2, 6.4, 12.4),
        (5.1, 6.4, 12.2),
        (5.3, 6.7, 12.5),
    ],
    "direita": [
        (7.0, 6.1, 11.8),
        (7.2, 6.3, 12.1),
        (7.6, 6.6, 12.2),
        (8.0, 6.8, 12.0),
        (8.1, 6.9, 12.1),
    ],
}


def media_dp(valores):
    return (
        statistics.mean(valores),
        statistics.stdev(valores),
    )


registos = []

for sentido, medicoes in MEDIDAS.items():
    print(f"\n=== CURVA À {sentido.upper()} ===")

    for n, (esquerda, centro, diagonal) in enumerate(
        medicoes, start=1
    ):
        caminho = (
            BASE / "odometria_curvas"
            / f"odometria_{sentido}_{n}.csv"
        )

        with caminho.open(newline="", encoding="utf-8") as f:
            linhas = list(csv.DictReader(f))

        if not linhas:
            raise ValueError(f"CSV vazio: {caminho}")

        ultima = linhas[-1]

        registo = {
            "sentido": sentido,
            "ensaio": n,
            "manual_esquerda_cm": esquerda,
            "manual_centro_cm": centro,
            "manual_diagonal_cm": diagonal,
            "odo_x_cm": float(ultima["x_cm"]),
            "odo_y_cm": float(ultima["y_cm"]),
            "odo_theta_deg": float(ultima["theta_deg"]),
        }

        registos.append(registo)

        print(
            f"{n}: "
            f"X={registo['odo_x_cm']:.3f} cm | "
            f"Y={registo['odo_y_cm']:.3f} cm | "
            f"Theta={registo['odo_theta_deg']:.3f} graus"
        )

    grupo = [r for r in registos if r["sentido"] == sentido]

    print("\nEstatística da odometria:")

    for campo in ("odo_x_cm", "odo_y_cm", "odo_theta_deg"):
        valores = [r[campo] for r in grupo]
        media, dp = media_dp(valores)

        print(
            f"  {campo}: "
            f"média={media:.3f}, DP={dp:.3f}"
        )

    print("Estatística das medições manuais:")

    for campo in (
        "manual_esquerda_cm",
        "manual_centro_cm",
        "manual_diagonal_cm",
    ):
        valores = [r[campo] for r in grupo]
        media, dp = media_dp(valores)

        print(
            f"  {campo}: "
            f"média={media:.3f}, DP={dp:.3f}"
        )


with SAIDA.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=list(registos[0].keys())
    )
    writer.writeheader()
    writer.writerows(registos)

print(f"\nFicheiro criado: {SAIDA}")
print(
    "NOTA: os dados manuais e odométricos foram "
    "consolidados, mas os erros de pose ainda "
    "não foram calculados por falta de "
    "referenciais geométricos equivalentes."
)
