import math
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from odometria import Pose,L_CM,wrap_angle

class TestOdometria(unittest.TestCase):
    def test_forward(self):
        p=Pose().update_distances(10,10)
        self.assertAlmostEqual(p.x_cm,10)
        self.assertAlmostEqual(p.y_cm,0)
        self.assertAlmostEqual(p.theta_rad,0)
    def test_pure_rotation(self):
        p=Pose().update_distances(-L_CM/2,L_CM/2)
        self.assertAlmostEqual(p.x_cm,0)
        self.assertAlmostEqual(p.y_cm,0)
        self.assertAlmostEqual(p.theta_rad,1)
    def test_left_turn(self):
        p=Pose().update_distances(2,4)
        self.assertGreater(p.y_cm,0)
        self.assertGreater(p.theta_rad,0)
    def test_right_turn(self):
        p=Pose().update_distances(4,2)
        self.assertLess(p.y_cm,0)
        self.assertLess(p.theta_rad,0)
    def test_wrap(self):
        self.assertAlmostEqual(wrap_angle(2*math.pi+0.1),0.1)

if __name__=='__main__': unittest.main()
