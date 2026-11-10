from pathlib import Path
from collections import Counter

PATH = Path("diagnostico/sequencia_serial_pi5.bin")
NODE_ID = 58360

data = PATH.read_bytes()

offset = 0
messages = []
errors = []
types = Counter()

print("=== ANÁLISE DO FLUXO ASEBA ===")
print("Bytes recebidos:", len(data))

while offset < len(data):
    remaining = len(data) - offset

    if remaining < 6:
        errors.append({
            "offset": offset,
            "reason": "Cabeçalho incompleto",
            "remaining": remaining,
        })
        break

    header = data[offset:offset + 6]

    length = int.from_bytes(header[0:2], "little")
    source = int.from_bytes(header[2:4], "little")
    message_id = int.from_bytes(header[4:6], "little")

    end = offset + 6 + length

    if end > len(data):
        errors.append({
            "offset": offset,
            "reason": "Payload ultrapassa o fim da captura",
            "length": length,
            "source": source,
            "message_id": message_id,
            "available": len(data) - offset - 6,
        })
        break

    if source != NODE_ID:
        errors.append({
            "offset": offset,
            "reason": "Origem inesperada",
            "length": length,
            "source": source,
            "message_id": message_id,
        })
        break

    payload = data[offset + 6:end]

    messages.append({
        "offset": offset,
        "length": length,
        "source": source,
        "message_id": message_id,
        "payload": payload,
    })

    types[message_id] += 1
    offset = end

print("\n=== RESULTADOS ===")
print("Mensagens enquadradas:", len(messages))
print("Bytes consumidos:", offset)
print("Bytes restantes:", len(data) - offset)
print("Anomalias:", len(errors))

print("\n=== TIPOS DE MENSAGEM ===")
for message_id, count in sorted(types.items()):
    print(f"0x{message_id:04X}: {count}")

print("\n=== ÚLTIMAS 10 MENSAGENS ===")
for m in messages[-10:]:
    print(
        f"offset={m['offset']:5} "
        f"origem={m['source']:5} "
        f"tipo=0x{m['message_id']:04X} "
        f"payload={m['length']:4}"
    )

if errors:
    print("\n=== PRIMEIRA ANOMALIA ===")
    for error in errors:
        print(error)

    pos = errors[0]["offset"]
    start = max(0, pos - 32)
    end = min(len(data), pos + 96)

    print("\n=== BYTES EM TORNO DA ANOMALIA ===")
    for i in range(start, end, 16):
        chunk = data[i:min(i + 16, end)]
        print(f"{i:06d}: {chunk.hex(' ')}")
else:
    print("\nNenhuma anomalia de enquadramento encontrada.")
