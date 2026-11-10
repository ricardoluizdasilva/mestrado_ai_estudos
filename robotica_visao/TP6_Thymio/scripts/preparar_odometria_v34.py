"""TP6 - Integrar controlador linear na odometria."""

from pathlib import Path

origem = Path("resultados/odometria_embarcada_v31.aesl")
modulo = Path("aseba/controlador_linear_v34.inc")
destino = Path("resultados/odometria_embarcada_v34.aesl")

codigo = origem.read_text(encoding="utf-8")
controlador = modulo.read_text(encoding="utf-8")

declaracoes = """
# Controlador linear V3.4
var lin_request = 0
var lin_mode = 0
var lin_active_mode = 0
var lin_abort = 0
var lin_state = 0
var lin_ticks = 0
var lin_progress_001mm = 0
var lin_increment_001mm = 0
var lin_stop_001mm = 0
var lin_settle_ticks = 0

"""

marcador = "timer.period[0] = 100"

if codigo.count(marcador) != 1:
    raise RuntimeError("Temporizador inesperado")

if "var lin_state" in codigo:
    raise RuntimeError("Controlador ja integrado")

if destino.exists():
    raise FileExistsError(destino)

codigo = codigo.replace(
    marcador, declaracoes + marcador, 1
)

codigo = codigo.rstrip() + "\n\n" + controlador

destino.write_text(codigo, encoding="utf-8")

print("=== ODOMETRIA V3.4 ===")
print("Criado:", destino)
print("Modo inicial: simulacao")
print("Pedido inicial: desativado")
print("V3.1 preservada")
