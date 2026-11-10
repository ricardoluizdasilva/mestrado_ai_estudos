import json
import time
from datetime import datetime, timezone
from pathlib import Path

import serial

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

OUTPUT = Path("diagnostico/serial_handshake_pi5.bin")
LOG = Path("diagnostico/serial_handshake_pi5.jsonl")

DURATION = 10
HANDSHAKE = bytes.fromhex("0200010011a00500")


def log_event(handle, event, data=b""):
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "length": len(data),
        "hex": data.hex(),
    }
    handle.write(json.dumps(entry) + "\n")


print("=== CAPTURA SÉRIE COM HANDSHAKE ===", flush=True)

total = 0

with serial.Serial(
    PORT,
    baudrate=115200,
    timeout=0.2,
    write_timeout=1,
) as ser:

    with OUTPUT.open("wb") as output, LOG.open("w") as log:

        print("A enviar pedido de descoberta...", flush=True)

        written = ser.write(HANDSHAKE)
        ser.flush()

        if written != len(HANDSHAKE):
            raise RuntimeError("Pedido de descoberta incompleto")

        log_event(log, "TX", HANDSHAKE)

        end = time.monotonic() + DURATION

        while time.monotonic() < end:
            data = ser.read(4096)

            if data:
                output.write(data)
                log_event(log, "RX", data)
                total += len(data)

print("Bytes recebidos:", total, flush=True)
print("Ficheiro:", OUTPUT, flush=True)
print("Registo:", LOG, flush=True)
