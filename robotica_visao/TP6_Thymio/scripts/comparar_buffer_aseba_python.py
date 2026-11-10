"""TP6 - Comparação quantitativa Aseba vs. Python."""

import json
import math
from pathlib import Path

ENTRADA = Path("resultados/odometria_buffer_ensaio2.json")
SAIDA = Path("resultados/comparacao_aseba_python.json")

L_CM = 9.35
UNIDADE_CM = 0.01
ASEBA_RAD = math.pi / 32768

dados = json.loads(ENTRADA.read_text(encoding="utf-8"))

n = int(dados["n"])
dl = dados["dl_01mm"]
dr = dados["dr_01mm"]
pose_aseba = dados["pose_aseba"]

assert 0 < n <= 40
assert len(dl) == n
assert len(dr) == n
assert len(pose_aseba) == 3

# Integração Python com os incrementos quantizados no Aseba.
x = 0.0
y = 0.0
theta = 0.0
distancia = 0.0

for dl_i, dr_i in zip(dl, dr):
    dl_cm = dl_i * UNIDADE_CM
    dr_cm = dr_i * UNIDADE_CM

    ds = (dl_cm + dr_cm) / 2
    dtheta = (dr_cm - dl_cm) / L_CM

    theta_medio = theta + dtheta / 2

    x += ds * math.cos(theta_medio)
    y += ds * math.sin(theta_medio)
    theta += dtheta

    distancia += ds

# Converter pose embarcada.
xa = pose_aseba[0] * UNIDADE_CM
ya = pose_aseba[1] * UNIDADE_CM
ta = pose_aseba[2] * ASEBA_RAD

# Diferenças.
erro_x = xa - x
erro_y = ya - y
erro_theta = math.degrees(
    math.atan2(
        math.sin(ta - theta),
        math.cos(ta - theta)
    )
)
erro_posicao = math.hypot(erro_x, erro_y)

print("=== TP6 - COMPARAÇÃO ASEBA / PYTHON ===")
print(f"Ciclos utilizados: {n}")
print(f"Soma dl: {sum(dl)} unidades de 0,1 mm")
print(f"Soma dr: {sum(dr)} unidades de 0,1 mm")
print(f"Percurso assinado estimado: {distancia:.4f} cm")

print("\n                 Aseba       Python")
print(f"X (cm)         {xa:9.4f}   {x:9.4f}")
print(f"Y (cm)         {ya:9.4f}   {y:9.4f}")
print(
    f"Theta (graus)  {math.degrees(ta):9.4f}"
    f"   {math.degrees(theta):9.4f}"
)

print("\n=== DIFERENÇAS ===")
print(f"Erro X: {erro_x:+.4f} cm")
print(f"Erro Y: {erro_y:+.4f} cm")
print(f"Erro posição: {erro_posicao:.4f} cm")
print(f"Erro angular: {erro_theta:+.4f} graus")

resultado = {
    "ciclos": n,
    "kd_representado": 0.035,
    "distancia_entre_rodas_cm": L_CM,
    "pose_aseba": {
        "x_cm": xa,
        "y_cm": ya,
        "theta_graus": math.degrees(ta),
    },
    "pose_python": {
        "x_cm": x,
        "y_cm": y,
        "theta_graus": math.degrees(theta),
    },
    "erros_aseba_menos_python": {
        "x_cm": erro_x,
        "y_cm": erro_y,
        "posicao_cm": erro_posicao,
        "theta_graus": erro_theta,
    },
}

SAIDA.write_text(
    json.dumps(resultado, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("\nResultados guardados em:", SAIDA)
