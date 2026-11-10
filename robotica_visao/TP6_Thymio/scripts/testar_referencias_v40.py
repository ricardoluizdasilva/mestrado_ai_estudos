
"""TP6 - Exercicio 9: validar referencias configuraveis V4.0."""

import json
import re
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("aseba/correcao_pose_v40.aesl")
SAIDA = Path("resultados/ex9_referencias_v40.json")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

# Coordenadas coarse: 0,1 mm.
# Residuos: 0,01 mm.
# Angulo Aseba: 90 graus = 16384.
TESTES = [
    ("A - origem", (0, 0, 0, 0, 0, 0)),
    ("B - positiva", (1000, 0, 500, 0, 16384, 0)),
    ("C - negativa", (-500, 0, -1000, 0, -16384, 0)),

    # D: X = 10,123 cm; Y = -5,067 cm; theta = 270 graus
    ("D - residuos", (1012, 3, -506, -7, -16384, 1)),

    # E: X = 0,001 cm; Y = -0,001 cm; theta = 360 graus
    ("E - precisao", (0, 1, 0, -1, 0, 1)),
]

CAMPOS_REF = (
    "corr_ref_x_coarse",
    "corr_ref_x_rem",
    "corr_ref_y_coarse",
    "corr_ref_y_rem",
    "corr_ref_theta_b",
    "corr_ref_turns",
)

CAMPOS_POSE = (
    "odo_x_coarse",
    "odo_x_rem",
    "odo_y_coarse",
    "odo_y_rem",
    "odo_theta_b",
    "odo_turns",
)


def verificar_resultado(resultado, operacao):
    if resultado is not None:
        raise RuntimeError(f"{operacao}: {resultado}")


def ler(node, campos):
    return tuple(
        int(getattr(node.v, nome))
        for nome in campos
    )


async def aguardar(client, condicao, mensagem, segundos=3.0):
    limite = time.monotonic() + segundos

    while time.monotonic() < limite:
        await client.sleep(0.1)
        if condicao():
            return

    raise TimeoutError(mensagem)


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")

    # Verificar que o programa nao comanda os motores.
    comandos = re.findall(
        r"(?m)^\s*motor\.(?:left|right)\.target\s*=\s*(.+)$",
        codigo,
    )
    if any(c.strip() != "0" for c in comandos):
        raise RuntimeError("Comando motor nao permitido")

    resultados = []

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def testar():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            execucao_solicitada = False

            async def parar():
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

            try:
                await parar()

                verificar_resultado(
                    await node.compile(codigo), "Compilacao"
                )

                await node.watch(variables=True)

                execucao_solicitada = True
                verificar_resultado(
                    await node.run(), "Execucao"
                )

                await node.wait_for_variables(
                    set(CAMPOS_REF)
                    | set(CAMPOS_POSE)
                    | {
                        "corr_request", "corr_applied",
                        "motor.left.target",
                        "motor.right.target",
                    }
                )

                print("=== TESTES V4.0 ===", flush=True)

                for nome, referencia in TESTES:
                    valores = dict(zip(CAMPOS_REF, referencia))

                    # Configurar a referencia antes de pedir correcao.
                    verificar_resultado(
                        await node.set_variables({
                            chave: [valor]
                            for chave, valor in valores.items()
                        }),
                        "Configuracao da referencia"
                    )

                    await aguardar(
                        client,
                        lambda: ler(node, CAMPOS_REF) == referencia,
                        f"Referencia nao confirmada: {nome}"
                    )

                    anterior = int(node.v.corr_applied)

                    verificar_resultado(
                        await node.set_variables({
                            "corr_request": [1]
                        }),
                        "Pedido de correcao"
                    )

                    await aguardar(
                        client,
                        lambda: (
                            int(node.v.corr_applied) == anterior + 1
                            and int(node.v.corr_request) == 0
                            and ler(node, CAMPOS_POSE) == referencia
                        ),
                        f"Correcao nao confirmada: {nome}"
                    )

                    pose = ler(node, CAMPOS_POSE)

                    motores = (
                        int(node.v.motor.left.target),
                        int(node.v.motor.right.target),
                    )
                    if motores != (0, 0):
                        raise RuntimeError("Motores nao estao parados")

                    xc, xr, yc, yr, theta_b, turns = pose

                    resultado = {
                        "teste": nome,
                        "x_cm": (10 * xc + xr) / 1000,
                        "y_cm": (10 * yc + yr) / 1000,
                        "theta_graus": (
                            theta_b + 65536 * turns
                        ) * 180 / 32768,
                        "aplicacoes": int(node.v.corr_applied),
                        "motores": list(motores),
                    }

                    resultados.append(resultado)
                    print(resultado, flush=True)

                assert len(resultados) == len(TESTES)

                SAIDA.parent.mkdir(
                    parents=True, exist_ok=True
                )
                SAIDA.write_text(
                    json.dumps(
                        resultados,
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                print("\nREFERENCIAS V4.0: OK", flush=True)
                print("Resultados:", SAIDA, flush=True)

            finally:
                try:
                    await parar()
                    if execucao_solicitada:
                        await node.stop()
                finally:
                    try:
                        await node.watch(variables=False)
                    finally:
                        await node.unlock()
                        print(
                            "Programa parado. No desbloqueado.",
                            flush=True,
                        )

        client.run_async_program(testar)


if __name__ == "__main__":
    main()
