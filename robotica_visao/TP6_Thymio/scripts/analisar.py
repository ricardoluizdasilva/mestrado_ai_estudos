"""TP6 Q5/Q6/Q2b/Q3: integrar velocidades, comparar pose medida e resumos."""
import argparse
import json
import math
from odometria import integrate_log, compare_manual, summarize_repetitions


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--log',help='CSV com velocidades reais recolhidas')
    ap.add_argument('--calibracao',required=True)
    ap.add_argument('--saida',default='resultados/odometria.csv')
    ap.add_argument('--medicoes-manuais',help='CSV de medidas manuais para comparar')
    args=ap.parse_args()
    if args.log:
        pose=integrate_log(args.log,args.calibracao,args.saida)
        print(f"Pose final: x={pose.x_cm:.3f} cm, y={pose.y_cm:.3f} cm, θ={math.degrees(pose.theta_rad):.3f}°")
        print('Trajetória:',args.saida)
    if args.medicoes_manuais:
        target='resultados/comparacao_pose.csv'
        compared=compare_manual(args.medicoes_manuais,args.calibracao,target)
        print('Comparações:',len(compared),target)
        print(json.dumps(summarize_repetitions(compared),ensure_ascii=False,indent=2))
    if not args.log and not args.medicoes_manuais:
        ap.error('Indique --log e/ou --medicoes-manuais')

if __name__=='__main__':main()
