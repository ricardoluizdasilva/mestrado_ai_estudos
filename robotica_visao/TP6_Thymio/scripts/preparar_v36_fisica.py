from pathlib import Path

origem = Path("resultados/odometria_embarcada_v31.aesl")
modulo = Path("aseba/controlador_sequencia_v36.inc")
destino = Path("resultados/odometria_embarcada_v36_fisica.aesl")

codigo = origem.read_text(encoding="utf-8")
controlador = modulo.read_text(encoding="utf-8")

declaracoes = """
var seq_request = 0
var seq_arm = 0
var seq_abort = 0
var seq_state = 0
var seq_fault = 0
var seq_ticks = 0
var seq_line_ticks = 0
var seq_turn_ticks = 0
var seq_progress = 0
var seq_heading_b = 0
var seq_correction = 0
var seq_angle_b = 0
var seq_wait = 0
var seq_last_state = 0
var seq_history[6]
var seq_history_n = 0
"""

marcador = "timer.period[0] = 100"
assert codigo.count(marcador) == 1

codigo = codigo.replace(
    marcador,
    declaracoes + "\n" + marcador,
    1
)

codigo = codigo.rstrip() + "\n\n" + controlador

if destino.exists():
    raise FileExistsError(destino)

destino.write_text(codigo, encoding="utf-8")

print("V3.6 física criada:", destino)
print("Arranque desativado por defeito.")
print("Programa ainda não carregado.")
