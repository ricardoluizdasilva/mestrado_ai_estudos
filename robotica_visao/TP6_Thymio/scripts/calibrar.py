"""TP6 Q4: calcular Kd experimental com distância manual e velocidades REAIS registadas."""
import argparse
import csv
import json
import statistics
from pathlib import Path


def read_area(logfile):
    with Path(logfile).open(newline='',encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"Registo vazio: {logfile}")
    aleft = sum(float(r['speed_left'])*float(r['dt_s']) for r in rows)
    aright = sum(float(r['speed_right'])*float(r['dt_s']) for r in rows)
    return (aleft + aright)/2.0


def main():
    ap=argparse.ArgumentParser(description='Calibrar motor speeds a partir de deslocamentos reais')
    ap.add_argument('--medicoes',required=True,help='CSV com run_id,log_file,distance_cm; movimentos retos apenas')
    ap.add_argument('--saida',default='resultados/calibracao.json')
    args=ap.parse_args()
    with open(args.medicoes,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    used=[]
    for r in rows:
        if not r.get('log_file') or not r.get('distance_cm'):
            continue
        a=read_area(r['log_file'])
        d=float(r['distance_cm'])
        if abs(a) < 1 or abs(d)<0.1 or a*d<=0:
            raise ValueError(f"Dados inválidos em {r.get('run_id')}: área={a:.2f}, d={d}")
        used.append((a,d,r.get('run_id','')))
    if len(used)<2:
        raise ValueError('Recolha pelo menos duas medições reais para calibrar; recomendam-se cinco')
    gain=sum(a*d for a,d,_ in used)/sum(a*a for a,_,_ in used)
    details=[{"run_id":name,"kd":d/a,"area_speed_dt":a,"distance_cm":d} for a,d,name in used]
    if not 0 < gain < 0.3:
        raise ValueError(f"Kd implausível: {gain}; rever unidades e medições")
    model={"kd_left":gain,"kd_right":gain,"unit":"cm/(s*motor.speed)",
           "source":"experimental, straight runs, least squares through origin",
           "n":len(used),"trials":details}
    out=Path(args.saida);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(model,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Calibração experimental:',out)
    print('Kd =',round(gain,7),'cm/(s·unidade motor.speed)')
    print('Kd individuais:',[round(x['kd'],6) for x in details])
    if len(used)>1:
        print('DP amostral Kd individuais:',round(statistics.stdev(x['kd'] for x in details),7))
    print('NOTA: valores por roda e correções de derrapagem exigem calibração adicional.')

if __name__=='__main__':
    main()
