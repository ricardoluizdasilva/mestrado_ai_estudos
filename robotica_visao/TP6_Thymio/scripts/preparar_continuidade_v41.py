
"""TP6 - Exercicio 9: preparar V4.1 para testes de continuidade."""

from pathlib import Path

origem = Path("aseba/correcao_pose_v40.aesl")
destino = Path("aseba/correcao_pose_v41.aesl")

codigo = origem.read_text(encoding="utf-8")

# Declaracoes de diagnostico, antes do temporizador.
declaracoes = """var sim_mode = 0
var sim_request = 0
var sim_dl_01mm = 0
var sim_dr_01mm = 0
var sim_applied = 0

"""

marcador = "timer.period[0] = 100"

if codigo.count(marcador) != 1:
    raise RuntimeError("Temporizador nao encontrado")

codigo = codigo.replace(
    marcador, declaracoes + marcador, 1
)

# Substituir apenas a leitura dos incrementos das rodas.
antigo = """    call math.muldiv(odo_dl_01mm, motor.left.speed, odo_kd_milli, 100)
    call math.muldiv(odo_dr_01mm, motor.right.speed, odo_kd_milli, 100)"""

novo = """    if sim_mode == 1 then
        # Sem pedido: nenhum deslocamento simulado
        odo_dl_01mm = 0
        odo_dr_01mm = 0

        if sim_request == 1 then
            odo_dl_01mm = sim_dl_01mm
            odo_dr_01mm = sim_dr_01mm
            sim_request = 0
            sim_applied = sim_applied + 1
        end
    else
        call math.muldiv(odo_dl_01mm, motor.left.speed, odo_kd_milli, 100)
        call math.muldiv(odo_dr_01mm, motor.right.speed, odo_kd_milli, 100)
    end"""

if codigo.count(antigo) != 1:
    raise RuntimeError("Leitura das rodas nao encontrada")

codigo = codigo.replace(antigo, novo, 1)

# Mover snapshot para o final do evento, depois da correcao.
snapshot = """    # Fotografia da pose e das velocidades após cada ciclo
    odo_snapshot = [
        odo_ticks,
        odo_x_01mm,
        odo_y_01mm,
        odo_theta_b,
        motor.left.speed,
        motor.right.speed
    ]"""

if codigo.count(snapshot) != 1:
    raise RuntimeError("Bloco snapshot nao encontrado")

codigo = codigo.replace(snapshot, "", 1)
codigo = codigo.rstrip() + "\n\n" + snapshot + "\n"

if destino.exists():
    raise FileExistsError(
        f"{destino} ja existe. A versao anterior foi preservada."
    )

destino.write_text(codigo, encoding="utf-8")

print("Criado:", destino)
print("Modo de simulacao por incremento unico.")
print("Snapshot atualizado apos a correcao.")
print("V4.0 preservada.")
