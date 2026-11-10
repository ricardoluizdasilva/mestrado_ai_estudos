"""Encerramento testado no TP5 WSL2 e Raspberry Pi 5 Ubuntu; thymiodirect 0.1.2."""
import asyncio
import time

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
