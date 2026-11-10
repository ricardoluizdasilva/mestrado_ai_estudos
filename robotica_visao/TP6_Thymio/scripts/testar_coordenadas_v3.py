"""TP6 - Testar coordenadas segmentadas sem hardware."""

import math


def dividir_truncado(valor, divisor):
    return math.trunc(valor / divisor)


def atualizar(coarse, rem, incremento):
    total = rem + incremento
    carry = dividir_truncado(total, 10)

    coarse += carry
    rem = total - carry * 10

    assert -9 <= rem <= 9
    assert -32768 <= coarse <= 32767

    return coarse, rem


def testar(nome, incrementos):
    coarse = 0
    rem = 0
    referencia = 0

    for incremento in incrementos:
        coarse, rem = atualizar(coarse, rem, incremento)
        referencia += incremento

        reconstruido = 10 * coarse + rem
        assert reconstruido == referencia

    print(
        f"{nome:25s}"
        f" posição={referencia / 1000:+.4f} cm"
        f" coarse={coarse:+d}, residual={rem:+d}"
    )


print("=== TESTES OFFLINE V3 ===")

testar("Incrementos positivos", [7] * 100)
testar("Incrementos negativos", [-7] * 100)
testar("Mudança de direção", [13] * 50 + [-17] * 50)
testar("Cruzamento do zero", [9] * 30 + [-11] * 40)
testar("Acima do limite V2", [100] * 400)
testar("Abaixo do limite V2", [-100] * 400)

print("Todos os testes de representação: OK")
