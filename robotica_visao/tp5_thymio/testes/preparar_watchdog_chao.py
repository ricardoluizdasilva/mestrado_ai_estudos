from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
ORIGEM = BASE / "src" / "aseba" / "watchdog_motores.asm"
DESTINO = BASE / "src" / "aseba" / "watchdog_chao.asm"

LIMITE_ORIGINAL = 20
LIMITE_CHAO = 10


def main():
    print("=== PREPARAR WATCHDOG PARA TESTE NO CHAO ===")

    if not ORIGEM.is_file():
        raise FileNotFoundError(ORIGEM)

    if DESTINO.exists():
        raise FileExistsError(f"O ficheiro ja existe: {DESTINO}")

    codigo = ORIGEM.read_text(encoding="utf-8")

    # Verificar as secoes de limitacao dos dois motores
    marcadores = (
        "limitar_esquerdo:",
        "limitar_direito:",
        "diagnostico:",
    )

    for marcador in marcadores:
        if marcador not in codigo:
            raise RuntimeError(f"Marcador em falta: {marcador}")

    # Apenas alterar a secao dos limitadores
    inicio = codigo.index("limitar_esquerdo:")
    fim = codigo.index("diagnostico:", inicio)

    antes = codigo[:inicio]
    secao = codigo[inicio:fim]
    depois = codigo[fim:]

    # Procurar apenas instrucoes push.s completas
    padrao_pos = r"(?m)^(\s*push\.s\s+)20(\s*(?:;.*)?)$"
    padrao_neg = r"(?m)^(\s*push\.s\s+)-20(\s*(?:;.*)?)$"

    positivos = len(re.findall(padrao_pos, secao))
    negativos = len(re.findall(padrao_neg, secao))

    print("Limites positivos encontrados:", positivos)
    print("Limites negativos encontrados:", negativos)

    if positivos != 4 or negativos != 4:
        raise RuntimeError(
            "Estrutura diferente da esperada. Nenhum ficheiro foi criado."
        )

    secao = re.sub(
        padrao_pos,
        lambda m: f"{m.group(1)}10{m.group(2)}",
        secao,
    )

    secao = re.sub(
        padrao_neg,
        lambda m: f"{m.group(1)}-10{m.group(2)}",
        secao,
    )

    resultado = antes + secao + depois

    DESTINO.write_text(resultado, encoding="utf-8")

    print("Ficheiro criado:", DESTINO)
    print("Limites configurados: -10 a +10")
    print("Watchdog original preservado.")
    print("PREPARACAO CONCLUIDA")


if __name__ == "__main__":
    main()
