import time
from pathlib import Path

import serial

PORT = (
    "/dev/serial/by-id/"
    "usb-Mobsya.org_Thymio-II_Wireless_"
    "00124B001DF456B0-if00"
)

OUTPUT = Path("diagnostico/serial_raw_pi5.bin")
DURATION = 10

print("=== CAPTURA SÉRIE RAW ===", flush=True)
print("Porta:", PORT, flush=True)

total = 0

with serial.Serial(PORT, baudrate=115200, timeout=0.2) as ser:
    with OUTPUT.open("wb") as output:
        end = time.monotonic() + DURATION

        while time.monotonic() < end:
            data = ser.read(4096)

            if data:
                output.write(data)
                total += len(data)

print("Bytes recebidos:", total, flush=True)
print("Ficheiro:", OUTPUT, flush=True)
