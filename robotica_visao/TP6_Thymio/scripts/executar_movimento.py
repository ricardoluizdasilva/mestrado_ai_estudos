"""TP6: Q1/Q4 e extra Q8. Controlo supervisionado, sem ROS2.
Execução com motores exige --execute; parâmetros conservadores e watchdog por segmento.
Velocidade observada: motor.left.speed/motor.right.speed; os targets não são odometria.
"""
import argparse
import csv
import math
import signal
import time
from datetime import datetime, timezone
from pathlib import Path
from threading import Event

from odometria import L_CM, read_calibration, Pose

PORT_DEFAULT = '/dev/serial/by-id/usb-Mobsya.org_Thymio-II_Wireless_00124B001DF456B0-if00'
EXPECTED_NODE = 58360


def scalar(value):
    if isinstance(value, (list,tuple)):
        return float(value[0])
    return float(value)


def stop_motors(node):
    node['motor.left.target'] = 0
    node['motor.right.target'] = 0


def main():
    ap=argparse.ArgumentParser(description='Movimentos TP6 com registo velocidades reais; exige --execute')
    ap.add_argument('--mode',choices=['left','right','straight','square'],default='left')
    ap.add_argument('--left',type=int,default=80)
    ap.add_argument('--right',type=int,default=120)
    ap.add_argument('--duration',type=float,default=2.0)
    ap.add_argument('--side-cm',type=float,default=15.0)
    ap.add_argument('--speed',type=int,default=110)
    ap.add_argument('--turn-speed',type=int,default=80)
    ap.add_argument('--calibration',help='Ficheiro JSON com Kd experimental, obrigatório para square')
    ap.add_argument('--port',default=PORT_DEFAULT)
    ap.add_argument('--output',default='resultados/velocidades_tp6.csv')
    ap.add_argument('--execute',action='store_true',help='Autorizar movimento real')
    args=ap.parse_args()

    if args.duration <= 0 or args.duration > 3.0:
        ap.error('Para ensaios individuais, duração deve estar entre 0 e 3 segundos')
    if max(abs(args.left),abs(args.right),abs(args.speed),abs(args.turn_speed)) > 200:
        ap.error('Limite conservador: velocidades de motor até 200 unidades')
    if args.mode=='left' and not 0 <= args.left < args.right:
        ap.error('Curva esquerda suave exige 0 <= left < right')
    if args.mode=='right' and not 0 <= args.right < args.left:
        ap.error('Curva direita exige 0 <= right < left')
    if args.mode=='straight' and args.left != args.right:
        ap.error('Para reta, --left e --right devem coincidir')
    if args.mode=='square' and not 5 <= args.side_cm <= 20:
        ap.error('Lado do quadrado limitado a 5–20 cm por segurança')

    commands=[]
    if args.mode=='square':
        if not args.calibration:
            ap.error('Para o quadrado, primeiro medir Kd e indicar --calibration')
        kl,kr=read_calibration(args.calibration)
        kv=(kl+kr)/2
        linear_time=args.side_cm/(args.speed*kv)
        turn_time=(L_CM*math.pi/4)/(args.turn_speed*kv)
        if max(linear_time,turn_time)>6:
            ap.error('Segmento maior que 6s. Ajustar velocidade/tamanho do lado ou calibração.')
        for i in range(4):
            commands.extend([(f'aresta_{i+1}',args.speed,args.speed,linear_time),
                             (f'rotacao_{i+1}',-args.turn_speed,args.turn_speed,turn_time)])
    else:
        commands=[(args.mode,args.left,args.right,args.duration)]

    print('=== TP6: PLANO DE MOVIMENTO ===')
    for name,l,r,d in commands:
        print(f'{name}: left={l}, right={r}, duração={d:.3f}s')
    if not args.execute:
        print('SIMULAÇÃO DO PLANO: nenhum comando enviado aos motores. Use --execute quando estiver seguro.')
        return

    from thymiodirect import Thymio
    from thymio_shutdown import encerrar
    kl,kr=read_calibration(args.calibration) if args.calibration else (None,None)
    pose=Pose()
    def on_term(_sig, _frame):
        raise KeyboardInterrupt('SIGTERM recebido: solicitar paragem segura')
    signal.signal(signal.SIGTERM, on_term)
    fault = Event()
    print('SEGURANÇA: piso desimpedido, robô no chão, supervisão contínua.')
    print('Movimento inicia após 3 segundos; Ctrl+C solicita paragem.')
    time.sleep(3)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    robot=Thymio(serial_port=args.port,refreshing_rate=0.05,
                 refreshing_coverage={'motor.left.speed','motor.right.speed'},
                 on_connect=lambda node_id:print('Thymio conectado:',node_id,flush=True),
                 on_disconnect=lambda node_id:fault.set(),
                 on_comm_error=lambda err:(print('ERRO COMUNICAÇÃO:',repr(err),flush=True),fault.set()))
    node_id=None
    rows=[]
    started=time.monotonic()
    try:
        print('A estabelecer comunicação...',flush=True)
        robot.connect() # pode bloquear: executar com watchdog externo só quando parado
        node_id=robot.first_node()
        if node_id != EXPECTED_NODE:
            raise RuntimeError(f'Nó inesperado: {node_id}; esperado {EXPECTED_NODE}')
        node=robot[node_id]
        stop_motors(node)
        time.sleep(0.3)
        for segment,left,right,duration in commands:
            print('Início:',segment,flush=True)
            node['motor.left.target']=left
            node['motor.right.target']=right
            last=time.monotonic()
            end=last+duration
            while True:
                if fault.is_set():
                    raise RuntimeError('Ligação perdida/erro de comunicação; abortar movimento')
                now=time.monotonic()
                if now>=end:
                    break
                time.sleep(min(0.05,end-now))
                now=time.monotonic()
                dl=now-last
                last=now
                vl=scalar(node['motor.left.speed'])
                vr=scalar(node['motor.right.speed'])
                if kl is not None:
                    pose.update_speeds(vl,vr,dl,kl,kr)
                rows.append({'x_odo_cm':round(pose.x_cm,6) if kl is not None else '',
                             'y_odo_cm':round(pose.y_cm,6) if kl is not None else '',
                             'theta_odo_deg':round(math.degrees(pose.theta_rad),6) if kl is not None else '',
                             'timestamp_utc':datetime.now(timezone.utc).isoformat(),
                             'time_s':round(now-started,6), 'dt_s':round(dl,6),
                             'segment':segment,'target_left':left,'target_right':right,
                             'speed_left':vl,'speed_right':vr})
            stop_motors(node)
            time.sleep(0.4)  # margem de travagem; não inclui coasting na odometria
            print('Fim:',segment,'amostras:',len(rows),flush=True)
    finally:
        if node_id is not None:
            try:
                stop_motors(robot[node_id])
            except Exception as exc:
                print('AVISO: não foi possível confirmar paragem dos motores:',repr(exc),flush=True)
        with out.open('w',newline='',encoding='utf-8') as f:
            cols=['timestamp_utc','time_s','dt_s','segment','target_left','target_right','speed_left','speed_right','x_odo_cm','y_odo_cm','theta_odo_deg']
            w=csv.DictWriter(f,fieldnames=cols); w.writeheader();w.writerows(rows)
        print('Registo:',out,'amostras:',len(rows),flush=True)
        encerrar(robot,node_id)

if __name__=='__main__':
    main()
