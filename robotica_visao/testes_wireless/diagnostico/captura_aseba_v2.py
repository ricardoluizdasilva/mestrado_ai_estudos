import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

import serial

# Configuração
PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

# OUTPUT = Path("diagnostico/aseba_trace_pi5.jsonl")
OUTPUT = Path("diagnostico/aseba_trace_pi5_v2.jsonl")

MAX_RECORDS = 2000

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

original_read = serial.Serial.read
original_write = serial.Serial.write

count = 0
start = time.monotonic()

log_file = OUTPUT.open("w", encoding="utf-8", buffering=1)


"""
def record(direction, data):
    global count

    if count >= MAX_RECORDS:
        return

    count += 1

    entry = {
        "seq": count,
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "elapsed_s": round(time.monotonic() - start, 6),
        "direction": direction,
        "length": len(data),
        "hex": bytes(data[:64]).hex(),
        "truncated": len(data) > 64,
    }

    log_file.write(json.dumps(entry) + "\n")
"""

def record(direction, data, requested_bytes=None, duration_ms=None):
    global count

    if count >= MAX_RECORDS:
        return

    count += 1

    entry = {
        "seq": count,
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "elapsed_s": round(time.monotonic() - start, 6),
        "direction": direction,
        "requested_bytes": requested_bytes,
        "received_bytes": len(data),
        "length": len(data),
        "read_duration_ms": (
            round(duration_ms, 3)
            if duration_ms is not None else None
        ),
        "short_read": (
            len(data) < requested_bytes
            if requested_bytes is not None else False
        ),
        "hex": bytes(data).hex(),
        "truncated": False,
    }

    log_file.write(json.dumps(entry) + "\n")

'''
def traced_read(self, size=1):
    data = original_read(self, size)

    if data:
        record("RX", data)

    return data
'''

def traced_read(self, size=1):
    start_read = time.monotonic()

    data = original_read(self, size)

    duration_ms = (
        time.monotonic() - start_read
    ) * 1000

    record(
        "RX",
        data,
        requested_bytes=size,
        duration_ms=duration_ms,
    )

    if len(data) != size:
        print(
            f"[SHORT READ] "
            f"solicitados={size}, "
            f"recebidos={len(data)}, "
            f"tempo={duration_ms:.2f} ms",
            flush=True
        )

    return data

def traced_write(self, data):
    record("TX", data)
    return original_write(self, data)


# Interceção apenas neste processo
serial.Serial.read = traced_read
serial.Serial.write = traced_write

# Importar após instalar a instrumentação
from thymiodirect import Thymio

print("=== DIAGNÓSTICO ASEBA ===", flush=True)
print("Python:", sys.version.split()[0], flush=True)
print("Porta:", PORT, flush=True)
print("Registo:", OUTPUT, flush=True)

robot = Thymio(
    serial_port=PORT,
    refreshing_rate=0.2,
    refreshing_coverage={"prox.horizontal"},
    on_connect=lambda node_id: print(
        f"Thymio conectado: {node_id}",
        flush=True
    ),
)

try:
    print("A estabelecer ligação...", flush=True)
    robot.connect()

    node_id = robot.first_node()
    print("ID:", node_id, flush=True)

    time.sleep(5)

finally:
    log_file.flush()
    print("Registos:", count, flush=True)
