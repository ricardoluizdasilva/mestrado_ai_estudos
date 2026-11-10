"""TP6 Exercício 9 — quadrado V4.2 e correção por pose externa medida.

O robô move-se apenas depois de confirmação explícita INICIAR.
A medição de pose é solicitada após concluir os quatro lados e parar.
Requer Thymio supervisionado, espaço livre e TDM em 127.0.0.1:8596.
"""
import csv
import json
import math
import select
import sys
import time
from datetime import datetime
from pathlib import Path
from tdmclient import ClientAsync

BASE = Path('resultados/validacao_v45')
ASEBA = Path('aseba/odometria_embarcada_v45_calibrada.aesl')
NODE_ID = 'd2e63ca0-00fa-4913-b67b-563cc7c73352'
FIELDS = ('odo_x_coarse','odo_x_rem','odo_y_coarse','odo_y_rem','odo_theta_b','odo_turns')
REF = ('corr_ref_x_coarse','corr_ref_x_rem','corr_ref_y_coarse','corr_ref_y_rem','corr_ref_theta_b','corr_ref_turns')
PRE = ('corr_pre_x_coarse','corr_pre_x_rem','corr_pre_y_coarse','corr_pre_y_rem','corr_pre_theta_b','corr_pre_turns')
WATCH = set(FIELDS+REF+PRE) | {'seq_state','seq_fault','seq_side','seq_arm','seq_request','seq_abort','corr_request','corr_applied','corr_rejected','corr_status','motor.left.target','motor.right.target','motor.left.speed','motor.right.speed'}

def value(node, name):
    v = node.v
    for part in name.split('.'):
        v = getattr(v, part)
    return int(v) if isinstance(v, (int, float)) else None

def values(node, fields):
    r = tuple(value(node,k) for k in fields)
    return r if all(v is not None for v in r) else None

def pose_from(raw):
    x, xr, y, yr, t, turns = raw
    return {'x_cm': (10*x+xr)/1000, 'y_cm': (10*y+yr)/1000,
            'theta_graus': (t+65536*turns)*180/32768}

def xyz_to_aseba(x,y,theta):
    def encode_cm(cm):
        unit = round(cm*1000)  # 0.01 mm
        c = math.trunc(unit/10)
        return c, unit-10*c
    xc,xr=encode_cm(x); yc,yr=encode_cm(y)
    turns=math.floor((theta+180)/360)
    norm=theta-360*turns
    ab=round(norm*32768/180)
    if ab==32768: ab=-32768; turns+=1
    nums=(xc,xr,yc,yr,ab,turns)
    if not all(-32768<=z<=32767 for z in nums):
        raise ValueError('Pose excede a representacao int16')
    return nums

async def until(client, pred, seconds, msg):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        await client.sleep(0.1)
        if pred(): return
    raise TimeoutError(msg)

async def ask(client,prompt):
    """Lê stdin sem bloquear o processamento da comunicação TDM."""
    print(prompt, end='', flush=True)
    while True:
        if select.select([sys.stdin],[],[],0)[0]:
            line=sys.stdin.readline()
            if not line: raise EOFError('Entrada encerrada; sem correcao')
            return line.strip()
        await client.sleep(0.1)

def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False), encoding='utf-8')

async def set_and_confirm(node,client,dictvalues):
    result=await node.set_variables({k:[v] for k,v in dictvalues.items()})
    if result is not None: raise RuntimeError(f'Falha escrita TDM: {result}')
    await until(client,lambda: all(value(node,k)==v for k,v in dictvalues.items()),5,'Variáveis escritas não confirmadas')

