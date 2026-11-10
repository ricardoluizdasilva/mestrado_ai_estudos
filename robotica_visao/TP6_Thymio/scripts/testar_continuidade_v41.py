
"""TP6 - Exercicio 9: continuidade da odometria V4.1.

Testes com incrementos de rodas simulados.
Nao comanda movimento fisico.
"""

import json
import math
import time
from pathlib import Path

from tdmclient import ClientAsync

PROGRAMA = Path("aseba/correcao_pose_v41.aesl")
SAIDA = Path("resultados/ex9_continuidade_v41.json")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

CAMPOS_POSE = (
    "odo_x_coarse", "odo_x_rem",
    "odo_y_coarse", "odo_y_rem",
    "odo_theta_b", "odo_turns",
)

CAMPOS_REFERENCIA = (
    "corr_ref_x_coarse", "corr_ref_x_rem",
    "corr_ref_y_coarse", "corr_ref_y_rem",
    "corr_ref_theta_b", "corr_ref_turns",
)

TESTES = [
    {
        "nome": "A - deslocamento Y",
        "referencia": (1000, 0, 500, 0, 16384, 0),
        "dl": 20,
        "dr": 20,
        "esperado": (10.0, 5.2, 90.0),
    },
    {
        "nome": "B - preservacao de residuos",
        "referencia": (1012, 3, -506, -7, 0, 0),
        "dl": 20,
        "dr": 20,
        "esperado": (10.323, -5.067, 0.0),
    },
    {
        "nome": "C - rotacao",
        "referencia": (0, 0, 0, 0, 0, 0),
        "dl": -20,
        "dr": 20,
        "esperado": None,
    },
]


def valor(node, nome):
    return int(getattr(node.v, nome))


def ler_pose(node):
    xc, xr, yc, yr, theta_b, turns = (
        valor(node, nome) for nome in CAMPOS_POSE
    )

    return {
        "x_cm": (10 * xc + xr) / 1000,
        "y_cm": (10 * yc + yr) / 1000,
        "theta_graus": (
            theta_b + 65536 * turns
        ) * 180 / 32768,
    }


async def aguardar(client, condicao, mensagem, segundos=4):
    limite = time.monotonic() + segundos

    while time.monotonic() < limite:
        await client.sleep(0.1)
        if condicao():
            return

    raise TimeoutError(mensagem)


def proximo(a, b, tolerancia):
    return math.isclose(a, b, rel_tol=0, abs_tol=tolerancia)


def validar(teste, pose):
    esperado = teste["esperado"]

    if esperado is not None:
        x, y, theta = esperado

        assert proximo(pose["x_cm"], x, 0.002), pose
        assert proximo(pose["y_cm"], y, 0.002), pose
        assert proximo(
            pose["theta_graus"], theta, 0.02
        ), pose

    else:
        # Rotacao pura: variacao angular positiva.
        assert abs(pose["x_cm"]) < 0.02, pose
        assert abs(pose["y_cm"]) < 0.02, pose
        assert 1.0 < pose["theta_graus"] < 5.0, pose


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")
    resultados = []

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def executar():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            execucao_solicitada = False

            async def parar_motores():
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

            try:
                await parar_motores()

                erro = await node.compile(codigo)
                if erro is not None:
                    raise RuntimeError(f"Compilacao: {erro}")

                await node.watch(variables=True)

                execucao_solicitada = True
                erro = await node.run()
                if erro is not None:
                    raise RuntimeError(f"Execucao: {erro}")

                await node.wait_for_variables(
                    set(CAMPOS_POSE)
                    | set(CAMPOS_REFERENCIA)
                    | {
                        "corr_request",
                        "corr_applied",
                        "sim_mode",
                        "sim_request",
                        "sim_dl_01mm",
                        "sim_dr_01mm",
                        "sim_applied",
                        "motor.left.target",
                        "motor.right.target",
                    }
                )

                # Ativar a fonte de incrementos simulados.
                await node.set_variables({"sim_mode": [1]})

                await aguardar(
                    client,
                    lambda: valor(node, "sim_mode") == 1,
                    "Modo de simulacao nao confirmado",
                )

                print("=== CONTINUIDADE V4.1 ===", flush=True)

                for teste in TESTES:
                    nome = teste["nome"]
                    referencia = teste["referencia"]

                    # Referencia configuravel.
                    await node.set_variables({
                        campo: [v]
                        for campo, v in zip(
                            CAMPOS_REFERENCIA, referencia
                        )
                    })

                    await aguardar(
                        client,
                        lambda: tuple(
                            valor(node, campo)
                            for campo in CAMPOS_REFERENCIA
                        ) == referencia,
                        f"Referencia nao confirmada: {nome}",
                    )

                    anterior = valor(node, "corr_applied")

                    await node.set_variables({
                        "corr_request": [1]
                    })

                    await aguardar(
                        client,
                        lambda: (
                            valor(node, "corr_applied")
                            == anterior + 1
                            and valor(node, "corr_request") == 0
                        ),
                        f"Correcao nao confirmada: {nome}",
                    )

                    pose_inicial = ler_pose(node)

                    # Um unico incremento, em unidades de 0,1 mm.
                    await node.set_variables({
                        "sim_dl_01mm": [teste["dl"]],
                        "sim_dr_01mm": [teste["dr"]],
                    })

                    await aguardar(
                        client,
                        lambda: (
                            valor(node, "sim_dl_01mm") == teste["dl"]
                            and valor(node, "sim_dr_01mm") == teste["dr"]
                        ),
                        f"Incrementos nao confirmados: {nome}",
                    )

                    aplicacoes = valor(node, "sim_applied")

                    await node.set_variables({
                        "sim_request": [1]
                    })

                    await aguardar(
                        client,
                        lambda: (
                            valor(node, "sim_applied")
                            == aplicacoes + 1
                            and valor(node, "sim_request") == 0
                        ),
                        f"Incremento nao aplicado: {nome}",
                    )

                    await client.sleep(0.35)

                    if valor(node, "sim_applied") != aplicacoes + 1:
                        raise RuntimeError(
                            f"Incremento duplicado: {nome}"
                        )

                    pose_final = ler_pose(node)
                    validar(teste, pose_final)

                    motores = [
                        valor(node, "motor.left.target"),
                        valor(node, "motor.right.target"),
                    ]

                    if motores != [0, 0]:
                        raise RuntimeError(
                            f"Motores ativos: {motores}"
                        )

                    resultado = {
                        "teste": nome,
                        "referencia": pose_inicial,
                        "incrementos_01mm": {
                            "esquerda": teste["dl"],
                            "direita": teste["dr"],
                        },
                        "pose_final": pose_final,
                        "motores": motores,
                        "estado": "OK",
                    }

                    resultados.append(resultado)

                    print(f"\n{nome}", flush=True)
                    print(
                        "Pose inicial:", pose_inicial,
                        flush=True,
                    )
                    print(
                        "Pose final:", pose_final,
                        flush=True,
                    )
                    print("VALIDADO", flush=True)

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

                print(
                    "\nCONTINUIDADE V4.1: OK",
                    flush=True,
                )
                print("Resultados:", SAIDA, flush=True)

            finally:
                try:
                    await parar_motores()

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

        client.run_async_program(executar)


if __name__ == "__main__":
    main()
