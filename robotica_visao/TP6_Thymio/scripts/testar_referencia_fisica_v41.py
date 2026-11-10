
"""TP6 - Exercicio 9: estacao de referencia fisica V4.1.

O robot fica parado. Uma pose de teste e introduzida
deliberadamente e corrigida para uma referencia fisica
alinhada e confirmada pelo operador.
"""

import csv
import json
import time
from datetime import datetime
from pathlib import Path

from tdmclient import ClientAsync

BASE = Path("resultados")
PROGRAMA = Path("aseba/correcao_pose_v41.aesl")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

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

# Valores nas unidades internas Aseba.
POSE_TESTE = (1000, 0, 500, 0, 16384, 0)
REFERENCIA_FISICA = (0, 0, 0, 0, 0, 0)


def valor(node, nome):
    return int(getattr(node.v, nome))


def ler_campos(node, campos):
    return tuple(valor(node, c) for c in campos)


def pose(node):
    xc, xr, yc, yr, theta, turns = ler_campos(
        node, CAMPOS_POSE
    )
    return {
        "x_cm": (10 * xc + xr) / 1000,
        "y_cm": (10 * yc + yr) / 1000,
        "theta_graus": (
            theta + 65536 * turns
        ) * 180 / 32768,
    }


async def aguardar(client, condicao, mensagem):
    limite = time.monotonic() + 5.0

    while time.monotonic() < limite:
        await client.sleep(0.1)
        if condicao():
            return

    raise TimeoutError(mensagem)


async def definir_referencia(node, client, valores):
    await node.set_variables({
        campo: [v]
        for campo, v in zip(CAMPOS_REF, valores)
    })

    await aguardar(
        client,
        lambda: ler_campos(node, CAMPOS_REF) == valores,
        "Referencia nao confirmada pelo TDM",
    )


async def aplicar_correcao(node, client, valores):
    await definir_referencia(node, client, valores)

    anterior = valor(node, "corr_applied")

    await node.set_variables({"corr_request": [1]})

    await aguardar(
        client,
        lambda: (
            valor(node, "corr_applied") == anterior + 1
            and valor(node, "corr_request") == 0
            and ler_campos(node, CAMPOS_POSE) == valores
        ),
        "Correcao de pose nao confirmada",
    )

    return pose(node)


def guardar(registos):
    BASE.mkdir(parents=True, exist_ok=True)

    ficheiro_json = BASE / "ex9_referencia_fisica_v41.json"
    ficheiro_csv = BASE / "ex9_referencia_fisica_v41.csv"

    ficheiro_json.write_text(
        json.dumps(registos, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with ficheiro_csv.open(
        "w", newline="", encoding="utf-8"
    ) as ficheiro:
        escritor = csv.DictWriter(
            ficheiro,
            fieldnames=[
                "instante",
                "etapa",
                "x_cm",
                "y_cm",
                "theta_graus",
                "corr_applied",
            ],
        )
        escritor.writeheader()
        escritor.writerows(registos)

    print("JSON:", ficheiro_json)
    print("CSV:", ficheiro_csv)


def main():
    print("=== TP6 - REFERENCIA FISICA V4.1 ===")
    print("Thymio parado, referencia (0, 0, 0 graus)")
    print("A discrepancia inicial sera artificial.")
    print()
    confirmacao = input(
        "Robot alinhado e seguro? Escreva SIM: "
    ).strip()

    if confirmacao != "SIM":
        print("Teste cancelado.")
        return

    codigo = PROGRAMA.read_text(encoding="utf-8")
    registos = []

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def executar():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            iniciou = False

            async def parar():
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

            try:
                await parar()

                erro = await node.compile(codigo)
                if erro is not None:
                    raise RuntimeError(f"Compilacao: {erro}")

                await node.watch(variables=True)

                iniciou = True
                erro = await node.run()
                if erro is not None:
                    raise RuntimeError(f"Execucao: {erro}")

                await node.wait_for_variables(
                    set(CAMPOS_POSE)
                    | set(CAMPOS_REF)
                    | {
                        "corr_request",
                        "corr_applied",
                        "sim_mode",
                        "motor.left.target",
                        "motor.right.target",
                        "motor.left.speed",
                        "motor.right.speed",
                    }
                )

                # O teste utiliza odometria normal, sem
                # incrementos artificiais das rodas.
                await node.set_variables({
                    "sim_mode": [0],
                    "sim_request": [0],
                })

                await aguardar(
                    client,
                    lambda: valor(node, "sim_mode") == 0,
                    "Modo normal nao confirmado",
                )

                # Verificacao dos comandos e velocidades.
                await client.sleep(0.4)

                comandos = (
                    int(node.v.motor.left.target),
                    int(node.v.motor.right.target),
                )
                velocidades = (
                    int(node.v.motor.left.speed),
                    int(node.v.motor.right.speed),
                )

                if comandos != (0, 0):
                    raise RuntimeError(
                        f"Comandos motores inesperados: {comandos}"
                    )

                if any(abs(v) > 2 for v in velocidades):
                    raise RuntimeError(
                        f"Rodas em movimento: {velocidades}"
                    )

                print("\nMotores parados.", flush=True)

                # 1. Introduzir deliberadamente uma pose
                # incorreta, para demonstrar a correcao.
                pose_antes = await aplicar_correcao(
                    node, client, POSE_TESTE
                )

                registos.append({
                    "instante": datetime.now().isoformat(),
                    "etapa": "pose_teste_artificial",
                    **pose_antes,
                    "corr_applied": valor(node, "corr_applied"),
                })

                print(
                    "Pose artificial:", pose_antes,
                    flush=True,
                )

                # 2. Aplicar a referencia fisica conhecida.
                pose_depois = await aplicar_correcao(
                    node, client, REFERENCIA_FISICA
                )

                registos.append({
                    "instante": datetime.now().isoformat(),
                    "etapa": "referencia_fisica_aplicada",
                    **pose_depois,
                    "corr_applied": valor(node, "corr_applied"),
                })

                print(
                    "Pose corrigida:", pose_depois,
                    flush=True,
                )

                assert pose_depois == {
                    "x_cm": 0.0,
                    "y_cm": 0.0,
                    "theta_graus": 0.0,
                }

                await client.sleep(0.4)

                if ler_campos(
                    node, CAMPOS_POSE
                ) != REFERENCIA_FISICA:
                    raise RuntimeError(
                        "Pose corrigida nao permaneceu estavel"
                    )

                comandos = (
                    int(node.v.motor.left.target),
                    int(node.v.motor.right.target),
                )

                if comandos != (0, 0):
                    raise RuntimeError(
                        "Comandos motores nao nulos"
                    )

                guardar(registos)

                print(
                    "\nREFERENCIA FISICA V4.1: OK",
                    flush=True,
                )

            finally:
                try:
                    await parar()
                    if iniciou:
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

        client.run_async_program(executar)


if __name__ == "__main__":
    main()
