"""TP6 - Exercicio 9: preparar correcao a partir de medicao fisica."""

import json
import math
from pathlib import Path

SAIDA = Path("resultados/validacao_ex9/correcao_fisica_ex9.json")

# Pose final estimada pela V3.8, retirada do log.
odometria = {
    "x_cm": -0.228,
    "y_cm": 0.747,
    "theta_graus": 356.759,
}

# Pose medida fisicamente, confirmada pelo operador.
medicao = {
    "x_cm": -2.0,
    "y_cm": 0.5,
    "theta_graus": 342.0,
}


def codificar_coordenada(cm):
    unidades = round(cm * 1000)  # unidades de 0,01 mm
    coarse = math.trunc(unidades / 10)
    rem = unidades - coarse * 10
    return coarse, rem


def codificar_angulo(graus):
    voltas = math.floor((graus + 180) / 360)
    normalizado = graus - 360 * voltas
    theta_b = round(normalizado * 32768 / 180)
    return theta_b, voltas


xc, xr = codificar_coordenada(medicao["x_cm"])
yc, yr = codificar_coordenada(medicao["y_cm"])
theta_b, turns = codificar_angulo(medicao["theta_graus"])

referencia_aseba = {
    "corr_ref_x_coarse": xc,
    "corr_ref_x_rem": xr,
    "corr_ref_y_coarse": yc,
    "corr_ref_y_rem": yr,
    "corr_ref_theta_b": theta_b,
    "corr_ref_turns": turns,
}

delta_x = medicao["x_cm"] - odometria["x_cm"]
delta_y = medicao["y_cm"] - odometria["y_cm"]
delta_theta = (
    (medicao["theta_graus"] - odometria["theta_graus"] + 180)
    % 360 - 180
)

resultado = {
    "tipo": "correcao_por_medicao_fisica_manual",
    "odometria_antes": odometria,
    "pose_fisica_medida": medicao,
    "correcao": {
        "delta_x_cm": delta_x,
        "delta_y_cm": delta_y,
        "delta_theta_graus": delta_theta,
        "discrepancia_posicional_mm": (
            math.hypot(delta_x, delta_y) * 10
        ),
    },
    "referencia_aseba": referencia_aseba,
    "aplicada_no_robot": False,
}

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(
    json.dumps(resultado, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("=== CORRECAO FISICA EX9 ===")
print("Odometria:", odometria)
print("Medicao:", medicao)
print("Correcao:", resultado["correcao"])
print("Referencia Aseba:", referencia_aseba)
print("Ficheiro:", SAIDA)
print("Estado: preparada, ainda nao aplicada no robot")
