"""TP6 Ex9: derive guarded pose correction from validated V3.8.
Never changes V3.8 in place.
"""
from pathlib import Path

SRC = Path('resultados/odometria_embarcada_v38_fisica_4lados.aesl')
DST = Path('aseba/odometria_embarcada_v42_correcao.aesl')

DECLARATIONS = '''# TP6 Ex9 V4.2: external measured pose (signed 16-bit Aseba units)
var corr_request = 0
var corr_applied = 0
var corr_rejected = 0
var corr_status = 0
var corr_ref_x_coarse = 0
var corr_ref_x_rem = 0
var corr_ref_y_coarse = 0
var corr_ref_y_rem = 0
var corr_ref_theta_b = 0
var corr_ref_turns = 0
# Preserve pose before correction for audit
var corr_pre_x_coarse = 0
var corr_pre_x_rem = 0
var corr_pre_y_coarse = 0
var corr_pre_y_rem = 0
var corr_pre_theta_b = 0
var corr_pre_turns = 0

'''

CORRECTION = '''
# V4.2: apply external pose only once the 4-side sequence has finished.
# State 5 means complete, 6 means fault. Never correct on a fault.
if corr_request == 1 then
    if seq_state == 5 and seq_fault == 0 then
        if motor.left.target == 0 and motor.right.target == 0 then
            if motor.left.speed >= -2 and motor.left.speed <= 2 and motor.right.speed >= -2 and motor.right.speed <= 2 then
                corr_pre_x_coarse = odo_x_coarse
                corr_pre_x_rem = odo_x_rem
                corr_pre_y_coarse = odo_y_coarse
                corr_pre_y_rem = odo_y_rem
                corr_pre_theta_b = odo_theta_b
                corr_pre_turns = odo_turns

                odo_x_coarse = corr_ref_x_coarse
                odo_x_rem = corr_ref_x_rem
                odo_y_coarse = corr_ref_y_coarse
                odo_y_rem = corr_ref_y_rem
                odo_x_carry = 0
                odo_y_carry = 0
                odo_x_01mm = odo_x_coarse
                odo_y_01mm = odo_y_coarse
                odo_theta_b = corr_ref_theta_b
                odo_turns = corr_ref_turns

                corr_request = 0
                corr_applied = corr_applied + 1
                corr_status = 1
                # Snapshot is refreshed after the correction.
                odo_snapshot = [odo_ticks, odo_x_01mm, odo_y_01mm, odo_theta_b, motor.left.speed, motor.right.speed]
            end
        end
    else
        # Invalid sequence state: do not change any odometry coordinate.
        corr_request = 0
        corr_rejected = corr_rejected + 1
        corr_status = -1
    end
end
'''

def build(src: Path = SRC, dst: Path = DST) -> Path:
    content = src.read_text(encoding='utf-8')
    anchor = 'timer.period[0] = 100'
    if content.count(anchor) != 1 or content.count('onevent timer0') != 1:
        raise ValueError('Unexpected V3.8 structure; no file written')
    if 'var corr_request' in content:
        raise ValueError('Source already has correction variables')
    if content.count('if seq_state != seq_last_state then') != 1:
        raise ValueError('Missing end-of-event state-history block')
    content = content.replace(anchor, DECLARATIONS + anchor, 1)
    content = content.rstrip() + '\n' + CORRECTION
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise FileExistsError(f'{dst} exists; preserve old version')
    dst.write_text(content, encoding='utf-8')
    print('Created:', dst)
    print('Existing V3.8 preserved; no robot movement executed')
    return dst

if __name__ == '__main__':
    build()
