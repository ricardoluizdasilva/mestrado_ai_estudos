"""TP6: comparação offline da odometria original e V2."""

import json
import math
from pathlib import Path

p = Path("resultados/odometria_buffer_ensaio2.json")
dados = json.loads(p.read_text(encoding="utf-8"))

dl = dados["dl_01mm"]
dr = dados["dr_01mm"]

if len(dl) != 40 or len(dr) != 40:
    raise ValueError("Esperados 40 incrementos por roda")

x_ref = y_ref = theta_ref = 0.0
x_v2 = y_v2 = theta_b = 0

for left, right in zip(dl, dr):
    # Referência Python com vírgula flutuante
    ds = (left + right) / 2
    dtheta = (right - left) / 935
    mid = theta_ref + dtheta / 2

    x_ref += ds * math.cos(mid)
    y_ref += ds * math.sin(mid)
    theta_ref += dtheta

    # Emulação aproximada da aritmética Aseba V2
    dt_b = math.trunc((right - left) * 10430 / 935)
    mid_b = theta_b + math.trunc(dt_b / 2)

    angulo = mid_b * math.pi / 32768
    cos_b = math.trunc(math.cos(angulo) * 32767)
    sin_b = math.trunc(math.sin(angulo) * 32767)

    ds2 = left + right
    x_v2 += math.trunc(ds2 * cos_b / 6553)
    y_v2 += math.trunc(ds2 * sin_b / 6553)
    theta_b += dt_b

# A referência usa unidades de 0,1 mm.
# A V2 usa unidades de 0,01 mm.
xr, yr = x_ref / 100, y_ref / 100
x2, y2 = x_v2 / 1000, y_v2 / 1000

erro = math.hypot(x2 - xr, y2 - yr)
erro_ang = theta_b * 180 / 32768 - math.degrees(theta_ref)

print("=== SIMULAÇÃO OFFLINE V2 ===")
print(f"Referência: X={xr:.4f} cm, Y={yr:.4f} cm")
print(f"V2 simulada: X={x2:.4f} cm, Y={y2:.4f} cm")
print(f"Diferença posição: {erro * 10:.4f} mm")
print(f"Diferença angular: {erro_ang:+.4f} graus")
print(f"Diferença anterior: 2.5200 mm")

if erro < 0.252:
    print("Melhoria numérica prevista: SIM")
else:
    print("Melhoria numérica prevista: NÃO")

print("Nota: simulação aproximada, não é medição embarcada.")
