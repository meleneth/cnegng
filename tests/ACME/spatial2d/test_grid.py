import pytest

from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.grid_cell import GridCell
from cnegng.ACME.spatial2d.grid import Grid


def test_grid_cell_for():
    area = Area(position=Position(0, 0), dimensions=Dimensions(100, 100))
    grid = Grid(area, Dimensions(10, 10))
    cell = grid.cell_for(Position(50, 50))
    assert isinstance(cell, GridCell)
    assert cell is grid.cells[55]

class TestGrid:
    @pytest.fixture
    def grid(self):
        grid_area = Area(0, 0, 100, 100)
        grid_dimensions = Dimensions(10, 20)
        return Grid(grid_area, grid_dimensions)

    def test_cells_in_range(self, grid):
        """Test that cells_in_range correctly yields cells that overlap the given area."""
        target_area = Area(10, 10, 40, 40)
        cells = list(grid.cells_in_range(target_area))

        assert len(cells) > 0
        for cell in cells:
            assert Grid.areas_overlap(cell.area, target_area)

    def test_no_overlap(self, grid):
        """Test that no cells are yielded when the area doesn't overlap with any cells."""
        non_overlapping_area = Area(150, 150, 160, 160)
        cells = list(grid.cells_in_range(non_overlapping_area))
        assert len(cells) == 0
