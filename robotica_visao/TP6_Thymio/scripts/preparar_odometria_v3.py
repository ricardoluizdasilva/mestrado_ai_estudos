"""TP6 - Criar V3 com coordenadas segmentadas."""

from pathlib import Path

origem = Path("resultados/odometria_embarcada_v2.aesl")
destino = Path("resultados/odometria_embarcada_v3.aesl")

codigo = origem.read_text(encoding="utf-8")


def substituir(antigo, novo):
    global codigo
    if codigo.count(antigo) != 1:
        raise RuntimeError(f"Marcador inesperado: {antigo}")
    codigo = codigo.replace(antigo, novo, 1)


substituir(
    "var odo_x_001mm = 0",
    "var odo_x_coarse = 0\nvar odo_x_rem = 0\nvar odo_x_carry = 0",
)

substituir(
    "var odo_y_001mm = 0",
    "var odo_y_coarse = 0\nvar odo_y_rem = 0\nvar odo_y_carry = 0",
)

substituir(
    "var odo_pose_hi_log[2] = [0, 0]",
    "var odo_pose_hi_log[4] = [0, 0, 0, 0]",
)

substituir(
    """    odo_x_001mm = odo_x_001mm + odo_dx_001mm
    odo_x_01mm = odo_x_001mm / 10""",
    """    odo_x_rem = odo_x_rem + odo_dx_001mm
    odo_x_carry = odo_x_rem / 10
    odo_x_coarse = odo_x_coarse + odo_x_carry
    odo_x_rem = odo_x_rem - odo_x_carry * 10
    odo_x_01mm = odo_x_coarse""",
)

substituir(
    """    odo_y_001mm = odo_y_001mm + odo_dy_001mm
    odo_y_01mm = odo_y_001mm / 10""",
    """    odo_y_rem = odo_y_rem + odo_dy_001mm
    odo_y_carry = odo_y_rem / 10
    odo_y_coarse = odo_y_coarse + odo_y_carry
    odo_y_rem = odo_y_rem - odo_y_carry * 10
    odo_y_01mm = odo_y_coarse""",
)

substituir(
    "odo_pose_hi_log = [odo_x_001mm, odo_y_001mm]",
    """odo_pose_hi_log = [
            odo_x_coarse, odo_x_rem,
            odo_y_coarse, odo_y_rem
        ]""",
)

destino.write_text(codigo, encoding="utf-8")

print("=== ODOMETRIA V3 ===")
print("Criado:", destino)
print("V2 original preservada.")
print("Coordenadas: coarse + residual.")
