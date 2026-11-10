"""TP6 - Testes offline da representação angular Aseba."""

import math

ESCALA = 32768 / 180


def normalizar_graus(angulo):
    return (angulo + 180) % 360 - 180


def codificar_aseba(graus):
    normalizado = normalizar_graus(graus)
    return round(normalizado * ESCALA)


def descodificar_aseba(valor):
    return valor * 180 / 32768


def erro_circular(a, b):
    return normalizar_graus(a - b)


print("=== TP6 - TESTE ANGULAR ===")

angulos = [
    0, 90, 179, 180, 181,
    270, 359, 360, 450,
    -90, -179, -180, -181, -360
]

for angulo in angulos:
    codificado = codificar_aseba(angulo)
    recuperado = descodificar_aseba(codificado)
    erro = erro_circular(recuperado, angulo)

    assert -32768 <= codificado <= 32767
    assert abs(erro) <= 180 / 32768

    print(
        f"{angulo:+5d}° -> "
        f"{codificado:+7d} -> "
        f"{recuperado:+9.4f}°"
    )

print("\n=== QUATRO CURVAS DE 90° ===")

acumulado = 0

for curva in range(1, 5):
    acumulado += 90
    normalizado = normalizar_graus(acumulado)

    print(
        f"Curva {curva}: "
        f"acumulado={acumulado}°, "
        f"normalizado={normalizado}°"
    )

assert acumulado == 360
assert normalizar_graus(acumulado) == 0

print("\nTestes matemáticos: OK")
