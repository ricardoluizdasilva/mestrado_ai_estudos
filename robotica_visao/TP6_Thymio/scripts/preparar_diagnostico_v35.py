from pathlib import Path
import re

src = Path("resultados/odometria_embarcada_v35.aesl")
dst = Path("aseba/diagnostico_correcao_v35.aesl")
s = src.read_text(encoding="utf-8")

def trocar(a, b):
    global s
    if s.count(a) != 1:
        raise RuntimeError(f"Marcador inesperado: {a}")
    s = s.replace(a, b, 1)

trocar(
    "timer.period[0] = 100",
    """var test_n = 0
var test_heading[40]
var test_correction[40]

timer.period[0] = 100"""
)

trocar(
    "call math.muldiv(odo_dl_01mm, motor.left.speed, odo_kd_milli, 100)",
    "odo_dl_01mm = 25"
)
trocar(
    "call math.muldiv(odo_dr_01mm, motor.right.speed, odo_kd_milli, 100)",
    "odo_dr_01mm = 25"
)
trocar(
    "call math.muldiv(odo_dtheta_b, odo_diff_01mm, 10430, 935)",
    """if lin_ticks < 10 then
        odo_dtheta_b = -182
    elseif lin_ticks < 20 then
        odo_dtheta_b = 182
    else
        odo_dtheta_b = 0
    end"""
)

# Instrumentar as correções no fim de cada ciclo de controlo.
s += """
    if lin_state == 1 and test_n < 40 then
        test_heading[test_n] = lin_heading_b
        test_correction[test_n] = lin_correction
        test_n = test_n + 1
    end
"""

# Neutralizar todas as atribuições aos motores.
s = re.sub(
    r'(?m)^(\s*motor\.(?:left|right)\.target\s*=).*$',
    r'\1 0',
    s
)

comandos = re.findall(
    r'(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$',
    s
)
assert comandos and all(x.strip() == "0" for x in comandos)

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s, encoding="utf-8")

print("Diagnóstico criado:", dst)
print("Todas as atribuições aos motores são zero.")
