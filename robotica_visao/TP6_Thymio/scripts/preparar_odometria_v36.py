"""TP6 - Gerar V3.6 exclusivamente para simulação."""

from pathlib import Path
import re

src = Path("resultados/odometria_embarcada_v35.aesl")
dst = Path("resultados/odometria_embarcada_v36_sim.aesl")

codigo = src.read_text(encoding="utf-8")

marcador = "# TP6 - Controlador linear embarcado V3.4"

if codigo.count(marcador) != 1:
    raise RuntimeError("Bloco linear original não identificado")

# Preservar a odometria e retirar o controlador V3.5 antigo.
codigo = codigo.split(marcador, 1)[0].rstrip()

declaracoes = """
# V3.6 - Sequencia de simulacao
var seq_request = 0
var seq_abort = 0
var seq_state = 0
var seq_total_ticks = 0
var seq_line_ticks = 0
var seq_turn_ticks = 0
var seq_progress = 0
var seq_angle = 0
var seq_global_angle = 0
var seq_stop_distance = 0
var seq_stop_angle = 0
var seq_wait = 0
var seq_virtual_left = 0
var seq_virtual_right = 0
var seq_history[5]
var seq_history_n = 0
var seq_last_logged = 0
"""

marcador_timer = "timer.period[0] = 100"

if codigo.count(marcador_timer) != 1:
    raise RuntimeError("Temporizador não identificado")

codigo = codigo.replace(
    marcador_timer,
    declaracoes + "\n" + marcador_timer,
    1,
)

controlador = """
# V3.6 - Maquina de estados, apenas simulacao
# Nenhum comando de movimento diferente de zero.

motor.left.target = 0
motor.right.target = 0

if seq_abort == 1 then
    seq_state = 6
end

if seq_state == 0 then
    if seq_request == 1 then
        seq_request = 0
        seq_total_ticks = 0
        seq_line_ticks = 0
        seq_turn_ticks = 0
        seq_progress = 0
        seq_angle = 0
        seq_global_angle = 0
        seq_stop_distance = 0
        seq_stop_angle = 0
        seq_wait = 0
        seq_history_n = 0
        seq_last_logged = 0
        seq_state = 1
    end

elseif seq_state == 1 then
    # Simular avancar 0,25 cm a cada ciclo.
    seq_total_ticks = seq_total_ticks + 1
    seq_line_ticks = seq_line_ticks + 1
    seq_progress = seq_progress + 250

    if seq_progress >= 7000 then
        seq_virtual_left = 40
        seq_virtual_right = 40
    else
        seq_virtual_left = 80
        seq_virtual_right = 80
    end

    if seq_line_ticks >= 60 then
        seq_state = 6
    elseif seq_progress >= 9700 then
        seq_stop_distance = seq_progress
        seq_wait = 0
        seq_state = 2
    end

elseif seq_state == 2 then
    seq_total_ticks = seq_total_ticks + 1
    seq_wait = seq_wait + 1
    seq_virtual_left = 0
    seq_virtual_right = 0

    if seq_wait >= 5 then
        seq_wait = 0
        seq_angle = 0
        seq_state = 3
    end

elseif seq_state == 3 then
    # Simular incremento de 2,8125 graus por ciclo.
    seq_total_ticks = seq_total_ticks + 1
    seq_turn_ticks = seq_turn_ticks + 1
    seq_angle = seq_angle + 512
    seq_global_angle = seq_global_angle + 512

    if seq_angle >= 11833 then
        seq_virtual_left = -30
        seq_virtual_right = 30
    else
        seq_virtual_left = -60
        seq_virtual_right = 60
    end

    if seq_turn_ticks >= 95 then
        seq_state = 6
    elseif seq_angle >= 16111 then
        seq_stop_angle = seq_angle
        seq_wait = 0
        seq_state = 4
    end

elseif seq_state == 4 then
    seq_total_ticks = seq_total_ticks + 1
    seq_wait = seq_wait + 1
    seq_virtual_left = 0
    seq_virtual_right = 0

    if seq_wait >= 5 then
        seq_state = 5
    end
end

if seq_total_ticks >= 150 then
    if seq_state != 5 then
        seq_state = 6
    end
end

if seq_state == 5 or seq_state == 6 then
    seq_virtual_left = 0
    seq_virtual_right = 0
end

# Registar transicoes uma unica vez.
if seq_state != seq_last_logged then
    if seq_history_n < 5 then
        seq_history[seq_history_n] = seq_state
        seq_history_n = seq_history_n + 1
    end
    seq_last_logged = seq_state
end
"""

codigo = codigo + "\n\n" + controlador

# Garantir ausência de comandos físicos diferentes de zero.
comandos = re.findall(
    r'(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$',
    codigo,
)

if len(comandos) != 2 or any(
    comando.strip() != "0" for comando in comandos
):
    raise RuntimeError("Comandos motores não seguros")

if dst.exists():
    raise FileExistsError(dst)

dst.write_text(codigo, encoding="utf-8")

print("Criado:", dst)
print("Controlador V3.5 original preservado.")
print("Simulacao: 10 cm + 90 graus.")
print("Comandos motores: sempre zero.")
