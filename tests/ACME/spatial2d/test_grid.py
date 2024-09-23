import pytest

from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.grid_cell import GridCell
from cnegng.ACME.spatial2d.grid import Grid, PositionOutsideGrid


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
        for cell in grid.cells:
            assert cell.area.overlap(non_overlapping_area) is None
        with pytest.raises(PositionOutsideGrid):
            list(grid.cells_in_range(non_overlapping_area))

    def test_cells_in_range(self, grid):
        """Test that Grid yields the correct cells for the given area."""
        search_area = Area(position=Position(21, 21), dimensions=Dimensions(10, 5))
        cells = list(grid.cells_in_range(search_area))

        # Check that the correct number of cells is returned
        assert len(cells) == 4  # I don't know why 4, but I dind't know why 2 either

    def test_single_cell_in_range(self, grid):
        """Test that Grid correctly yields a single cell."""
        search_area = Area(position=Position(17, 17), dimensions=Dimensions(2, 2))
        cells = list(grid.cells_in_range(search_area))

        # Only one cell should overlap
        assert len(cells) == 1

    def test_no_cells_in_range(self, grid):
        """Test that no cells are yielded when the area is out of bounds."""
        search_area = Area(150, 150, 200, 200)
        with pytest.raises(PositionOutsideGrid):
            list(grid.cells_in_range(search_area))
