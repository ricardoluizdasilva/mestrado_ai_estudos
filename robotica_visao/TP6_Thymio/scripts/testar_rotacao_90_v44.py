"""TP6 - Calibracao angular: rotacao isolada de 90 graus."""

import json
import time
from datetime import datetime
from pathlib import Path

from tdmclient import ClientAsync

PROGRAMA = Path("aseba/odometria_rotacao_90_v44.aesl")
PASTA = Path("resultados/validacao_rotacoes_90_v44")
NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"


def valor(node, nome):
    return int(getattr(node.v, nome))


def disponivel(node, nome):
    return isinstance(getattr(node.v, nome), (int, float))


async def aguardar(client, condicao, descricao, segundos=5):
    limite = time.monotonic() + segundos

    while time.monotonic() < limite:
        await client.sleep(0.1)
        if condicao():
            return

    raise TimeoutError(descricao)


def main():
    print("=== TP6 - ROTACAO ISOLADA V4.4 ===")
    print("Objetivo: rotacao anti-horaria de aproximadamente 90 graus.")
    print("Realizar apenas UM ensaio por execucao.")
    print()

    confirmacao = input(
        "Robot alinhado, espaco livre e supervisao? "
        "Escreva INICIAR: "
    ).strip()

    if confirmacao != "INICIAR":
        print("Ensaio cancelado.")
        return

    codigo = PROGRAMA.read_text(encoding="utf-8")
    resultado = {}

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
                    raise RuntimeError(
                        f"Erro na compilacao: {erro}"
                    )

                await node.watch(variables=True)

                await node.set_variables({
                    "seq_arm": [0],
                    "seq_request": [0],
                    "seq_abort": [0],
                })

                iniciou = True
                erro = await node.run()

                if erro is not None:
                    raise RuntimeError(
                        f"Erro de execucao: {erro}"
                    )

                campos = {
                    "seq_state",
                    "seq_fault",
                    "seq_arm",
                    "seq_request",
                    "seq_angle_b",
                    "odo_theta_b",
                    "odo_turns",
                    "odo_x_coarse",
                    "odo_x_rem",
                    "odo_y_coarse",
                    "odo_y_rem",
                    "motor.left.target",
                    "motor.right.target",
                    "motor.left.speed",
                    "motor.right.speed",
                }

                await node.wait_for_variables(campos)

                await aguardar(
                    client,
                    lambda: all(
                        disponivel(node, campo)
                        for campo in campos
                    ),
                    "Variaveis TDM nao recebidas",
                )

                if valor(node, "seq_state") != 0:
                    raise RuntimeError(
                        "Estado inicial diferente de zero"
                    )

                if (
                    valor(node, "seq_arm") != 0
                    or valor(node, "seq_request") != 0
                ):
                    raise RuntimeError(
                        "Controlador indevidamente armado"
                    )

                print("V4.4 carregada. Estado inicial seguro.")
                print("A iniciar rotacao...", flush=True)

                # Autorizar em duas etapas, como na V3.8.
                await node.set_variables({"seq_arm": [1]})

                await aguardar(
                    client,
                    lambda: valor(node, "seq_arm") == 1,
                    "Armamento nao confirmado",
                )

                await node.set_variables({"seq_request": [1]})

                estado_anterior = -1
                limite = time.monotonic() + 30.0

                while time.monotonic() < limite:
                    await client.sleep(0.1)

                    estado = valor(node, "seq_state")
                    falha = valor(node, "seq_fault")

                    if estado != estado_anterior:
                        print(
                            f"Estado {estado} | Falha {falha}",
                            flush=True,
                        )
                        estado_anterior = estado

                    if estado == 6 or falha != 0:
                        raise RuntimeError(
                            f"Rotacao abortada: falha {falha}"
                        )

                    if estado == 5:
                        break
                else:
                    raise TimeoutError(
                        "Limite de tempo da rotacao excedido"
                    )

                # Parar explicitamente e aguardar estabilizacao.
                await parar()
                await client.sleep(0.6)

                velocidades = (
                    valor(node, "motor.left.speed"),
                    valor(node, "motor.right.speed"),
                )

                if any(abs(v) > 2 for v in velocidades):
                    raise RuntimeError(
                        f"Rodas ainda em movimento: {velocidades}"
                    )

                theta_b = valor(node, "odo_theta_b")
                turns = valor(node, "odo_turns")
                angle_b = valor(node, "seq_angle_b")

                x_cm = (
                    10 * valor(node, "odo_x_coarse")
                    + valor(node, "odo_x_rem")
                ) / 1000

                y_cm = (
                    10 * valor(node, "odo_y_coarse")
                    + valor(node, "odo_y_rem")
                ) / 1000

                theta = (
                    theta_b + 65536 * turns
                ) * 180 / 32768

                angulo_controlador = (
                    angle_b * 180 / 32768
                )

                resultado.update({
                    "instante": datetime.now().isoformat(),
                    "versao": "V4.4",
                    "estado_final": valor(node, "seq_state"),
                    "falha": valor(node, "seq_fault"),
                    "x_cm": x_cm,
                    "y_cm": y_cm,
                    "angulo_odometria_graus": theta,
                    "angulo_controlador_graus":
                        angulo_controlador,
                    "velocidades_finais": list(velocidades),
                })

                print("\n=== RESULTADOS DA ODOMETRIA ===")
                print(f"X: {x_cm:+.3f} cm")
                print(f"Y: {y_cm:+.3f} cm")
                print(f"Angulo estimado: {theta:+.3f} graus")
                print(
                    "Angulo do controlador: "
                    f"{angulo_controlador:+.3f} graus"
                )
                print("ROTACAO V4.4: CONCLUIDA", flush=True)

            finally:
                try:
                    await node.set_variables({
                        "seq_abort": [1],
                        "motor.left.target": [0],
                        "motor.right.target": [0],
                    })

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

    if not resultado:
        raise RuntimeError("Ensaio sem resultados.")

    print("\nMeça o angulo fisico com um transferidor.")
    print("Introduza o angulo absoluto relativamente aos 0 graus.")
    print("Use valor positivo para rotacao anti-horaria.")

    texto = input(
        "Angulo fisico medido (graus): "
    ).strip().replace(",", ".")

    if texto:
        angulo_fisico = float(texto)

        resultado["angulo_fisico_graus"] = angulo_fisico
        resultado["erro_fisico_face_90_graus"] = (
            angulo_fisico - 90.0
        )
        resultado["erro_odometria_graus"] = (
            resultado["angulo_odometria_graus"]
            - angulo_fisico
        )
    else:
        resultado["angulo_fisico_graus"] = None
        print("Angulo fisico nao medido.")

    PASTA.mkdir(parents=True, exist_ok=True)

    destino = PASTA / (
        "rotacao_90_"
        + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        + ".json"
    )

    destino.write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n=== RESULTADO FINAL ===")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print("Evidencia:", destino)


if __name__ == "__main__":
    main()
