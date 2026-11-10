"""Gerar diagnóstico V3.7 sem movimento físico."""

from pathlib import Path
import re

src = Path(
    "resultados/odometria_embarcada_v37_fisica_2lados.aesl"
)
dst = Path("aseba/diagnostico_v37_2lados.aesl")

s = src.read_text(encoding="utf-8")


def trocar(antigo, novo):
    global s
    if s.count(antigo) != 1:
        raise RuntimeError(f"Marcador inesperado: {antigo}")
    s = s.replace(antigo, novo, 1)


# Substituir as leituras das rodas por incrementos simulados.
trocar(
    "call math.muldiv(odo_dl_01mm, motor.left.speed, odo_kd_milli, 100)",
    """if seq_state == 1 then
        odo_dl_01mm = 25
    else
        odo_dl_01mm = 0
    end"""
)

trocar(
    "call math.muldiv(odo_dr_01mm, motor.right.speed, odo_kd_milli, 100)",
    """if seq_state == 1 then
        odo_dr_01mm = 25
    else
        odo_dr_01mm = 0
    end"""
)

# Simular a rotação na odometria global e no controlador.
trocar(
    "call math.muldiv(odo_dtheta_b, odo_diff_01mm, 10430, 935)",
    """if seq_state == 3 then
        odo_dtheta_b = 512
    else
        odo_dtheta_b = 0
    end"""
)

# Neutralizar todos os comandos físicos dos motores.
s = re.sub(
    r"(?m)^(\s*motor\.(?:left|right)\.target\s*=).*$",
    r"\1 0",
    s,
)

comandos = re.findall(
    r"(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$",
    s,
)

if not comandos or any(c.strip() != "0" for c in comandos):
    raise RuntimeError("Comando motor não seguro")

if dst.exists():
    raise FileExistsError(dst)

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s, encoding="utf-8")

print("Diagnóstico criado:", dst)
print("Deslocamento simulado: 0,25 cm/ciclo")
print("Rotação simulada: 2,8125 graus/ciclo")
print("Motores: todos os comandos neutralizados")
