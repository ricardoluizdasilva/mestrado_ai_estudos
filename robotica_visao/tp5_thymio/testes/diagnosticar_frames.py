from pathlib import Path
import time

ficheiro = Path("/mnt/c/Users/ricar/ThymioCam/frame.jpg")

print("A verificar atualizações da webcam durante 10 segundos...")

anterior = None
alteracoes = 0
inicio = time.monotonic()

while time.monotonic() - inicio < 10:
    if ficheiro.exists():
        stat = ficheiro.stat()
        atual = (stat.st_mtime_ns, stat.st_size)

        if atual != anterior:
            alteracoes += 1
            anterior = atual
            print(
                f"Frame {alteracoes:03d} | "
                f"Tamanho: {stat.st_size:6d} bytes | "
                f"mtime_ns: {stat.st_mtime_ns}"
            )

    time.sleep(0.05)

print()
print("Atualizações observadas:", alteracoes)
print("Frequência aproximada:", round(alteracoes / 10, 2), "FPS")
