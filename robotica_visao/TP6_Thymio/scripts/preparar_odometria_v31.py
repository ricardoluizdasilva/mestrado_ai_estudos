"""TP6: integrar normalização angular na odometria V3."""

from pathlib import Path

origem = Path("resultados/odometria_embarcada_v3.aesl")
destino = Path("resultados/odometria_embarcada_v31.aesl")

codigo = origem.read_text(encoding="utf-8")


def substituir(antigo, novo):
    global codigo
    if codigo.count(antigo) != 1:
        raise RuntimeError(f"Marcador inesperado: {antigo}")
    codigo = codigo.replace(antigo, novo, 1)


substituir(
    "timer.period[0] = 100",
    """var odo_half_b = 0
var odo_turns = 0

timer.period[0] = 100"""
)

# Calcular o ângulo intermédio sem overflow de 16 bits.
substituir(
    "    odo_theta_mid_b = odo_theta_b + odo_dtheta_b / 2",
    """    odo_half_b = odo_dtheta_b / 2

    if odo_half_b > 0 then
        if odo_theta_b > 32767 - odo_half_b then
            odo_theta_mid_b = odo_theta_b - 16384
            odo_theta_mid_b = odo_theta_mid_b - 16384
            odo_theta_mid_b = odo_theta_mid_b + odo_half_b
            odo_theta_mid_b = odo_theta_mid_b - 16384
            odo_theta_mid_b = odo_theta_mid_b - 16384
        else
            odo_theta_mid_b = odo_theta_b + odo_half_b
        end
    else
        if odo_theta_b < -32768 - odo_half_b then
            odo_theta_mid_b = odo_theta_b + 16384
            odo_theta_mid_b = odo_theta_mid_b + 16384
            odo_theta_mid_b = odo_theta_mid_b + odo_half_b
            odo_theta_mid_b = odo_theta_mid_b + 16384
            odo_theta_mid_b = odo_theta_mid_b + 16384
        else
            odo_theta_mid_b = odo_theta_b + odo_half_b
        end
    end"""
)

# Atualizar orientação normalizada e contador de voltas.
substituir(
    "    odo_theta_b = odo_theta_b + odo_dtheta_b",
    """    if odo_dtheta_b > 0 then
        if odo_theta_b > 32767 - odo_dtheta_b then
            odo_theta_b = odo_theta_b - 16384
            odo_theta_b = odo_theta_b - 16384
            odo_theta_b = odo_theta_b + odo_dtheta_b
            odo_theta_b = odo_theta_b - 16384
            odo_theta_b = odo_theta_b - 16384
            odo_turns = odo_turns + 1
        else
            odo_theta_b = odo_theta_b + odo_dtheta_b
        end
    else
        if odo_theta_b < -32768 - odo_dtheta_b then
            odo_theta_b = odo_theta_b + 16384
            odo_theta_b = odo_theta_b + 16384
            odo_theta_b = odo_theta_b + odo_dtheta_b
            odo_theta_b = odo_theta_b + 16384
            odo_theta_b = odo_theta_b + 16384
            odo_turns = odo_turns - 1
        else
            odo_theta_b = odo_theta_b + odo_dtheta_b
        end
    end"""
)

destino.write_text(codigo, encoding="utf-8")

print("=== ODOMETRIA V3.1 ===")
print("Ficheiro:", destino)
print("Normalização angular: integrada")
print("Ângulo intermédio: protegido")
print("Contador de voltas: integrado")
print("V3 original: preservada")
