from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area


def test_area_contains():
    pos = Position(5, 5)
    dim = Dimensions(10, 10)
    area = Area(position=pos, dimensions=dim)
    assert area.contains(Position(10, 10))
    assert not area.contains(Position(16, 16))


def test_area_overlap():
    area1 = Area(0, 0, 10, 10)
    area2 = Area(5, 5, 15, 15)
    overlap_area = area1.overlap(area2)

    assert overlap_area is not None
    assert overlap_area.top == 5
    assert overlap_area.left == 5
    assert overlap_area.bottom == 10
    assert overlap_area.right == 10

    no_overlap_area = Area(20, 20, 30, 30)
    assert area1.overlap(no_overlap_area) is None


def test_area_scale_by():
    area1 = Area(0, 0, 10, 10)
    area2 = Area(0, 0, 20, 20)
    scale_fn = area1.scale_by(area2)

    position = Position(5, 5)
    scaled_position = scale_fn(position)

    assert scaled_position.x == 10
    assert scaled_position.y == 10

    area3 = Area(0, 0, 5, 5)
    scale_fn2 = area1.scale_by(area3)
    scaled_position2 = scale_fn2(position)

    assert scaled_position2.x == 2.5
    assert scaled_position2.y == 2.5
