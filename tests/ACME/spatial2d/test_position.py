from cnegng.ACME.spatial2d.position import Position


def test_position_randomize():
    pos = Position()
    pos.randomize((0, 10), (0, 10))
    assert 0 <= pos.x <= 10
    assert 0 <= pos.y <= 10
