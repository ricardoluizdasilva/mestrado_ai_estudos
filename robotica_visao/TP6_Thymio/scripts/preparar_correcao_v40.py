"""TP6 — V4.0: correção de pose com referência configurável."""

from pathlib import Path

origem = Path("aseba/correcao_pose_v39.aesl")
destino = Path("aseba/correcao_pose_v40.aesl")

codigo = origem.read_text(encoding="utf-8")

declaracoes = """
var corr_ref_x_coarse = 0
var corr_ref_x_rem = 0
var corr_ref_y_coarse = 0
var corr_ref_y_rem = 0
var corr_ref_theta_b = 0
var corr_ref_turns = 0
"""

marcador = "timer.period[0] = 100"

if codigo.count(marcador) != 1:
    raise RuntimeError("Temporizador não encontrado")

codigo = codigo.replace(
    marcador, declaracoes + "\n" + marcador, 1
)

antigo = """        odo_x_coarse = 0
        odo_x_rem = 0
        odo_y_coarse = 0
        odo_y_rem = 0

        odo_x_01mm = 0
        odo_y_01mm = 0

        # 360 graus acumulados = theta normalizado 0, turns 1
        odo_theta_b = 0
        odo_turns = 1"""

novo = """        odo_x_coarse = corr_ref_x_coarse
        odo_x_rem = corr_ref_x_rem
        odo_y_coarse = corr_ref_y_coarse
        odo_y_rem = corr_ref_y_rem

        odo_x_01mm = odo_x_coarse
        odo_y_01mm = odo_y_coarse

        odo_theta_b = corr_ref_theta_b
        odo_turns = corr_ref_turns"""

if codigo.count(antigo) != 1:
    raise RuntimeError("Bloco de correção não encontrado")

codigo = codigo.replace(antigo, novo, 1)

if destino.exists():
    raise FileExistsError(destino)

destino.write_text(codigo, encoding="utf-8")

print("V4.0 criada:", destino)
print("Referência configurável: X, Y e orientação.")
print("V3.9 preservada.")
