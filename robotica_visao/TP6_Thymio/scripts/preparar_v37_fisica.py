"""TP6 - Preparar V3.7 física para dois lados."""

from pathlib import Path

origem = Path(
    "resultados/odometria_embarcada_v361_fisica.aesl"
)
destino = Path(
    "resultados/odometria_embarcada_v37_fisica_2lados.aesl"
)

codigo = origem.read_text(encoding="utf-8")


def substituir(antigo, novo):
    global codigo
    if codigo.count(antigo) != 1:
        raise RuntimeError(f"Marcador inesperado: {antigo!r}")
    codigo = codigo.replace(antigo, novo, 1)


# Contador de lados.
substituir(
    "var seq_state = 0",
    """var seq_state = 0
var seq_side = 0
var seq_goal_sides = 2"""
)

# Histórico de transições maior.
substituir("var seq_history[6]", "var seq_history[20]")
substituir("seq_history_n < 6", "seq_history_n < 20")

# Reiniciar o contador de lados numa nova sequência.
substituir(
    "        seq_ticks = 0",
    """        seq_ticks = 0
        seq_side = 0"""
)

# Dar tempo suficiente a duas sequências.
substituir(
    "seq_ticks >= 160",
    "seq_ticks >= 300"
)

# Após cada rotação, iniciar o lado seguinte
# ou concluir a sequência.
substituir(
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

# Garantias estruturais.
assert "seq_progress = seq_progress + (odo_dl_01mm + odo_dr_01mm) * 5" in codigo
assert "seq_angle_b = seq_angle_b + odo_dtheta_b" in codigo
assert "seq_fault = 1" in codigo
assert "seq_abort == 1" in codigo

if destino.exists():
    raise FileExistsError(destino)

destino.write_text(codigo, encoding="utf-8")

print("V3.7 física criada:", destino)
print("Lados configurados: 2")
print("Odometria real preservada.")
print("Proteções da V3.6.1 preservadas.")
print("Programa ainda não carregado nem executado.")
