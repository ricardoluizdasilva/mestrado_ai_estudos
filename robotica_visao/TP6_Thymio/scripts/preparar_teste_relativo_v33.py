from pathlib import Path
import re

src = Path("resultados/odometria_embarcada_v33.aesl")
dst = Path("aseba/teste_relativo_v33.aesl")
s = src.read_text(encoding="utf-8")

def trocar(a, b):
    global s
    if s.count(a) != 1:
        raise RuntimeError(f"Marcador inesperado: {a}")
    s = s.replace(a, b, 1)

trocar(
    "call math.muldiv(odo_dtheta_b, odo_diff_01mm, 10430, 935)",
    """call math.muldiv(odo_dtheta_b, odo_diff_01mm, 10430, 935)
    if ctl_state == 1 and ctl_active_mode == 0 then
        odo_dtheta_b = 512
    end"""
)

trocar(
    "ctl_angle_b = ctl_ticks * 512",
    "ctl_angle_b = ctl_angle_b + odo_dtheta_b"
)

# Só no diagnóstico: permitir novo pedido após conclusão.
s += """
# Rearmar exclusivamente em modo de simulacao
if ctl_state == 3 and ctl_request == 1 and ctl_mode == 0 then
    ctl_state = 0
end
"""

# Segurança: retirar comandos de movimento do programa de diagnóstico.
s = re.sub(
    r"(motor\.(?:left|right)\.target\s*=\s*)-?\d+",
    r"\g<1>0",
    s
)

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s, encoding="utf-8")

print("Criado:", dst)
print("Movimento desativado nesta versão.")
