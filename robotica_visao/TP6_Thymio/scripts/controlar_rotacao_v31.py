"""TP6 - Controlo de rotação por odometria V3.1."""

import csv
import time
from pathlib import Path
from tdmclient import ClientAsync

PROGRAMA = Path("resultados/odometria_embarcada_v31.aesl")
SAIDA = Path("resultados/controlo_rotacao_45_v31.csv")

NODE_ID = "d2e63ca0-00fa-4913-b67b-563cc7c73352"

ALVO_GRAUS = 45.0
REDUZIR_GRAUS = 30.0
PARAR_GRAUS = 42.0
LIMITE_SEGUNDOS = 6.0

ESCALA_GRAUS = 180.0 / 32768


def verificar(resultado, operacao):
    if resultado is not None:
        raise RuntimeError(f"{operacao}: {resultado}")


def main():
    codigo = PROGRAMA.read_text(encoding="utf-8")
    linhas = []

    with ClientAsync(
        tdm_addr="127.0.0.1",
        tdm_port=8596,
    ) as client:

        async def executar():
            node = await client.wait_for_node()

            if node.id_str != NODE_ID:
                raise RuntimeError("Thymio inesperado")

            await node.lock()
            iniciado = False

            async def motores(esq, direita):
                resultado = await node.set_variables({
                    "motor.left.target": [esq],
                    "motor.right.target": [direita],
                })
                verificar(resultado, "Comando motores")

            try:
                await motores(0, 0)

                verificar(await node.compile(codigo), "Compilação")

                await node.watch(variables=True)

                iniciado = True
                verificar(await node.run(), "Execução")

                await node.wait_for_variables({
                    "odo_snapshot",
                    "odo_turns",
                })

                await client.sleep(0.2)

                snapshot = list(map(int, node.v.odo_snapshot))
                theta_inicio = (
                    snapshot[3] + 65536 * int(node.v.odo_turns)
                ) * ESCALA_GRAUS

                print("Orientação inicial:", theta_inicio)

                print("A iniciar rotação -60/+60")
                await motores(-60, 60)

                inicio = time.monotonic()
                ultimo_tick = None
                ultima_atualizacao = inicio
                reduzido = False
                motivo = "limite_temporal"

                while True:
                    await client.sleep(0.1)

                    agora = time.monotonic()
                    tempo = agora - inicio

                    s = list(map(int, node.v.odo_snapshot))
                    turns = int(node.v.odo_turns)

                    ticks, _, _, theta_b, ve, vd = s

                    theta = (
                        theta_b + 65536 * turns
                    ) * ESCALA_GRAUS

                    relativo = theta - theta_inicio

                    linhas.append({
                        "tempo_s": round(tempo, 3),
                        "ticks": ticks,
                        "theta_rel_graus": round(relativo, 5),
                        "vel_esq": ve,
                        "vel_dir": vd,
                    })

                    print(
                        f"t={tempo:.2f}s "
                        f"theta={relativo:.2f}° "
                        f"vel=({ve},{vd})",
                        flush=True,
                    )

                    if ticks != ultimo_tick:
                        ultimo_tick = ticks
                        ultima_atualizacao = agora

                    if relativo >= PARAR_GRAUS:
                        motivo = "limiar_angular"
                        break

                    if relativo < -3:
                        motivo = "sentido_inesperado"
                        break

                    if agora - ultima_atualizacao > 0.8:
                        motivo = "odometria_sem_atualizacao"
                        break

                    if tempo >= LIMITE_SEGUNDOS:
                        break

                    if relativo >= REDUZIR_GRAUS and not reduzido:
                        print("A reduzir velocidade.", flush=True)
                        await motores(-30, 30)
                        reduzido = True

                # Paragem imediata ao sair do ciclo.
                await motores(0, 0)
                print("Motivo de paragem:", motivo, flush=True)

                # Observar eventual rotação residual.
                await client.sleep(0.7)

                s = list(map(int, node.v.odo_snapshot))
                turns = int(node.v.odo_turns)

                theta_final = (
                    s[3] + 65536 * turns
                ) * ESCALA_GRAUS - theta_inicio

                print("\n=== RESULTADO ===")
                print(f"Alvo: {ALVO_GRAUS:.3f}°")
                print(f"Orientação final estimada: {theta_final:.3f}°")
                print(f"Desvio estimado: {theta_final - ALVO_GRAUS:+.3f}°")
                print("Motivo:", motivo)

                SAIDA.parent.mkdir(parents=True, exist_ok=True)

                with SAIDA.open(
                    "w", newline="", encoding="utf-8"
                ) as f:
                    writer = csv.DictWriter(
                        f, fieldnames=linhas[0].keys()
                    )
                    writer.writeheader()
                    writer.writerows(linhas)

                print("CSV:", SAIDA)

                if motivo != "limiar_angular":
                    raise RuntimeError(
                        "Controlo interrompido antes do limiar angular."
                    )

            finally:
                try:
                    await motores(0, 0)
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

        client.run_async_program(executar)


if __name__ == "__main__":
    main()
