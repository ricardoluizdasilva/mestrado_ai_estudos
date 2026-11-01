"""Pré-teste sem movimento. Verifica série, ligação e feedback do robô."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
from thymio_common import connect_robot, shutdown_robot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--porta', default='/dev/ttyACM0')
    args = parser.parse_args()
    th, node_id = None, None
    try:
        th, node_id = connect_robot(args.porta)
        robot = th[node_id]
        print('ID:', node_id)
        print('Proximidade:', robot['prox.horizontal'])
        print('Motor esquerdo:', robot['motor.left.speed'])
        print('Motor direito:', robot['motor.right.speed'])
        print('PREFLIGHT OK')
    except Exception as exc:
        print(f'PREFLIGHT FALHOU: {exc}', file=sys.stderr)
        return 1
    finally:
        shutdown_robot(th, node_id)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
