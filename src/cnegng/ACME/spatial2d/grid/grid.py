import copy
from collections import defaultdict
from typing import Generator

from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.circle import Circle
from cnegng.ACME.spatial2d.grid.collision_query import CollisionQuery
from cnegng.ACME.spatial2d.grid.grid_indexer import GridIndexer
from cnegng.ACME.spatial2d.grid.object_container import ObjectContainer


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

    def contains(self, grid_coord: "GridCoord") -> bool:
        """
        Checks if the given position is inside the area (inclusive).

        :param position: The position to check
        :return: True if the position is inside the area, False otherwise
        """
        return 0 <= grid_coord.x <= self.width and 0 <= grid_coord.y <= self.height


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

    def clone(self):
        return copy.deepcopy(self)

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
                GridCell(
                    area=self._area_for_cell(GridCoord(grid=self, x=col, y=row)),
                    grid=self,
                    grid_coord=GridCoord(grid=self, x=col, y=row),
                )
                for col in range(grid_size.width)
            ]
            for row in range(grid_size.height)
        ]
        self.query = CollisionQuery(
            self
        )  # Delegate collision queries to CollisionQuery

    def __repr__(self):
        return f"Grid(area={self.area}, grid_size={self.grid_size})"

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
        col_start = self.area.left + grid_coord.x * self.cell_width
        row_start = self.area.top + grid_coord.y * self.cell_height

        return Area(
            left=col_start,
            top=row_start,
            right=col_start + self.cell_width,
            bottom=row_start + self.cell_height,
        )

    def cell_at(self, location: GridCoord) -> object:
        if not self.grid_size.contains(location):
            return None
        return self.cells[location.y][location.x]

    def add_to_cell(self, obj, coords: GlobalCoord | Position, layer="default"):
        """
        Adds an object to the grid cell that contains the given position.
        :param obj: Object to be added.
        :param position: Position object with x and y coordinates.
        """
        match coords:
            case Position():  # Match based on the Position class
                coords = GlobalCoord(x=coords.x, y=coords.y)
            case GlobalCoord():  # Match based on the GlobalCoord class
                pass  # Already a GlobalCoord

        cell = self.cell_at(self.to_coords(coords))
        cell.add_to_cell(obj, layer=layer)

    def to_coords(self, global_coords: GlobalCoord | Position) -> GridCoord:
        """
        Converts GlobalCoords to GridCoords based on the grid's area and dimensions.
        :param global_coords: GlobalCoords object.
        :return: GridCoords corresponding to the global position.
        """
        match global_coords:
            case Position():  # Match based on the Position class
                global_coords = GlobalCoord(x=global_coords.x, y=global_coords.y)
            case GlobalCoord():  # Match based on the GlobalCoord class
                pass  # Already a GlobalCoord
        x = int(global_coords.x / (self.area.width / self.grid_size.width))
        y = int(global_coords.y / (self.area.height / self.grid_size.height))
        return GridCoord(grid=self, x=x, y=y)

    def all_objects(self, layer=None):
        if layer is None:
            for row in self.cells:
                for cell in row:
                    yield from cell.all_members()
        else:
            for row in self.cells:
                for cell in row:
                    yield from cell.all_members(layer=layer)

    def cells_in_area(self, area):
        """
        Yields all GridCells that overlap with the given Area.

        :param area: Area object representing the region to check.
        :return: Generator yielding all GridCells that overlap with the given area.
        """
        # Determine grid coordinates range for the area
        min_x = max(0, int(area.left / (self.area.width / self.grid_size.width)))
        max_x = min(
            self.grid_size.width - 1,
            int(area.right / (self.area.width / self.grid_size.width)),
        )
        min_y = max(0, int(area.top / (self.area.height / self.grid_size.height)))
        max_y = min(
            self.grid_size.height - 1,
            int(area.bottom / (self.area.height / self.grid_size.height)),
        )

        # Iterate over the grid cells within the range and yield overlapping ones
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                cell = self.cell_at(GridCoord(grid=self, x=x, y=y))
                if cell is not None:
                    if cell.area.overlap(area) is not None:
                        yield cell

    def cells_in_circle(self, circle: Circle) -> Generator["GridCell", None, None]:
        # Calculate the bounding box of the circle
        min_x = max(0, int((circle.center.x - circle.radius) // self.cell_width))
        max_x = min(
            self.grid_size.width,
            int((circle.center.x + circle.radius) // self.cell_width),
        )
        min_y = max(0, int((circle.center.y - circle.radius) // self.cell_height))
        max_y = min(
            self.grid_size.height,
            int((circle.center.y + circle.radius) // self.cell_height),
        )

        # Iterate over the cells within the bounding box
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                grid_coord = GridCoord(grid=self, x=x, y=y)
                cell_area = self._area_for_cell(grid_coord)

                # Check if the cell overlaps with the circle
                if cell_area.overlaps_with_circle(circle):
                    yield self.cells[y][x]

    def objects_in_circle(self, circle : Circle, layer="default"):
        for cell in self.cells_in_circle(circle):
            yield from cell.objects_in_circle(circle, layer)


class GridCell:
    def __init__(self, area: "Area", grid_coord: "GridCoord", grid: "Grid"):
        self.area = area.clone()
        self.grid_coord = grid_coord.clone()
        self.grid = grid
        self.object_container = ObjectContainer(
            owner=self, owner_attr_name="owning_cell"
        )

    def overlaps_with_circle(self, circle: "Circle") -> bool:
        """Check if the GridCell overlaps with a Circle."""
        return self.area.overlaps_with_circle(circle)

    def overlaps_with_area(self, area: "Area") -> bool:
        """Check if the GridCell overlaps with another Area."""
        return self.area.overlaps_with_area(area)

    def objects_in_circle(self, circle: "Circle", layer="default"):
        """Yield members within the circle."""
        for obj in self.object_container.get_all(layer):
            if circle.contains_position(obj.position):
                yield obj

    def add_to_cell(self, object, layer="default"):
        self.object_container.add(object, layer=layer)

    def remove(self, object, layer="default"):
        self.object_container.remove(object, layer=layer)

    def all_members(self, layer=None):
        return self.object_container.get_all(layer=layer)
      
    def members_in_area(self, area: "Area"):
        """Yield members within the area."""
        for layer in self.contents:
            for obj in self.contents[layer]:
                if area.contains(obj.position):
                    yield obj
