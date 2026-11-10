"""Criar V3.2 a partir da V3.1 validada."""

from pathlib import Path

src = Path("resultados/odometria_embarcada_v31.aesl")
inc = Path("aseba/controlador_angular_v32.inc")
dst = Path("resultados/odometria_embarcada_v32.aesl")

s = src.read_text(encoding="utf-8")
controlador = inc.read_text(encoding="utf-8")

declaracoes = """
# Controlador angular V3.2
var ctl_request = 0
var ctl_mode = 0
var ctl_active_mode = 0
var ctl_abort = 0
var ctl_state = 0
var ctl_ticks = 0
var ctl_angle_b = 0
var ctl_stop_angle_b = 0
var ctl_settle_ticks = 0

"""

marcador = "timer.period[0] = 100"

if s.count(marcador) != 1:
    raise RuntimeError("Temporizador inesperado")

if "var ctl_state" in s:
    raise RuntimeError("Controlador já integrado")

s = s.replace(marcador, declaracoes + marcador, 1)
s = s.rstrip() + "\n\n" + controlador

if dst.exists():
    raise FileExistsError(dst)

dst.write_text(s, encoding="utf-8")

print("Criado:", dst)
print("V3.1 preservada.")
print("Modo inicial: simulacao.")
print("Pedido de movimento inicial: desativado.")
