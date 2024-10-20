import math

from cnegng.ACME.spatial2d.motion import Motion


def test_motion_randomize():
    motion = Motion(0, 0)
    motion.randomize((0, 2 * math.pi), (1, 5))
    assert 0 <= motion.direction <= 2 * math.pi
    assert 1 <= motion.speed <= 5
