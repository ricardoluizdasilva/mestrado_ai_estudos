"""TP5: P/PI/PID externo com feedforward, derivada filtrada e CSV único."""
import argparse
import csv
import math
import time
from datetime import datetime
from pathlib import Path
from thymio_common import connect_robot, shutdown_robot

ROOT = Path(__file__).resolve().parent.parent


def clamp(x, a, b):
    return max(a, min(b, x))


class PID:
    def __init__(self, kp, ki, kd, tau=0.3, limit=100, int_limit=100):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.tau, self.limit, self.int_limit = tau, limit, int_limit
        self.integral = 0.0
        self.prev_measurement = None
        self.derivative = 0.0

    def step(self, ref, measured, dt):
        error = ref - measured
        if self.prev_measurement is None or dt <= 0:
            raw_d = 0.0
        else:
            raw_d = -(measured - self.prev_measurement) / dt
        self.prev_measurement = measured
        alpha = dt / (self.tau + dt) if dt > 0 else 0.0
        self.derivative += alpha * (raw_d - self.derivative)
        # Anti-windup condicional: não integrar quando a saturação pioraria.
        candidate = clamp(self.integral + error * dt, -self.int_limit, self.int_limit)
        raw = ref + self.kp * error + self.ki * candidate + self.kd * self.derivative
        if not ((raw > self.limit and error > 0) or (raw < -self.limit and error < 0)):
            self.integral = candidate
        output = ref + self.kp * error + self.ki * self.integral + self.kd * self.derivative
        return int(round(clamp(output, -self.limit, self.limit))), error, self.derivative


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--porta', default='/dev/ttyACM0')
    ap.add_argument('--ref', type=int, default=50)
    ap.add_argument('--duracao', type=float, default=4.0)
    ap.add_argument('--dt', type=float, default=0.2)
    ap.add_argument('--kp', type=float, default=0.3)
    ap.add_argument('--ki', type=float, default=0.05)
    ap.add_argument('--kd', type=float, default=0.01)
    ap.add_argument('--tau', type=float, default=0.3)
    ap.add_argument('--limite', type=int, default=100)
    args = ap.parse_args()
    if not (0.05 <= args.dt <= 1 and 0 < args.duracao <= 10 and 0 <= args.ref <= 80):
        ap.error('Use dt 0,05–1 s, duração 0–10 s e referência 0–80.')
    if not all(math.isfinite(x) and x >= 0 for x in [args.kp, args.ki, args.kd, args.tau]):
        ap.error('Ganhos/tau devem ser finitos e não negativos.')
    if not 1 <= args.limite <= 100:
        ap.error('Limite deve estar entre 1 e 100.')
    results_dir = ROOT / 'resultados'
    results_dir.mkdir(exist_ok=True, parents=True)
    label = 'P' if args.ki == args.kd == 0 else 'PI' if args.kd == 0 else 'PID'
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    out = results_dir / f'{stamp}_{label}_kp{args.kp:g}_ki{args.ki:g}_kd{args.kd:g}.csv'
    th = node_id = None
    rows = []
    left_pid = PID(args.kp, args.ki, args.kd, args.tau, args.limite)
    right_pid = PID(args.kp, args.ki, args.kd, args.tau, args.limite)
    try:
        print('A verificar a porta e a ligar ao Thymio...')
        th, node_id = connect_robot(args.porta)
        robot = th[node_id]
        robot['motor.left.target'] = robot['motor.right.target'] = 0
        time.sleep(0.5)
        print(f'Conectado: {node_id} | {label}: kp={args.kp} ki={args.ki} kd={args.kd}')
        start = time.monotonic()
        prev = start
        index = 0
        while True:
            deadline = start + index * args.dt
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(remaining)
            now = time.monotonic()
            elapsed = now - start
            if elapsed >= args.duracao:
                break
            actual_dt = max(now - prev, 0.001)
            prev = now
            vl = int(robot['motor.left.speed'])
            vr = int(robot['motor.right.speed'])
            ul, el, dl = left_pid.step(args.ref, vl, actual_dt)
            ur, er, dr = right_pid.step(args.ref, vr, actual_dt)
            robot['motor.left.target'] = ul
            robot['motor.right.target'] = ur
            rows.append(dict(tempo=round(elapsed, 4), dt=round(actual_dt, 4), referencia=args.ref,
                             velocidade_esquerda=vl, velocidade_direita=vr,
                             erro_esquerdo=el, erro_direito=er,
                             comando_esquerdo=ul, comando_direito=ur,
                             derivada_esquerda=round(dl, 4), derivada_direita=round(dr, 4),
                             kp=args.kp, ki=args.ki, kd=args.kd, tau=args.tau))
            print(f't={elapsed:4.1f}s | L={vl:4d} R={vr:4d} | uL={ul:4d} uR={ur:4d}')
            index += 1
    finally:
        shutdown_robot(th, node_id)
        if rows:
            with out.open('x', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            print('CSV:', out)


if __name__ == '__main__':
    main()
