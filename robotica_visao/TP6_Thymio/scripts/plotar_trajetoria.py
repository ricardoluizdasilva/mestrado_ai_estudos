"""Gráfico de trajetória calculada. Requer matplotlib (opcional)."""
import argparse
import csv
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trajetoria',required=True)
    ap.add_argument('--saida',default='resultados/trajetoria.png')
    args=ap.parse_args()
    with open(args.trajetoria,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise ValueError('Trajetória vazia')
    x=[float(row['x_cm']) for row in rows]
    y=[float(row['y_cm']) for row in rows]
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7,6))
    ax.plot(x,y,label='Odometria RK2')
    ax.scatter([x[0],x[-1]],[y[0],y[-1]],s=45)
    ax.annotate('Início',(x[0],y[0]))
    ax.annotate('Fim',(x[-1],y[-1]))
    ax.set(xlabel='x [cm]',ylabel='y [cm]',title='TP6 — Trajetória estimada')
    ax.axis('equal');ax.grid(True);ax.legend()
    path=Path(args.saida);path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=160,bbox_inches='tight')
    plt.close(fig)
    print('Gráfico:',path)

if __name__=='__main__':main()
