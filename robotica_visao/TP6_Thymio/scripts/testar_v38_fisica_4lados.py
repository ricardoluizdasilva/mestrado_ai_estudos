
"""TP6 - Teste físico integrado: reta de 10 cm + rotação de 90°."""

import csv
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v38_fisica_4lados.aesl")
SAIDA = Path("resultados/sequencia_v38_fisica_4lados.csv")
ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

ESCALA_ANGULAR = 180 / 32768
LIMIAR_OBSTACULO = 3000
TEMPO_MAXIMO_S = 80

codigo = PROGRAMA.read_text(encoding="utf-8")


def verificar(resultado, operacao):
    if resultado is not None:
        raise RuntimeError(f"{operacao}: {resultado}")


def main():
    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def testar():
            node = await client.wait_for_node()

            if node.id_str != ID:
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            iniciado = False
            registos = []

            async def parar():
                await node.set_variables({
                    "motor.left.target": [0],
                    "motor.right.target": [0],
                })

            try:
                await parar()
                verificar(
                    await node.compile(codigo),
                    "Compilação",
                )

                await node.watch(variables=True)

                iniciado = True
                verificar(await node.run(), "Execução")

                await node.wait_for_variables({
                    "seq_state",
                    "seq_side",
                    "seq_arm",
                    "seq_request",
                    "seq_fault",
                    "seq_progress",
                    "seq_angle_b",
                    "seq_line_ticks",
                    "seq_turn_ticks",
                    "odo_ticks",
                    "odo_x_coarse",
                    "odo_x_rem",
                    "odo_y_coarse",
                    "odo_y_rem",
                    "odo_theta_b",
                    "odo_turns",
                    "motor.left.target",
                    "motor.right.target",
                    "prox.horizontal",
                })

                await client.sleep(0.4)

                sensores = list(map(int, node.v.prox.horizontal))

                if max(sensores[:5]) > LIMIAR_OBSTACULO:
                    raise RuntimeError(
                        "Obstáculo detetado antes do arranque"
                    )

                if int(node.v.seq_state) != 0:
                    raise RuntimeError("Estado inicial inesperado")

                print("=== TESTE FÍSICO V3.6.1 ===", flush=True)
                print("Sensores iniciais:", sensores, flush=True)

                await node.set_variables({
                    "seq_abort": [0],
                    "seq_arm": [1],
                })
                # Aguardar confirmação do TDM, sem iniciar motores.
                prazo_armamento = time.monotonic() + 2.0

                while time.monotonic() < prazo_armamento:
                    await client.sleep(0.1)

                    arm = int(node.v.seq_arm)
                    estado = int(node.v.seq_state)
                    falha = int(node.v.seq_fault)

                    if estado != 0 or falha != 0:
                        raise RuntimeError(
                            f"Estado inesperado durante armamento: "
                            f"state={estado}, fault={falha}"
                        )

                    if arm == 1:
                        break
                else:
                    raise RuntimeError(
                        "Armamento não confirmado em 2 segundos"
                    )

                print("Controlador armado.", flush=True)

                await node.set_variables({"seq_request": [1]})
                print("Sequência autorizada.", flush=True)

                inicio = time.monotonic()
                estado_anterior = -1
                ultimo_tick = None
                ultima_atualizacao = inicio
                motivo = None

                while time.monotonic() - inicio < TEMPO_MAXIMO_S:
                    await client.sleep(0.15)

                    agora = time.monotonic()
                    estado = int(node.v.seq_state)
                    falha = int(node.v.seq_fault)
                    tick = int(node.v.odo_ticks)
                    proximidade = list(
                        map(int, node.v.prox.horizontal)
                    )

                    if tick != ultimo_tick:
                        ultimo_tick = tick
                        ultima_atualizacao = agora

                    if agora - ultima_atualizacao > 1.5:
                        motivo = "temporizador_sem_atualizacao"
                        break

                    linha = {
                        "tempo_s": round(agora - inicio, 3),
                        "estado": estado,
                        "lado": int(node.v.seq_side),
                        "falha": falha,
                        "ticks": tick,
                        "distancia_cm": (
                            int(node.v.seq_progress) / 1000
                        ),
                        "rotacao_rel_graus": (
                            int(node.v.seq_angle_b)
                            * ESCALA_ANGULAR
                        ),
                        "motor_esq": int(
                            node.v.motor.left.target
                        ),
                        "motor_dir": int(
                            node.v.motor.right.target
                        ),
                        "prox_max": max(proximidade[:5]),
                    }

                    registos.append(linha)

                    if estado != estado_anterior:
                        print(
                            f"Estado {estado}: "
                            f"dist={linha['distancia_cm']:.3f} cm, "
                            f"angulo={linha['rotacao_rel_graus']:.2f}°",
                            flush=True,
                        )
                        estado_anterior = estado

                    if estado == 6:
                        motivo = f"falha_aseba_{falha}"
                        break

                    if estado == 5:
                        motivo = "concluido"
                        break

                if motivo is None:
                    motivo = "timeout_python"

                await parar()
                await client.sleep(0.5)

                xc = int(node.v.odo_x_coarse)
                xr = int(node.v.odo_x_rem)
                yc = int(node.v.odo_y_coarse)
                yr = int(node.v.odo_y_rem)

                x = (10 * xc + xr) / 1000
                y = (10 * yc + yr) / 1000

                theta = (
                    int(node.v.odo_theta_b)
                    + 65536 * int(node.v.odo_turns)
                ) * ESCALA_ANGULAR

                print("\n=== RESULTADOS ===", flush=True)
                print("Motivo:", motivo, flush=True)
                print("Estado final:", int(node.v.seq_state))
                print("Lados concluídos:", int(node.v.seq_side))
                print("Falha:", int(node.v.seq_fault))
                print(f"X global: {x:+.4f} cm")
                print(f"Y global: {y:+.4f} cm")
                print(f"Orientação global: {theta:+.3f}°")
                print(
                    "Ciclos reta:",
                    int(node.v.seq_line_ticks),
                )
                print(
                    "Ciclos rotação:",
                    int(node.v.seq_turn_ticks),
                )

                SAIDA.parent.mkdir(
                    parents=True, exist_ok=True
                )

                if registos:
                    with SAIDA.open(
                        "w", newline="", encoding="utf-8"
                    ) as ficheiro:
                        writer = csv.DictWriter(
                            ficheiro,
                            fieldnames=registos[0].keys(),
                        )
                        writer.writeheader()
                        writer.writerows(registos)

                    print("CSV:", SAIDA)

                if motivo != "concluido":
                    raise RuntimeError(
                        f"Sequência interrompida: {motivo}"
                    )

                if int(node.v.seq_side) != 4:
                    raise RuntimeError(
                        "Não foram concluídos os quatro lados"
                    )

                if int(node.v.seq_fault) != 0:
                    raise RuntimeError("Falha Aseba registada")

                print("QUADRADO V3.8: CONCLUÍDO")

            finally:
                try:
                    await node.set_variables({"seq_abort": [1]})
                    await parar()
                    print("Paragem de segurança solicitada.")
                finally:
                    try:
                        if iniciado:
                            await node.stop()
                    finally:
                        try:
                            await node.watch(variables=False)
                        finally:
                            await node.unlock()
                            print("Nó desbloqueado.")

        client.run_async_program(testar)


if __name__ == "__main__":
    main()

