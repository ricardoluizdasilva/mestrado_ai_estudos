"""TP6: geometria diferencial, integração de 2.ª ordem e avaliação da pose.
Unidades: cm, s, rad; Kd: cm/(s * unidade de motor.left/right.speed).
Não controla hardware. Compatível com Python 3.10+.
"""
from __future__ import annotations
import csv
import json
import math
import statistics
from dataclasses import dataclass
from pathlib import Path

L_CM = 9.35
WHEEL_RADIUS_CM = 2.2


def wrap_angle(rad: float) -> float:
    return (rad + math.pi) % (2 * math.pi) - math.pi


@dataclass
class Pose:
    x_cm: float = 0.0
    y_cm: float = 0.0
    theta_rad: float = 0.0  # contínuo, sem wrap

    def update_distances(self, dl_cm: float, dr_cm: float, wheelbase_cm: float = L_CM) -> "Pose":
        if wheelbase_cm <= 0:
            raise ValueError("wheelbase_cm deve ser positivo")
        ds = (dl_cm + dr_cm) / 2.0
        dtheta = (dr_cm - dl_cm) / wheelbase_cm
        mid = self.theta_rad + dtheta / 2.0
        self.x_cm += ds * math.cos(mid)
        self.y_cm += ds * math.sin(mid)
        self.theta_rad += dtheta
        return self

    def update_speeds(self, speed_left: float, speed_right: float, dt_s: float,
                      kd_left: float, kd_right: float, wheelbase_cm: float = L_CM) -> "Pose":
        if dt_s < 0:
            raise ValueError("dt_s negativo")
        return self.update_distances(speed_left * kd_left * dt_s,
                                     speed_right * kd_right * dt_s, wheelbase_cm)


def read_calibration(path: str | Path) -> tuple[float, float]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    kd_l = float(obj.get("kd_left", obj.get("kd", 0)))
    kd_r = float(obj.get("kd_right", obj.get("kd", 0)))
    if not (0 < kd_l < 0.3 and 0 < kd_r < 0.3):
        raise ValueError("Coeficientes Kd não calibrados ou implausíveis; não usar dados simulados")
    return kd_l, kd_r


def integrate_log(logfile: str | Path, calibration: str | Path,
                  output_csv: str | Path | None = None, wheelbase_cm: float = L_CM) -> Pose:
    kl, kr = read_calibration(calibration)
    with Path(logfile).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("Registo sem amostras")
    pose = Pose()
    result = []
    for row in rows:
        dt = float(row['dt_s'])
        vl = float(row['speed_left'])
        vr = float(row['speed_right'])
        dl = kl * vl * dt
        dr = kr * vr * dt
        pose.update_distances(dl, dr, wheelbase_cm)
        result.append({"time_s": row['time_s'], "dt_s": dt,
                       "speed_left": vl, "speed_right": vr,
                       "dl_cm": f"{dl:.6f}", "dr_cm": f"{dr:.6f}",
                       "x_cm": f"{pose.x_cm:.6f}", "y_cm": f"{pose.y_cm:.6f}",
                       "theta_rad": f"{pose.theta_rad:.6f}",
                       "theta_deg": f"{math.degrees(pose.theta_rad):.4f}"})
    if output_csv:
        p = Path(output_csv)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, result[0].keys())
            w.writeheader()
            w.writerows(result)
    return pose


def compare_manual(manual_csv: str | Path, calibration: str | Path,
                   output_csv: str | Path) -> list[dict]:
    with Path(manual_csv).open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    result = []
    for r in rows:
        if not r.get('log_file') or not r.get('delta_x_cm') or not r.get('delta_y_cm') or not r.get('delta_theta_deg'):
            continue
        pose = integrate_log(r['log_file'], calibration)
        x, y, a = float(r['delta_x_cm']), float(r['delta_y_cm']), float(r['delta_theta_deg'])
        theta_err = math.degrees(wrap_angle(pose.theta_rad - math.radians(a)))
        result.append({"run_id": r.get('run_id',''), "mode": r.get('mode',''),
                       "x_measured_cm": x, "y_measured_cm": y, "theta_measured_deg": a,
                       "x_odo_cm": round(pose.x_cm,4), "y_odo_cm": round(pose.y_cm,4),
                       "theta_odo_deg": round(math.degrees(pose.theta_rad),4),
                       "position_error_cm": round(math.hypot(pose.x_cm-x, pose.y_cm-y),4),
                       "heading_error_deg": round(theta_err,4)})
    if result:
        p=Path(output_csv); p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,result[0].keys());w.writeheader();w.writerows(result)
    return result


def summarize_repetitions(rows: list[dict]) -> dict:
    summary = {}
    for mode in sorted(set(r['mode'] for r in rows)):
        subset = [r for r in rows if r['mode'] == mode]
        summary[mode] = {}
        for key in ('x_measured_cm','y_measured_cm','theta_measured_deg','position_error_cm','heading_error_deg'):
            values = [float(r[key]) for r in subset]
            summary[mode][key] = {"n": len(values), "mean": statistics.mean(values),
                                   "std_sample": statistics.stdev(values) if len(values)>=2 else None}
    return summary
