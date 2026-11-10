from pathlib import Path

src = Path("resultados/odometria_embarcada_v31.aesl")
dst = Path("aseba/teste_angular_integrado_v31.aesl")

s = src.read_text(encoding="utf-8")

def trocar(antigo, novo):
    global s
    assert s.count(antigo) == 1, antigo
    s = s.replace(antigo, novo, 1)

trocar(
    "timer.period[0] = 100",
    """var test_theta_log[8]
var test_mid_log[8]
var test_turns_log[8]

timer.period[0] = 100"""
)

trocar(
    "call math.muldiv(odo_dl_01mm, motor.left.speed, odo_kd_milli, 100)",
    "odo_dl_01mm = 0"
)
trocar(
    "call math.muldiv(odo_dr_01mm, motor.right.speed, odo_kd_milli, 100)",
    "odo_dr_01mm = 0"
)
trocar(
    "call math.muldiv(odo_dtheta_b, odo_diff_01mm, 10430, 935)",
    """if odo_ticks <= 4 then
        odo_dtheta_b = 16384
    elseif odo_ticks <= 8 then
        odo_dtheta_b = -16384
    else
        odo_dtheta_b = 0
    end"""
)

s += """
    if odo_ticks <= 8 then
        test_theta_log[odo_ticks - 1] = odo_theta_b
        test_mid_log[odo_ticks - 1] = odo_theta_mid_b
        test_turns_log[odo_ticks - 1] = odo_turns
    end
"""

assert "motor.left.target" not in s
assert "motor.right.target" not in s

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s, encoding="utf-8")
print("Programa de diagnóstico criado:", dst)
print("Sem comandos de movimento.")
