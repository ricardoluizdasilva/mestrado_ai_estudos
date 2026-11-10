import csv
from pathlib import Path

destino = Path("resultados/calibracao/medicoes.csv")
destino.parent.mkdir(parents=True, exist_ok=True)

registos = []

for n in range(1, 6):
    while True:
        entrada = input(
            f"Distância percorrida no ensaio {n} (cm): "
        ).replace(",", ".")

        try:
            distancia = float(entrada)
            if distancia <= 0:
                raise ValueError
            break
        except ValueError:
            print("Introduza uma distância positiva.")

    registos.append({
        "run_id": f"reta_{n}",
        "log_file": f"resultados/calibracao/reta_{n}.csv",
        "distance_cm": distancia,
        "notes": "",
    })

with destino.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "run_id",
            "log_file",
            "distance_cm",
            "notes",
        ],
    )
    writer.writeheader()
    writer.writerows(registos)

print(f"\nFicheiro criado: {destino}")
