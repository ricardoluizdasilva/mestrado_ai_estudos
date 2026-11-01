"""Ligação e encerramento de thymiodirect 0.1.2 (WSL/Linux)."""
import asyncio
import os
import time
from pathlib import Path
from serial import Serial, SerialException
from thymiodirect import Thymio


def check_port(port: str):
    p = Path(port)
    if not p.exists():
        raise RuntimeError(f"Porta {port} inexistente. Verifique 'usbipd list' no PowerShell e faça usbipd attach --wsl --busid BUSID.")
    if not os.access(port, os.R_OK | os.W_OK):
        raise RuntimeError(f"Sem permissões de leitura/escrita em {port}; verifique grupo dialout.")
    try:
        with Serial(port=port, baudrate=115200, timeout=0.3, write_timeout=0.3):
            pass
    except (SerialException, OSError) as exc:
        raise RuntimeError(f"Não foi possível abrir {port}: {exc}. Feche outros programas que usem o dongle.") from exc


def connect_robot(port: str, timeout: float = 5.0):
    """O connect() do thymiodirect pode bloquear; usar apenas após preflight.

    Executar sob `timeout`/supervisão se for essencial um limite global rígido.
    """
    check_port(port)
    th = Thymio(serial_port=port)
    node_id = None
    try:
        th.connect()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            node_id = th.first_node()
            if node_id is not None:
                return th, node_id
            time.sleep(0.1)
        raise RuntimeError("Porta abriu, mas nenhum Thymio foi descoberto; confirme o emparelhamento e a alimentação.")
    except BaseException:
        shutdown_robot(th, node_id)
        raise


def shutdown_robot(th, node_id):
    """Parar motores e encerrar threads/tarefa discover de thymiodirect 0.1.2."""
    if th is None:
        return
    if node_id is not None:
        try:
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
            time.sleep(0.4)
            print("Comandos de paragem enviados.")
        except Exception as exc:
            print(f"AVISO: não foi possível confirmar envio da paragem: {exc}")
    proxy = getattr(th, "thymio_proxy", None)
    conn = getattr(proxy, "connection", None)
    if proxy is None:
        return

    async def cancel_discovery():
        tasks = [task for task in asyncio.all_tasks()
                 if task is not asyncio.current_task()
                 and not task.done()
                 and "discover" in task.get_coro().__qualname__]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    try:
        if getattr(proxy, "loop", None) and proxy.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(cancel_discovery(), proxy.loop)
            future.result(timeout=3)
    except Exception as exc:
        print(f"AVISO: não foi possível cancelar a descoberta: {exc}")
    if conn is not None:
        try:
            conn.shutdown()
            conn.input_thread.join(timeout=5)
        except Exception as exc:
            print(f"AVISO: erro ao encerrar ligação: {exc}")
    thread = getattr(th, "thread", None)
    if thread is not None and thread.ident is not None:
        thread.join(timeout=7)
        if thread.is_alive():
            print("AVISO: thread Thymio continua ativa")
