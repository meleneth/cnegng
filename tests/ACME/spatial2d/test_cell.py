from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.cell import Cell


def test_cell_creation():
    area = Area(position=Position(0, 0), dimensions=Dimensions(100, 100))
    cell = Cell(area)
    assert isinstance(cell.inmates, list)
    assert len(cell.inmates) == 0
