import json
import time
from pathlib import Path

import serial

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

OUTPUT = Path("diagnostico/sequencia_serial_pi5.bin")
LOG = Path("diagnostico/sequencia_serial_pi5.jsonl")

COMMANDS = [
    ("discover", "0200010011a00500"),
    ("info_2", "0400010012a0f8e30200"),
    ("info_3", "0400010012a0f8e30300"),
    ("info_1", "0400010012a0f8e30100"),
    ("info_5", "0400010010a0f8e30500"),
]

def log_event(file, event, data, elapsed):
    record = {
        "elapsed_s": round(elapsed, 6),
        "event": event,
        "length": len(data),
        "hex": data.hex(),
    }
    file.write(json.dumps(record) + "\n")
    file.flush()


print("=== TESTE SEQUÊNCIA SÉRIE ===", flush=True)

start = time.monotonic()
total = 0

with serial.Serial(
    PORT,
    baudrate=115200,
    timeout=0.05,
    write_timeout=1,
) as ser, OUTPUT.open("wb") as binary, LOG.open("w") as log:

    def receive(duration):
        global total

        end = time.monotonic() + duration

        while time.monotonic() < end:
            data = ser.read(4096)

            if data:
                binary.write(data)
                log_event(
                    log,
                    "RX",
                    data,
                    time.monotonic() - start,
                )
                total += len(data)

    # Descoberta inicial
    name, command = COMMANDS[0]
    payload = bytes.fromhex(command)

    ser.write(payload)
    ser.flush()
    log_event(log, "TX", payload, time.monotonic() - start)

    print("Pedido de descoberta enviado", flush=True)
    receive(2.0)

    # Pedidos de informação
    for name, command in COMMANDS[1:]:
        payload = bytes.fromhex(command)

        ser.write(payload)
        ser.flush()

        log_event(
            log,
            "TX",
            payload,
            time.monotonic() - start,
        )

        print("Pedido enviado:", name, flush=True)

        receive(0.25)

    # Receber restantes respostas
    receive(5.0)

print("Bytes RX:", total, flush=True)
print("Captura:", OUTPUT, flush=True)
