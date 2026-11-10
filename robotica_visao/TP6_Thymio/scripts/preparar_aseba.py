"""Preparar código Aseba com ganho medido, sem o carregar no robô."""
import argparse
from pathlib import Path
from odometria import read_calibration

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--calibracao',required=True)
    a.add_argument('--template',default='aseba/odometria_embarcada_template.aesl')
    a.add_argument('--saida',default='resultados/odometria_embarcada_calibrada.aesl')
    args=a.parse_args()
    kl,kr=read_calibration(args.calibracao)
    if abs(kl-kr)>1e-9:
        raise ValueError('O protótipo embarcado usa ganho comum; calibrar ou reconciliar ganhos por roda antes.')
    kd=int(round(kl*1000))
    if kd <= 0:
        raise ValueError('Ganho insuficiente para representação inteira')
    path=Path(args.template)
    text=path.read_text(encoding='utf-8')
    if text.count('__KD_MILLI__')!=2:
        raise ValueError('Marcador de ganho inesperado no template')
    text=text.replace('var odo_kd_milli = __KD_MILLI__', f'var odo_kd_milli = {kd}')
    # substitui também a referência no comentário, para não deixar marcadores
    text=text.replace('# __KD_MILLI__:', '# KD_MILLI:')
    out=Path(args.saida);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(text,encoding='utf-8')
    print('Programa Aseba preparado (NÃO carregado):',out)
    print('Kd experimental=',kl,'-> inteiro de calibração=',kd)
    print('VALIDAÇÃO EM ASEBA STUDIO / COMPILADOR AINDA NECESSÁRIA')

if __name__=='__main__':main()
