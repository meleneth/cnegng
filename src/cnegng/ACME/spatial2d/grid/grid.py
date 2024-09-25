import copy
from collections import defaultdict

from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.grid.grid_indexer import GridIndexer
from cnegng.ACME.spatial2d.grid.collision_query import CollisionQuery
from cnegng.ACME.spatial2d.circle import Circle


class PositionOutsideGrid(Exception):
    pass


class GridSize:
    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError("GridSize must have positive width and height.")
        self.width = width
        self.height = height

    def __repr__(self):
        return f"GridSize(width={self.width}, height={self.height})"

    def clone(self):
        return copy.deepcopy(self)


class GlobalCoord:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"GlobalCoord(x={self.x}, y={self.y})"

    def to_grid_coord(self, grid: "Grid"):
        """Convert a global coordinate to a grid coordinate by dividing by grid size."""
        return GridCoord(
            grid,
            x=int(self.x) // grid.grid_size.width,
            y=int(self.y) // grid.grid_size.height,
        )


class GridCoord:
    def __init__(self, grid: "Grid", x: int, y: int):
        self.grid = grid  # Store a reference to the associated Grid
        self.x = x
        self.y = y

    def __repr__(self):
        return f"GridCoord(grid=Grid({self.grid.grid_size.width}x{self.grid.grid_size.height}), x={self.x}, y={self.y})"

    def to_flat_index(self):
        """Convert the grid coordinates to a flat index using the grid's width."""
        return self.y * self.grid.grid_size.width + self.x

    def to_global_coord(self):
        """Convert this grid coordinate back to a global coordinate using the grid's dimensions."""
        return GlobalCoord(
            self.x * self.grid.cell_width, self.y * self.grid.cell_height
        )


class Grid:
    def __init__(self, area: Area, grid_size: GridSize):
        self.area = area.clone()
        self.grid_size = grid_size.clone()
        self.cell_width = area.width / grid_size.width
        self.cell_height = area.height / grid_size.height

        self.indexer = GridIndexer(
            grid_size.width,
            grid_size.height,
            area.width / grid_size.width,
            area.height / grid_size.height,
        )
        self.cells = [
            [
                GridCell(self, area=self._area_for_cell(GridCoord(col, row)), grid=self)
                for col in range(grid_size.width)
            ]
            for row in range(grid_size.height)
        ]
        self.query = CollisionQuery(
            self
        )  # Delegate collision queries to CollisionQuery

    def _area_for_cell(self, grid_coord):
        """
        Calculate the area covered by the cell at the given grid coordinates.

        Parameters
        ----------
        grid_coord : GridCoord
            The grid coordinates for the cell (row, col).

        Returns
        -------
        Area
            The area object representing the space covered by this cell.
        """
        col_start = self.area.left + grid_coord.col * self.cell_width
        row_start = self.area.top + grid_coord.row * self.cell_height

        return Area(
            left=col_start,
            top=row_start,
            right=col_start + self.cell_width,
            bottom=row_start + self.cell_height,
        )

    def cell_at(self, row, col):
        return self.cells[row][col]


class GridCell:
    def __init__(self, area: "Area", grid_coord: "GridCoord"):
        self.area = area.clone()
        self.grid_coord = grid_coord.clone()
        self.contents = defaultdict(
            lambda: defaultdict(bool)
        )  # Layer -> Object -> bool

    def overlaps_with_circle(self, circle: "Circle") -> bool:
        """Check if the GridCell overlaps with a Circle."""
        return self.area.overlaps_with_circle(circle)

    def overlaps_with_area(self, area: "Area") -> bool:
        """Check if the GridCell overlaps with another Area."""
        return self.area.overlaps_with_area(area)

    def members_in_circle(self, circle: "Circle"):
        """Yield members within the circle."""
        for layer in self.contents:
            for obj in self.contents[layer]:
                if circle.contains_position(obj.position):
                    yield obj

    def members_in_area(self, area: "Area"):
        """Yield members within the area."""
        for layer in self.contents:
            for obj in self.contents[layer]:
                if area.contains(obj.position):
                    yield obj
