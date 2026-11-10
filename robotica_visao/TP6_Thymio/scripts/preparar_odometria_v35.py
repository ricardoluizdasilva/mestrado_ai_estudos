"""TP6 - V3.5: controlo linear com correcao de orientacao."""

from pathlib import Path

src = Path("resultados/odometria_embarcada_v34_ajustada.aesl")
dst = Path("resultados/odometria_embarcada_v35.aesl")

s = src.read_text(encoding="utf-8")

def trocar(antigo, novo):
    global s
    if s.count(antigo) != 1:
        raise RuntimeError(f"Marcador invalido: {antigo!r}")
    s = s.replace(antigo, novo, 1)

trocar(
    "var lin_settle_ticks = 0",
    """var lin_settle_ticks = 0
var lin_heading_b = 0
var lin_correction = 0"""
)

trocar(
    "        lin_progress_001mm = 0",
    """        lin_progress_001mm = 0
        lin_heading_b = 0
        lin_correction = 0"""
)

trocar(
    """        lin_progress_001mm = lin_progress_001mm + lin_increment_001mm""",
    """        lin_progress_001mm = lin_progress_001mm + lin_increment_001mm

        # Erro angular relativo ao inicio do segmento.
        lin_heading_b = lin_heading_b + odo_dtheta_b

        # 182 unidades Aseba equivalem a cerca de 1 grau.
        # Correcao de aproximadamente 1 unidade por grau.
        lin_correction = (0 - lin_heading_b) / 182

        if lin_correction > 8 then
            lin_correction = 8
        end
        if lin_correction < -8 then
            lin_correction = -8
        end"""
)

for velocidade in (40, 80):
    trocar(
        f"motor.left.target = {velocidade}",
        f"motor.left.target = {velocidade} - lin_correction"
    )
    trocar(
        f"motor.right.target = {velocidade}",
        f"motor.right.target = {velocidade} + lin_correction"
    )

if dst.exists():
    raise FileExistsError(dst)

dst.write_text(s, encoding="utf-8")

print("V3.5 criada:", dst)
print("Correcao proporcional limitada a +/-8.")
print("Limiar linear original preservado.")
print("Programa nao carregado nem executado.")