async def run(client):
    n=await client.wait_for_node()
    if n.id_str!=NODE_ID: raise RuntimeError('ID do Thymio não corresponde ao esperado')
    await n.lock()
    started=False
    trace=[]
    report={'tipo':'ensaio_fisico_com_correcao_v42','instante':datetime.now().isoformat(),
            'correcao_aplicada':False,'fonte_referencia':'medicao_manual_externa'}
    try:
        await n.set_variables({'motor.left.target':[0],'motor.right.target':[0]})
        code=ASEBA.read_text(encoding='utf-8')
        result=await n.compile(code)
        if result is not None: raise RuntimeError(f'Falha de compilação: {result}')
        await n.watch(variables=True)
        # Bloquear qualquer pedido de movimento até confirmação explícita.
        await n.set_variables({'seq_arm':[0],'seq_request':[0],'seq_abort':[0],'corr_request':[0]})
        result=await n.run(); started=True
        if result is not None: raise RuntimeError(f'Falha a iniciar: {result}')
        await n.wait_for_variables(WATCH)
        await until(client,lambda: all(value(n,k) is not None for k in WATCH),6,'Variáveis ainda indisponíveis')
        if value(n,'seq_state')!=0 or value(n,'seq_fault')!=0 or value(n,'seq_arm')!=0 or value(n,'seq_request')!=0:
            raise RuntimeError('Estado inicial inseguro')
        if any(value(n,k)!=0 for k in ('motor.left.target','motor.right.target')):
            raise RuntimeError('Motores com comando inesperado')
        print('\nV4.2 carregada. Estado 0, comandos de motor 0.')
        confirm=await ask(client,'Confirme robot alinhado, espaço livre e supervisão. Escreva INICIAR: ')
        if confirm!='INICIAR':
            print('Ensaio cancelado.'); return
        await set_and_confirm(n,client,{'seq_arm':1})
        await n.set_variables({'seq_request':[1]})
        await until(client,lambda: value(n,'seq_state') in (1,2,3,4,5,6),5,
                    'Pedido de início não aceite')
        print('Trajetória iniciada — pode interromper fisicamente o robô.')
        last_state=None; last_record=0
        start=time.monotonic()
        while time.monotonic()-start<85:
            await client.sleep(0.1)
            s=value(n,'seq_state'); fault=value(n,'seq_fault')
            if s is None: continue
            if s!=last_state:
                print(f'Estado {s} | lado {value(n,"seq_side")} | falha {fault}',flush=True)
                last_state=s
            if time.monotonic()-last_record>=0.5:
                raw=values(n,FIELDS)
                if raw:
                    trace.append({'tempo_s':round(time.monotonic()-start,2), 'estado':s,
                                  'lado':value(n,'seq_side'),**pose_from(raw)})
                last_record=time.monotonic()
            if s==6 or (fault is not None and fault!=0):
                raise RuntimeError(f'Falha embarcada, estado={s}, fault={fault}')
            if s==5:
                break
        else:
            await n.set_variables({'seq_abort':[1], 'motor.left.target':[0],'motor.right.target':[0]})
            raise TimeoutError('Trajetória excedeu 85 segundos')
        await until(client,lambda: all(value(n,k)==0 for k in ('motor.left.target','motor.right.target'))
                    and all(value(n,k) is not None and abs(value(n,k))<=2
                            for k in ('motor.left.speed','motor.right.speed')),6,
                    'Robô ainda não parado')
        await client.sleep(0.4)
        raw=values(n,FIELDS)
        if raw is None: raise RuntimeError('Pose final não disponível')
        report['odometria_pre_correcao']=pose_from(raw)
        report['estado_final']=value(n,'seq_state')
        report['lados']=value(n,'seq_side')
        print('\nQUADRADO CONCLUÍDO. NÃO DESLOQUE O ROBÔ.')
        print('Odometria pré-correção:',report['odometria_pre_correcao'])
        save_json(report,BASE/'ensaio_v45_parcial.json')
        # Guardar trajetória antes de solicitar as medições.
        csvpath=BASE/'trajetoria_v45.csv'
        with csvpath.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=['tempo_s','estado','lado','x_cm','y_cm','theta_graus'])
            w.writeheader(); w.writerows(trace)
        print('Trajetória guardada:',csvpath)
        print('Meça X e Y com sinais e o desvio angular assinado relativo à orientação inicial.')
        print('A pose será corrigida para theta=360° + desvio angular.')
        measures=[]
        for name,unit in [('X','cm'),('Y','cm'),('desvio angular','graus')]:
            s=await ask(client,f'{name} ({unit}, com sinal; Enter cancela): ')
            if not s:
                print('Correção cancelada; trajetória preservada.'); return
            measures.append(float(s.replace(',','.')))
        x,y,da=measures
        if not (-100<=x<=100 and -100<=y<=100 and -180<=da<=180):
            raise ValueError('Medição fora dos limites de segurança do ensaio')
        theta=360+da
        ref=xyz_to_aseba(x,y,theta)
        report['medicao_externa']={'x_cm':x,'y_cm':y,'desvio_angular_graus':da,'theta_global_graus':theta}
        report['referencia_aseba']=dict(zip(REF,ref))
        save_json(report,BASE/'ensaio_v45_parcial.json')
        response=await ask(client,'Confirmar a aplicação desta pose física? Escreva CORRIGIR: ')
        if response!='CORRIGIR':
            print('Correção cancelada; dados pré-correção guardados.'); return
        if value(n,'seq_state')!=5 or value(n,'seq_fault')!=0:
            raise RuntimeError('Controlador não está em conclusão segura')
        if any(value(n,k) != 0 for k in ('motor.left.target','motor.right.target')):
            raise RuntimeError('Comandos motores não nulos')
        if any(value(n,k) is None or abs(value(n,k))>2 for k in ('motor.left.speed','motor.right.speed')):
            raise RuntimeError('Rodas não estão imobilizadas')
        await set_and_confirm(n,client,dict(zip(REF,ref)))
        old=value(n,'corr_applied')
        await n.set_variables({'corr_request':[1]})
        await until(client,lambda: value(n,'corr_applied')==old+1 and value(n,'corr_request')==0
                    and value(n,'corr_status')==1 and values(n,FIELDS)==ref,6,
                    'Correção não confirmada')
        report['correcao_aplicada']=True
        report['pose_guardada_embarcada_pre_correcao']=pose_from(values(n,PRE))
        report['pose_corrigida']=pose_from(values(n,FIELDS))
        report['corr_applied']=value(n,'corr_applied')
        report['corr_rejected']=value(n,'corr_rejected')
        save_json(report,BASE/'ensaio_v45_corrigido.json')
        print('\nCORREÇÃO V4.2: OK')
        print('Pose antes:',report['pose_guardada_embarcada_pre_correcao'])
        print('Pose depois:',report['pose_corrigida'])
        print('Evidência:',BASE/'ensaio_v45_corrigido.json')
    finally:
        try:
            await n.set_variables({'motor.left.target':[0],'motor.right.target':[0],'seq_abort':[1]})
            if started: await n.stop()
        finally:
            try: await n.watch(variables=False)
            finally:
                await n.unlock()
                print('Paragem solicitada. Nó desbloqueado.',flush=True)

def main():
    with ClientAsync(tdm_addr='127.0.0.1',tdm_port=8596) as client:
        client.run_async_program(lambda: run(client))

if __name__=='__main__':
    try: main()
    except KeyboardInterrupt:
        print('Interrupção do utilizador. Confirme fisicamente a paragem.'); raise
