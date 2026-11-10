from pathlib import Path

src = Path("resultados/odometria_embarcada_v32_teste2.aesl")
dst = Path("resultados/odometria_embarcada_v33.aesl")

s = src.read_text(encoding="utf-8")

def trocar(antigo, novo):
    global s
    if s.count(antigo) != 1:
        raise RuntimeError(f"Marcador inesperado: {antigo}")
    s = s.replace(antigo, novo, 1)

# Controlar o ângulo relativo.
trocar(
    "var ctl_settle_ticks = 0",
    "var ctl_settle_ticks = 0\nvar ctl_skip_delta = 0"
)

trocar(
    "        ctl_angle_b = 0",
    "        ctl_angle_b = 0\n        ctl_skip_delta = 1"
)

trocar(
    "        ctl_angle_b = odo_theta_b",
    """        if ctl_skip_delta == 1 then
            ctl_skip_delta = 0
        else
            ctl_angle_b = ctl_angle_b + odo_dtheta_b
        end"""
)

# Parâmetros da rotação de 90 graus.
trocar("ctl_ticks >= 50", "ctl_ticks >= 100")
trocar("ctl_angle_b >= 7919", "ctl_angle_b >= 16111")
trocar("ctl_angle_b >= 3641", "ctl_angle_b >= 11833")

dst.write_text(s, encoding="utf-8")

print("V3.3 criada:", dst)
print("Alvo: 90 graus")
print("Desaceleracao: 65 graus")
print("Paragem: 88,5 graus")
print("Limite: 100 ciclos")
