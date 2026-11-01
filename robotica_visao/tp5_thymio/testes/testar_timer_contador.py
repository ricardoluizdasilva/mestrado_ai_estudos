
import asyncio
import time
from pathlib import Path

from thymiodirect import Thymio


# ============================================================
# CONFIGURACAO
# ============================================================

BASE = Path(__file__).resolve().parent.parent

ASM = BASE / "src" / "aseba" / "teste_timer_contador.asm"

PORTA = "/dev/ttyACM0"

NUM_AMOSTRAS = 6
INTERVALO_AMOSTRAGEM = 0.2


# ============================================================
# ENCERRAMENTO CONTROLADO
# ============================================================


def encerrar(th, node_id):
    """
    Encerramento controlado da comunicacao com o Thymio.

    Compativel com a estrutura interna do thymiodirect 0.1.2.

    Etapas:
      1. Enviar comandos de paragem aos motores.
      2. Solicitar o encerramento da comunicacao.
      3. Terminar a thread de entrada.
      4. Finalizar tarefas asyncio e parar o ciclo.
      5. Aguardar a thread principal.
      6. Limpar tarefas restantes e fechar o ciclo asyncio.
    """

    print("\n=== ENCERRAMENTO ===")

    # ========================================================
    # 1. PARAGEM PREVENTIVA DOS MOTORES
    # ========================================================

    if node_id is not None:
        try:
            robot = th[node_id]

            robot["motor.left.target"] = 0
            robot["motor.right.target"] = 0

            time.sleep(0.5)
            print("Comandos de paragem enviados.")

        except Exception as exc:
            print("AVISO na paragem dos motores:", repr(exc))

    # ========================================================
    # 2. OBTER OBJETOS DE COMUNICACAO
    # ========================================================

    proxy = th.thymio_proxy

    if proxy is None:
        print("Proxy Thymio inexistente.")
        return

    conn = proxy.connection
    loop = proxy.loop

    # ========================================================
    # 3. TERMINAR A RECECAO DE MENSAGENS
    # ========================================================

    if conn is not None:
        try:
            conn.shutdown()
            print("Shutdown da comunicacao solicitado.")

        except Exception as exc:
            print("AVISO no shutdown:", repr(exc))

        entrada = conn.input_thread

        if entrada is not None:
            entrada.join(timeout=5)

            if entrada.is_alive():
                print("AVISO: thread de entrada ainda ativa.")
                return

            print("Thread de entrada terminada.")

    # ========================================================
    # 4. FINALIZAR TAREFAS NO CICLO EM EXECUCAO
    # ========================================================

    async def finalizar_tarefas():
        atual = asyncio.current_task()
        total = 0

        for _ in range(5):
            await asyncio.sleep(0.05)

            pendentes = [
                tarefa
                for tarefa in asyncio.all_tasks()
                if tarefa is not atual and not tarefa.done()
            ]

            if not pendentes:
                break

            total += len(pendentes)

            for tarefa in pendentes:
                tarefa.cancel()

            await asyncio.gather(
                *pendentes,
                return_exceptions=True
            )

        return total

    if loop is not None and loop.is_running():

        futuro = asyncio.run_coroutine_threadsafe(
            finalizar_tarefas(),
            loop
        )

        try:
            total = futuro.result(timeout=5)
            print(f"Tarefas tratadas: {total}")

        except Exception as exc:
            print(
                "AVISO na finalizacao inicial:",
                repr(exc)
            )
            futuro.cancel()

        if loop.is_running():
            loop.call_soon_threadsafe(loop.stop)

    # ========================================================
    # 5. AGUARDAR A THREAD PRINCIPAL
    # ========================================================

    if th.thread is not None:
        th.thread.join(timeout=5)

        if th.thread.is_alive():
            print("AVISO: thread principal ainda ativa.")
            return

        print("Thread principal terminada.")

    # ========================================================
    # 6. LIMPEZA FINAL DAS TAREFAS ASYNCIO
    # ========================================================

    if loop is None:
        print("Ciclo asyncio inexistente.")
        return

    if loop.is_closed():
        print("Ciclo asyncio ja estava fechado.")
        return

    if loop.is_running():
        print("AVISO: ciclo asyncio ainda ativo.")
        return

    async def limpeza_final():
        """
        Cancelar tarefas ainda pendentes depois de a
        thread principal ter terminado.
        """

        atual = asyncio.current_task()

        pendentes = [
            tarefa
            for tarefa in asyncio.all_tasks()
            if tarefa is not atual and not tarefa.done()
        ]

        print(
            "Tarefas pendentes antes da limpeza:",
            len(pendentes)
        )

        for tarefa in pendentes:
            tarefa.cancel()

        if pendentes:
            await asyncio.gather(
                *pendentes,
                return_exceptions=True
            )

        await asyncio.sleep(0)

        restantes = [
            tarefa
            for tarefa in asyncio.all_tasks()
            if tarefa is not atual and not tarefa.done()
        ]

        print(
            "Tarefas pendentes apos limpeza:",
            len(restantes)
        )

        return len(restantes)

    try:
        # O ciclo ja nao esta em execucao noutra thread.
        # Executar temporariamente para concluir cancelamentos.
        restantes = loop.run_until_complete(
            limpeza_final()
        )

        if restantes != 0:
            print(
                "AVISO: ainda existem tarefas pendentes. "
                "O ciclo nao sera fechado."
            )
            return

        # Finalizar geradores assincronos
        loop.run_until_complete(
            loop.shutdown_asyncgens()
        )

        # Finalizar executores asyncio, quando aplicavel.
        if hasattr(loop, "shutdown_default_executor"):
            loop.run_until_complete(
                loop.shutdown_default_executor()
            )

        # Verificacao final antes do fecho
        pendentes = [
            tarefa
            for tarefa in asyncio.all_tasks(loop)
            if not tarefa.done()
        ]

        if pendentes:
            print(
                "AVISO: tarefas pendentes antes de fechar:",
                len(pendentes)
            )
            return

        loop.close()
        print("Ciclo asyncio fechado corretamente.")

    except Exception as exc:
        print(
            "AVISO durante a limpeza final:",
            repr(exc)
        )

    print("Procedimento de encerramento concluido.")


