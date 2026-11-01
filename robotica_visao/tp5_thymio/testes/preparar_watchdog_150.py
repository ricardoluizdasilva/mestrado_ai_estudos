"""Gera watchdog_joystick_150.asm a partir do watchdog_motores.asm validado.
Nao envia comandos ao Thymio. Nao substitui o ficheiro original.
"""
from pathlib import Path
import re

base = Path(__file__).resolve().parent.parent
origem = base / 'src' / 'aseba' / 'watchdog_motores.asm'
destino = base / 'src' / 'aseba' / 'watchdog_joystick_150.asm'
if not origem.is_file():
    raise SystemExit(f'Ficheiro ausente: {origem}')
if destino.exists():
    raise SystemExit(f'Destino ja existe; nao substitui: {destino}')
s = origem.read_text(encoding='utf-8')
i = s.index('limitar_esquerdo:')
j = s.index('diagnostico:', i)
parte = s[i:j]
parte, np = re.subn(r'(?m)^(\s*push\.s\s+)20(\s*(?:;.*)?)$',r'\g<1>150\g<2>',parte)
parte, nn = re.subn(r'(?m)^(\s*push\.s\s+)-20(\s*(?:;.*)?)$',r'\g<1>-150\g<2>',parte)
if (np,nn)!=(4,4):
    raise SystemExit(f'Estrutura inesperada: +20={np}, -20={nn}. Nada foi criado.')
destino.write_text(s[:i]+parte+s[j:], encoding='utf-8')
print('Gerado:',destino)
print('Alteracoes: +20->+150 (4); -20->-150 (4). Validar compilacao Aseba antes de usar.')
