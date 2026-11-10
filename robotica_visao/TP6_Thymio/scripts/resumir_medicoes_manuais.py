"""TP6 Q2(b), Q3: médias e desvios-padrão amostrais sem calibração."""
import argparse
import csv
import statistics
from collections import defaultdict

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--medicoes',default='modelos/medicoes_pose.csv')
    a=p.parse_args()
    by=defaultdict(list)
    with open(a.medicoes,newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                x=float(r['delta_x_cm']);y=float(r['delta_y_cm']);t=float(r['delta_theta_deg'])
            except (ValueError,TypeError):
                continue
            by[r['mode']].append((x,y,t))
    if not by:
        raise SystemExit('Preencha primeiro as colunas de medição real no CSV')
    for mode, values in sorted(by.items()):
        print(f'\n{mode}: {len(values)} medições')
        for i,label in enumerate(('Δx [cm]','Δy [cm]','Δθ [graus]')):
            series=[row[i] for row in values]
            std=statistics.stdev(series) if len(series)>1 else float('nan')
            print(f'{label}: média={statistics.mean(series):.3f}, DP_amostral={std:.3f}')

if __name__=='__main__': main()