# ============================================================
# TESTE DO TEMPORIZADOR ASEBA
# ============================================================

def main():

    # Verificar a existencia do programa assembly
    if not ASM.is_file():
        raise FileNotFoundError(
            f"Programa Aseba nao encontrado: {ASM}"
        )

    print("=== TP5 - TESTE DO TEMPORIZADOR ASEBA ===")
    print(f"Programa: {ASM}")
    print(f"Porta serie: {PORTA}")

    # Criar ligacao ao Thymio
    th = Thymio(
        serial_port=PORTA,
        refreshing_rate=0.1,
        refreshing_coverage={
            "leds.top",
            "timer.period",
            "motor.left.target",
            "motor.right.target",
        },
    )

    node_id = None

    try:
        # ----------------------------------------------------
        # 1. LIGACAO
        # ----------------------------------------------------

        print("\nA ligar ao Thymio...")

        th.connect()

        # Aguardar pela descoberta do robo
        for tentativa in range(30):
            node_id = th.first_node()

            if node_id is not None:
                break

            time.sleep(0.1)

        if node_id is None:
            raise RuntimeError(
                "Thymio nao encontrado."
            )

        print(f"Thymio conectado: {node_id}")

        # Permitir estabilizacao das primeiras leituras
        time.sleep(0.5)

        robot = th[node_id]

        # ----------------------------------------------------
        # 2. PARAGEM PREVENTIVA
        # ----------------------------------------------------

        robot["motor.left.target"] = 0
        robot["motor.right.target"] = 0

        time.sleep(0.3)

        print("Motores inicialmente parados.")

        # ----------------------------------------------------
        # 3. VERIFICAR EVENTOS
        # ----------------------------------------------------

        eventos = th.events(node_id)

        print("\nEventos disponiveis:")
        print(eventos)

        if "timer0" not in eventos:
            raise RuntimeError(
                "Evento timer0 indisponivel."
            )

        # ----------------------------------------------------
        # 4. CARREGAR PROGRAMA ASEBA
        # ----------------------------------------------------

        print("\nA carregar teste Aseba...")

        programa = ASM.read_text(
            encoding="utf-8"
        )

        th.run_asm(node_id, programa)

        # Aguardar pela inicializacao do programa
        time.sleep(0.3)

        periodo = robot["timer.period"]

        print("timer.period:", periodo)

        if int(periodo[0]) != 100:
            raise RuntimeError(
                "O temporizador nao foi configurado "
                "para 100 ms."
            )

        # ----------------------------------------------------
        # 5. OBSERVAR O CONTADOR
        # ----------------------------------------------------

        print(
            f"\nA observar o contador durante "
            f"{NUM_AMOSTRAS * INTERVALO_AMOSTRAGEM:.1f} "
            "segundos..."
        )

        valores = []

        for i in range(NUM_AMOSTRAS):

            time.sleep(INTERVALO_AMOSTRAGEM)

            contador = int(
                robot["leds.top"][0]
            )

            esquerda = int(
                robot["motor.left.target"]
            )

            direita = int(
                robot["motor.right.target"]
            )

            valores.append(contador)

            print(
                f"Amostra {i + 1}: "
                f"contador={contador} | "
                f"L={esquerda} R={direita}"
            )

            # Confirmar que nao existem comandos de movimento
            if esquerda != 0 or direita != 0:
                raise RuntimeError(
                    "ERRO: comando de motor inesperado!"
                )

        # ----------------------------------------------------
        # 6. VALIDAR RESULTADOS
        # ----------------------------------------------------

        print("\n=== RESULTADOS ===")

        print("Contadores:", valores)

        if valores[-1] > valores[0]:

            incremento = valores[-1] - valores[0]

            print(
                f"Incremento observado: {incremento}"
            )

            print("TIMER0: CONTADOR A AUMENTAR")

        else:
            raise RuntimeError(
                "O contador nao aumentou. "
                "Verificar o programa Aseba."
            )

        print("TESTE DO TEMPORIZADOR: OK")

    finally:
        # Executar sempre a rotina de encerramento
        encerrar(th, node_id)

        print("Comunicacao encerrada.")


# ============================================================
# EXECUCAO
# ============================================================

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(
            "\nTeste interrompido pelo utilizador."
        )

    except Exception as exc:
        print(
            "\nERRO durante o teste:",
            repr(exc)
        )
        raise
