"""TP6 - Exercicio 9: correcao de pose por referencia externa."""

import json
import math
from pathlib import Path

SAIDA = Path("resultados/ex9_correcao_pose_simulada.json")

# Pose estimada no segundo quadrado V3.8
pose_odom = {
    "x_cm": -0.266,
    "y_cm": 0.079,
    "theta_graus": 359.676,
}

# Exemplo hipotetico de referencia externa conhecida
pose_ref = {
    "x_cm": 0.0,
    "y_cm": 0.0,
    "theta_graus": 360.0,
}


def diferenca_angular(a, b):
    return (a - b + 180) % 360 - 180


def distancia(p, q):
    return math.hypot(
        p["x_cm"] - q["x_cm"],
        p["y_cm"] - q["y_cm"],
    )


erro_antes = distancia(pose_odom, pose_ref)
erro_ang_antes = diferenca_angular(
    pose_odom["theta_graus"],
    pose_ref["theta_graus"],
)

# Correcao absoluta: referencia aceite como pose verdadeira.
pose_corrigida = pose_ref.copy()

erro_depois = distancia(pose_corrigida, pose_ref)
erro_ang_depois = diferenca_angular(
    pose_corrigida["theta_graus"],
    pose_ref["theta_graus"],
)

resultado = {
    "tipo": "simulacao_com_referencia_ideal",
    "pose_odom": pose_odom,
    "pose_referencia": pose_ref,
    "pose_corrigida": pose_corrigida,
    "erro_antes_cm": erro_antes,
    "erro_depois_cm": erro_depois,
    "erro_angular_antes_graus": erro_ang_antes,
    "erro_angular_depois_graus": erro_ang_depois,
}

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(
    json.dumps(resultado, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("=== TP6 - EXERCICIO 9 ===")
print("Correcao de pose com referencia externa")
print("Tipo de teste: SIMULACAO")
print()
print("Pose odometria:", pose_odom)
print("Pose referencia:", pose_ref)
print("Pose corrigida:", pose_corrigida)
print()
print(f"Erro antes: {erro_antes * 10:.4f} mm")
print(f"Erro depois: {erro_depois * 10:.4f} mm")
print(f"Erro angular antes: {erro_ang_antes:+.4f} graus")
print(f"Erro angular depois: {erro_ang_depois:+.4f} graus")
print()
print("Resultados:", SAIDA)
