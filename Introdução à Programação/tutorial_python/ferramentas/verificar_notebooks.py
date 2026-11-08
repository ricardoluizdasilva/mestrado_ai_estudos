"""Executa os notebooks do tutorial e verifica que não há erros inesperados.

Uso (a partir da pasta tutorial_python):

    python ferramentas/verificar_notebooks.py                    # todos os notebooks
    python ferramentas/verificar_notebooks.py nivel_1_introducao # só uma pasta
    python ferramentas/verificar_notebooks.py nivel_3_ia/N3_04_Redes_Neuronais_NumPy.ipynb

Como funciona:

- Copia o tutorial para uma pasta temporária e executa lá cada notebook, para não
  deixar ficheiros criados pelos exemplos (CSV, módulos, imagens) na pasta original.
  Os notebooks originais não são alterados.
- Substitui as chamadas a input() por respostas pré-definidas, para que os exemplos
  interativos corram sem ninguém a escrever.
- Os erros feitos de propósito (células marcadas com ⚠️) são esperados e não contam.
  Qualquer outro erro faz o script terminar com código 1.

Opções úteis: --kernel (nome do kernel, por omissão python3), --timeout (segundos
por célula, por omissão 600) e --lista (mostra os notebooks sem os executar).
"""

from __future__ import annotations

import argparse
import copy
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

import nbformat
from jupyter_client.manager import KernelManager
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parent.parent
PASTAS = ("nivel_1_introducao", "nivel_2_avancado", "nivel_3_ia")

RESPOSTAS = ["10", "3", "5", "7", "2", "4", "8", "1", "6", "9", "sair", "n", "0"]
CELULA_INPUT = (
    f"_respostas = iter({RESPOSTAS!r} * 50)\n"
    "def _inp(pergunta=''):\n"
    "    resposta = next(_respostas)\n"
    "    print(pergunta + resposta)\n"
    "    return resposta\n"
)
RE_INPUT = re.compile(r"(?<![\w.])input\(")


def de_proposito(fonte: str) -> bool:
    return "⚠️" in fonte or "de propósito" in fonte


def escolher(alvos: list[str]) -> list[Path]:
    if not alvos:
        alvos = list(PASTAS)
    notebooks = []
    for alvo in alvos:
        p = (RAIZ / alvo).resolve()
        if p.is_dir():
            notebooks += sorted(p.glob("*.ipynb"))
        elif p.suffix == ".ipynb" and p.exists():
            notebooks.append(p)
        else:
            sys.exit(f"Não encontrei: {alvo}")
    return notebooks


def executar(
    original: Path, copia: Path, kernel: str, timeout: int
) -> tuple[list, int, str]:
    nb = nbformat.read(original, as_version=4)
    run = copy.deepcopy(nb)
    for c in run.cells:
        if c.cell_type == "code":
            c.outputs = []
            c.source = RE_INPUT.sub("_inp(", c.source)
    run.cells.insert(0, nbformat.v4.new_code_cell(CELULA_INPUT))
    estado = "ok"
    pasta_ipc = Path(tempfile.mkdtemp(prefix="kernel_"))
    try:
        # Em Linux e macOS, o kernel comunica por IPC (sockets locais) em vez de TCP:
        # é igualmente local e evita o aviso «Kernel is running over TCP without encryption».
        # O caminho dos sockets tem de ser absoluto, porque o kernel corre noutra pasta.
        km = KernelManager(kernel_name=kernel)
        if sys.platform != "win32":
            km.transport = "ipc"
            km.ip = str(pasta_ipc / "ipc")
        NotebookClient(
            run,
            km=km,
            kernel_name=kernel,
            timeout=timeout,
            allow_errors=True,
            resources={"metadata": {"path": str(copia.parent)}},
        ).execute()
    except Exception as e:  # noqa: BLE001 - tempo esgotado, kernel morto, etc.
        estado = f"{type(e).__name__}: {str(e).splitlines()[0][:150]}"
    finally:
        shutil.rmtree(pasta_ipc, ignore_errors=True)
    inesperados, esperados = [], 0
    for i, c in enumerate(run.cells[1:], start=1):
        for o in c.get("outputs", []):
            if o.output_type == "error":
                if de_proposito(c.source):
                    esperados += 1
                else:
                    ultima = (
                        c.source.strip().splitlines()[-1][:70]
                        if c.source.strip()
                        else ""
                    )
                    inesperados.append((i, o.ename, str(o.evalue)[:120], ultima))
    return inesperados, esperados, estado


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "alvos", nargs="*", help="pastas ou notebooks (relativos a tutorial_python)"
    )
    ap.add_argument("--kernel", default="python3")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--lista", action="store_true", help="mostra os notebooks e sai")
    args = ap.parse_args()

    notebooks = escolher(args.alvos)
    if args.lista:
        print("\n".join(str(p.relative_to(RAIZ)) for p in notebooks))
        return 0

    temp = Path(tempfile.mkdtemp(prefix="tutorial_python_"))
    trabalho = temp / "tutorial_python"
    shutil.copytree(
        RAIZ,
        trabalho,
        ignore=shutil.ignore_patterns(".git", ".ipynb_checkpoints", "__pycache__"),
    )
    falhas = 0
    t_total = time.time()
    try:
        for p in notebooks:
            rel = p.relative_to(RAIZ)
            t0 = time.time()
            inesperados, esperados, estado = executar(
                p, trabalho / rel, args.kernel, args.timeout
            )
            ok = estado == "ok" and not inesperados
            falhas += not ok
            marca = "OK   " if ok else "FALHA"
            print(
                f"{marca} {rel!s:<62} {time.time() - t0:6.1f} s  erros de propósito: {esperados}",
                flush=True,
            )
            if estado != "ok":
                print(f"      execução interrompida: {estado}")
            for i, nome, valor, ultima in inesperados:
                print(f"      célula {i}: {nome}: {valor}\n        → {ultima}")
    finally:
        shutil.rmtree(temp, ignore_errors=True)

    print(
        f"\n{len(notebooks) - falhas}/{len(notebooks)} notebooks sem erros inesperados "
        f"({time.time() - t_total:.0f} s)."
    )
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
