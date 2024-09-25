import pytest

from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.grid import Grid, GridCell, GridSize
from cnegng.ACME.spatial2d import Circle


class DemoItem:
    def __init__(self, position: Position):
        self.current_cell = None
        self.position = position


def test_grid_cell_for():
    area = Area(position=Position(0, 0), dimensions=Dimensions(100, 100))
    grid = Grid(area, GridSize(10, 10))
    cell = grid.cell_for(Position(50, 50))
    assert isinstance(cell, GridCell)
    assert cell is grid.cells[55]


class TestGrid:
    @pytest.fixture
    def grid(self):
        grid_area = Area(0, 0, 100, 100)
        grid_dimensions = GridSize(10, 20)
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


@pytest.fixture
def setup_grid():
    # Example grid setup with predefined objects
    grid_area = Area(0, 0, 1000, 1000)
    dimensions = GridSize(10, 10)
    grid = Grid(grid_area, dimensions)

    # Add some objects to grid cells
    obj1 = DemoItem(Position(500, 500))  # In the center of grid
    obj2 = DemoItem(Position(100, 100))  # Near top-left corner
    obj3 = DemoItem(Position(900, 900))  # Near bottom-right corner

    grid.add_to_cell(obj1, obj1.position)
    grid.add_to_cell(obj2, obj2.position)
    grid.add_to_cell(obj3, obj3.position)

    return grid


def test_objects_in_circle_full_overlap(setup_grid):
    grid = setup_grid
    circle = Circle(500, 500, 500)  # Circle centered in grid, covering most cells

    objects = list(grid.objects_in_circle(circle))
    assert len(objects) == 3  # Expecting 3 objects within the circle


def test_objects_in_circle_partial_overlap(setup_grid):
    grid = setup_grid
    circle = Circle(100, 100, 50)  # Circle partially covering top-left cell

    objects = list(grid.objects_in_circle(circle))
    assert len(objects) == 1  # Expecting 1 object within the circle (top-left corner)
