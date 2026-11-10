"""TP6 - V3.7: duas sequências simuladas, sem movimento."""

from pathlib import Path
import re

origem = Path("resultados/odometria_embarcada_v361_fisica.aesl")
destino = Path("resultados/odometria_embarcada_v37_sim.aesl")

s = origem.read_text(encoding="utf-8")


def trocar(antigo, novo):
    global s
    if s.count(antigo) != 1:
        raise RuntimeError(f"Marcador inesperado: {antigo!r}")
    s = s.replace(antigo, novo, 1)


# Contador e número de lados do ensaio.
trocar(
    "var seq_state = 0",
    "var seq_state = 0\nvar seq_side = 0\nvar seq_goal_sides = 2"
)

# Aumentar a capacidade do histórico.
trocar("var seq_history[6]", "var seq_history[20]")
trocar("seq_history_n < 6", "seq_history_n < 20")

# Reiniciar o contador no início da sequência.
trocar(
    "        seq_ticks = 0",
    "        seq_ticks = 0\n        seq_side = 0"
)

# Simular os incrementos de distância e rotação.
trocar(
    "seq_progress = seq_progress + (odo_dl_01mm + odo_dr_01mm) * 5",
    "seq_progress = seq_progress + 250"
)
trocar(
    "seq_angle_b = seq_angle_b + odo_dtheta_b",
    "seq_angle_b = seq_angle_b + 512"
)

# Aumentar o limite global apenas nesta simulação.
trocar("seq_ticks >= 160", "seq_ticks >= 380")

# Após cada curva, avançar para o próximo lado ou concluir.
trocar(
    """    if seq_wait >= 8 then
        seq_state = 5
    end""",
    """    if seq_wait >= 8 then
        seq_side = seq_side + 1

        if seq_side >= seq_goal_sides then
            seq_state = 5
        else
            seq_line_ticks = 0
            seq_turn_ticks = 0
            seq_progress = 0
            seq_heading_b = 0
            seq_correction = 0
            seq_angle_b = 0
            seq_wait = 0
            seq_state = 1
        end
    end"""
)

# Neutralizar TODOS os comandos dos motores.
s = re.sub(
    r"(?m)^(\s*motor\.(?:left|right)\.target\s*=).*$",
    r"\1 0",
    s
)

comandos = re.findall(
    r"(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$",
    s
)

if not comandos or any(c.strip() != "0" for c in comandos):
    raise RuntimeError("Comando de movimento encontrado")

if destino.exists():
    raise FileExistsError(destino)

destino.write_text(s, encoding="utf-8")

print("V3.7 simulada criada:", destino)
print("Número de lados:", 2)
print("Comandos motores: todos zero")
print("V3.6.1 preservada")
