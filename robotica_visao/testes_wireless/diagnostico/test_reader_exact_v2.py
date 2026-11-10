import json
import sys
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

from thymiodirect import Thymio
from thymiodirect.connection import InputThread
from thymiodirect.message import Message

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

OUTPUT = Path("diagnostico/reader_exact_pi5_v2.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

MAX_PAYLOAD = 4096
TIMEOUT_S = 2.0

original_read_message = InputThread.read_message
log_lock = threading.Lock()


def log_event(event, **details):
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **details,
    }

    with log_lock:
        with OUTPUT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")


def read_exact(io, size, timeout=TIMEOUT_S):
    deadline = time.monotonic() + timeout
    result = bytearray()

    while len(result) < size:
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Leitura incompleta: "
                f"{len(result)}/{size} bytes"
            )

        remaining = size - len(result)
        chunk = io.read(remaining)

        if chunk:
            result.extend(chunk)
        else:
            log_event(
                "empty_read",
                requested=remaining,
                accumulated=len(result),
            )

    return bytes(result)


def read_message_exact(self):
    try:
        # Aseba: comprimento (2), origem (2), ID (2)
        header = read_exact(self.io, 6)
        payload_len = int.from_bytes(header[:2], "little")
        source_node = int.from_bytes(header[2:4], "little")
        message_id = int.from_bytes(header[4:6], "little")

        log_event(
            "header",
            length=payload_len,
            source_node=source_node,
            message_id=message_id,
            header_hex=header.hex(),
        )

        if payload_len > MAX_PAYLOAD:
            raise ValueError(
                f"Comprimento suspeito: {payload_len}"
            )

        payload = read_exact(self.io, payload_len)

        log_event(
            "message",
            length=payload_len,
            source_node=source_node,
            message_id=message_id,
            header_hex=header.hex(),
            payload_hex=payload.hex(),
        )

        return Message(message_id, source_node, payload)

    except Exception as exc:
        log_event(
            "read_error",
            error_type=type(exc).__name__,
            error=str(exc),
        )
        raise


InputThread.read_message = read_message_exact

print("=== TESTE LEITOR ASEBA EXACT ===", flush=True)
print("Python:", sys.version.split()[0], flush=True)
print("Porta:", PORT, flush=True)

robot = Thymio(
    serial_port=PORT,
    refreshing_rate=0.2,
    refreshing_coverage={"prox.horizontal"},
    on_connect=lambda node_id: print(
        f"Thymio conectado: {node_id}",
        flush=True,
    ),
)

print("A estabelecer ligação...", flush=True)

robot.connect()

node_id = robot.first_node()
print("ID:", node_id, flush=True)

time.sleep(5)

print("Teste concluído.", flush=True)
