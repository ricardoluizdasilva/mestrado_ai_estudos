"""Ensaio controlado da v11 SEM filtro Python, APENAS com rodas suspensas.

O programa envia comandos pelos slots do watchdog e verifica se o Aseba
bloqueia independentemente os targets quando existe obstaculo.
"""
import sys
import time
from pathlib import Path

from thymiodirect import Thymio

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'testes'))
from testar_timer_contador import encerrar

ASM = BASE / 'src/aseba/watchdog_obstaculos_v11.asm'
PORTA = '/dev/ttyACM0'
COMANDO = 60  # reduzido para diagnostico, nao 200


def signed16(value):
    n = int(value) & 65535
    return n - 65536 if n >= 32768 else n


def perguntar(msg):
    resposta = input(msg + ' [s/N]: ').strip().lower()
    if resposta != 's':
        raise RuntimeError('Ensaio cancelado pelo operador.')


def etapa(conn, nid, offset, robot, sentido, segundos=2.5):
    seq = 0
    command = COMANDO * sentido
    start = time.monotonic()
    last_print = 0.0
    while time.monotonic() - start < segundos:
        conn.set_variables(nid, offset+4, [command & 65535, command & 65535])
        seq += 1
        conn.set_variables(nid, offset, [seq])
        time.sleep(0.12)
        elapsed = time.monotonic() - start
        if elapsed - last_print >= 0.35:
            last_print = elapsed
            prox = [int(v) for v in robot['prox.horizontal']]
            targets = (signed16(robot['motor.left.target']), signed16(robot['motor.right.target']))
            auth = robot['leds.top'][1]
            print(f'{elapsed:4.1f}s prox={prox} pedido={command}/{command} targets={targets} auth={auth}')
    conn.set_variables(nid, offset+4, [0, 0])
    # Nao renovar heartbeat; expiracao autonomamente em ~0.5 s
    time.sleep(0.8)
    print('Depois de expirar:', tuple(signed16(robot[k]) for k in ('motor.left.target','motor.right.target')))


def main():
    if not ASM.is_file():
        raise FileNotFoundError(ASM)
    print('TESTE EMBARCADO v11 - RODAS SUSPENSAS, FORA DO CHAO')
    print('NAO EXECUTAR com as rodas apoiadas no chao.')
    perguntar('Rodas suspensas, desimpedidas e Thymio ao alcance da mao?')
    th = Thymio(serial_port=PORTA, refreshing_rate=0.1,
                refreshing_coverage={'motor.left.target', 'motor.right.target', 'motor.left.speed', 'motor.right.speed', 'leds.top', 'prox.horizontal'})
    node_id = None
    try:
        th.connect()
        node_id = th.first_node()
        if node_id is None:
            raise RuntimeError('Thymio nao encontrado')
        robot = th[node_id]
        connection = th.thymio_proxy.connection
        offset = connection.remote_nodes[node_id].var_total_size
        if offset + 6 > connection.remote_nodes[node_id].max_var_size:
            raise RuntimeError('Memoria insuficiente')
        robot['motor.left.target'] = 0
        robot['motor.right.target'] = 0
        time.sleep(0.4)
        th.run_asm(node_id, ASM.read_text(encoding='utf-8'))
        time.sleep(0.5)
        print('Assembly carregado.')
        perguntar('Sem objetos na frente, ensaiar AVANCO com rodas suspensas?')
        etapa(connection, node_id, offset, robot, +1)
        perguntar('Colocar objeto OPACO junto ao sensor frontal e ensaiar AVANCO?')
        etapa(connection, node_id, offset, robot, +1)
        perguntar('Retirar objeto frontal e ensaiar RECUO com rodas suspensas?')
        etapa(connection, node_id, offset, robot, -1)
        perguntar('Colocar objeto OPACO junto a um sensor traseiro e ensaiar RECUO?')
        etapa(connection, node_id, offset, robot, -1)
        print('Fim. Esperado: target 0/0 com IR >=2200 na direcao pedida e auth=1.')
    finally:
        if node_id is not None:
            encerrar(th, node_id)
        else:
            try: th.disconnect()
            except Exception: pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupcao manual.')
