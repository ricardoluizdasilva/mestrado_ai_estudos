"""TP6 - Exercicio 9: correcao embarcada de pose."""

from pathlib import Path

src = Path("resultados/odometria_embarcada_v31.aesl")
dst = Path("aseba/correcao_pose_v39.aesl")

codigo = src.read_text(encoding="utf-8")

declaracoes = """
# Exercicio 9 - referencia conhecida
var corr_request = 0
var corr_applied = 0
"""

marcador = "timer.period[0] = 100"

if codigo.count(marcador) != 1:
    raise RuntimeError("Temporizador nao encontrado")

codigo = codigo.replace(
    marcador,
    declaracoes + "\n" + marcador,
    1
)

# A correcao ocorre no final do ciclo de odometria.
codigo += """

    # Correcao absoluta para origem apos uma volta completa
    if corr_request == 1 then
        odo_x_coarse = 0
        odo_x_rem = 0
        odo_y_coarse = 0
        odo_y_rem = 0

        odo_x_01mm = 0
        odo_y_01mm = 0

        # 360 graus acumulados = theta normalizado 0, turns 1
        odo_theta_b = 0
        odo_turns = 1

        corr_request = 0
        corr_applied = corr_applied + 1
    end
"""

if dst.exists():
    raise FileExistsError(dst)

dst.write_text(codigo, encoding="utf-8")

print("Criado:", dst)
print("Correcao apenas mediante pedido explicito.")
print("Versoes anteriores preservadas.")
