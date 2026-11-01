"""Compara ficheiros CSV TP5 e produz métricas e gráficos PNG."""
import argparse
import csv
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def metrics(rows, motor, tmin):
    samples = [(float(r['referencia']), float(r[f'velocidade_{motor}'])) for r in rows if float(r['tempo']) >= tmin]
    if not samples:
        return None
    error = [r - v for r, v in samples]
    n = len(error)
    return {'n': n, 'media': sum(v for _, v in samples)/n,
            'mae': sum(abs(e) for e in error)/n,
            'rmse': math.sqrt(sum(e*e for e in error)/n)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csvs', nargs='*', type=Path)
    ap.add_argument('--desde', type=float, default=1.0)
    args = ap.parse_args()
    csvs = args.csvs or sorted(Path(__file__).resolve().parent.parent.joinpath('resultados').glob('*.csv'))
    outdir = Path(__file__).resolve().parent.parent / 'resultados' / 'graficos'
    outdir.mkdir(parents=True, exist_ok=True)
    summary = []
    for path in csvs:
        with path.open(newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        if not rows or not {'tempo','referencia','velocidade_esquerda','velocidade_direita'}.issubset(rows[0]):
            print('Ignorado (formato inválido):', path)
            continue
        t = [float(r['tempo']) for r in rows]
        ref = [float(r['referencia']) for r in rows]
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(t, ref, linestyle='--', label='Referência')
        for motor in ('esquerda', 'direita'):
            ax.plot(t, [float(r[f'velocidade_{motor}']) for r in rows], label=motor)
            m = metrics(rows, motor, args.desde)
            if m:
                summary.append({'experiencia': path.name, 'motor': motor, **m})
        ax.set(title=path.stem, xlabel='Tempo (s)', ylabel='Velocidade (unid. Thymio)')
        ax.legend()
        ax.grid(True, alpha=.25)
        fig.tight_layout()
        dest = outdir / f'{path.stem}.png'
        fig.savefig(dest, dpi=160)
        plt.close(fig)
        print('Gráfico:', dest)
    if summary:
        path = outdir / 'metricas.csv'
        with path.open('w', newline='', encoding='utf-8') as f:
            wr = csv.DictWriter(f, fieldnames=list(summary[0]))
            wr.writeheader(); wr.writerows(summary)
        for s in summary:
            print(f"{s['experiencia']} | {s['motor']} | n={s['n']} | média={s['media']:.2f} MAE={s['mae']:.2f} RMSE={s['rmse']:.2f}")
        print('Métricas:', path)


if __name__ == '__main__':
    main()
