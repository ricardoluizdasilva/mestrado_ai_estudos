"""Aquisição de sensores Wireless com encerramento partilhado.
Executar nesta pasta ou indicar THYMIO_PORT; não envia movimento.
"""
import argparse
import csv
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from thymiodirect import Thymio
from thymio_shutdown import encerrar

DEFAULT_PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_00124B001DF456B0-if00"
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=os.environ.get("THYMIO_PORT", DEFAULT_PORT))
    parser.add_argument("--duration", type=float, default=10)
    parser.add_argument("--output", type=Path, default=Path("sensores_modular.csv"))
    args = parser.parse_args()
    if args.duration <= 0:
        parser.error("A duração tem de ser positiva")

    th = Thymio(
        serial_port=args.port,
        refreshing_rate=0.2,
        refreshing_coverage={"prox.horizontal"},
        on_connect=lambda node_id: print(f"Thymio conectado: {node_id}", flush=True),
    )
    node_id = None
    samples = []
    collecting = False
    try:
        print("A estabelecer comunicação...", flush=True)
        th.connect()  # A descoberta pode bloquear; usar timeout externo.
        node_id = th.first_node()
        if node_id != 58360:
            raise RuntimeError(f"Nó inesperado: {node_id}")
        print(f"ID: {node_id}", flush=True)
        start = time.monotonic()
        collecting = True

        def observer(updated_node_id):
            if not collecting or updated_node_id != node_id:
                return
            elapsed = time.monotonic() - start
            if elapsed > args.duration:
                return
            try:
                values = list(th[node_id]["prox.horizontal"])
                if len(values) == 7:
                    samples.append([datetime.now(timezone.utc).isoformat(), round(elapsed, 4), *values])
            except (KeyError, TypeError, ValueError) as exc:
                print(f"Aviso de leitura: {exc}", flush=True)

        th.set_variable_observer(node_id, observer)
        print(f"A recolher sensores durante {args.duration:g} s...", flush=True)
        time.sleep(args.duration)
    finally:
        collecting = False
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp_utc", "elapsed_s", *[f"prox_{i}" for i in range(7)]])
            writer.writerows(samples)
        print(f"Amostras: {len(samples)}", flush=True)
        print(f"Ficheiro: {args.output}", flush=True)
        encerrar(th, node_id)
        # A rotina validada produz mensagens de aviso se encontrar problemas.

if __name__ == "__main__":
    main()
