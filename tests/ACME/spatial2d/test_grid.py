from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.cell import Cell
from cnegng.ACME.spatial2d.grid import Grid


def test_grid_cell_for():
    area = Area(position=Position(0, 0), dimensions=Dimensions(100, 100))
    grid = Grid(area, Dimensions(10, 10))
    cell = grid.cell_for(Position(50, 50))
    assert isinstance(cell, Cell)
    assert cell is grid.cells[55]
