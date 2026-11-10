"""TP6 Q9 (extra): correção OFFLINE pela pose conhecida num canto.
Não deteta o canto automaticamente. O instante de contacto e a pose do canto
são fornecidos pelo experimentador após medição.
"""
import argparse
import csv
import math
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--trajetoria',required=True)
    p.add_argument('--tempo-marco',type=float,required=True)
    p.add_argument('--x-marco',type=float,required=True)
    p.add_argument('--y-marco',type=float,required=True)
    p.add_argument('--theta-marco-deg',type=float,required=True)
    p.add_argument('--saida',default='resultados/trajetoria_corrigida.csv')
    a=p.parse_args()
    with open(a.trajetoria,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise ValueError('Trajetória vazia')
    idx=min(range(len(rows)),key=lambda i:abs(float(rows[i]['time_s'])-a.tempo_marco))
    ref=rows[idx]
    xr=float(ref['x_cm']);yr=float(ref['y_cm']);ang=float(ref['theta_rad'])
    target=math.radians(a.theta_marco_deg)
    delta=target-ang
    c,s=math.cos(delta),math.sin(delta)
    output=[]
    for i,r in enumerate(rows):
        data=dict(r)
        if i>=idx:
            dx=float(r['x_cm'])-xr;dy=float(r['y_cm'])-yr
            x=a.x_marco+c*dx-s*dy
            y=a.y_marco+s*dx+c*dy
            theta=float(r['theta_rad'])+delta
        else:
            x=float(r['x_cm']);y=float(r['y_cm']);theta=float(r['theta_rad'])
        data.update(x_corrigido_cm=round(x,5),y_corrigido_cm=round(y,5),
                    theta_corrigido_deg=round(math.degrees(theta),4),
                    marco_aplicado=i>=idx)
        output.append(data)
    out=Path(a.saida);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,output[0].keys());w.writeheader();w.writerows(output)
    print('Marco associado à amostra',idx,'t=',ref['time_s'])
    print('Trajetória corrigida:',out)
    print('NOTA: correção com pose de canto fornecida manualmente; não é localização automática.')

if __name__=='__main__':main()
