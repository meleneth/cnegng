from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.cell import Cell
from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions


class Grid:
    """
    Represents a 2D grid using a single-dimensional list of cells.

    :param area: The area covered by the grid
    :param dimensions: The number of rows and columns (width, height)
    """

    def __init__(self, area: Area, dimensions: Dimensions):
        self.area = area
        self.columns = int(dimensions.width)
        self.rows = int(dimensions.height)
        self.cell_width = self.area.width() / self.columns
        self.cell_height = self.area.width() / self.rows
        self.cells = []
        self.orphaned_objects = []
        self.current_group = (
            0  # Keeps track of which group of cells we're checking this frame
        )
        for index in range(self.rows * self.columns):
            self._create_cell_for(index)

    def _create_cell_for(self, index):
        col = index % self.columns
        row = index // self.columns
        top = row * self.cell_height
        left = col * self.cell_width
        bottom = top + self.cell_height
        right = left + self.cell_width
        cell = Cell(area=Area(top, left, bottom, right))
        self.cells.append(cell)

    def cell_for(self, position: Position) -> Cell:
        """
        Finds the cell corresponding to the given position.

        :param position: The position to find the cell for
        :return: The corresponding cell object
        """
        if not self.area.contains(position):
            raise ValueError("Position out of bounds")

        col = int((position.x - self.area.left) / self.cell_width)
        row = int((position.y - self.area.top) / self.cell_height)
        index = row * self.columns + col
        return self.cells[index]

    def add_object_to_cell(self, obj):
        """Add an object to the specified cell."""
        cell = self.get_cell(position=obj.position)
        obj.current_cell = cell
        cell.add_object(obj)

    def remove_object_from_cell(self, obj):
        """Remove an object from its current cell."""
        if obj.current_cell is not None:
            obj.current_cell.remove_object(obj)

    def update_orphaned_objects(self):
        """Re-add orphaned objects to their correct cells after position updates."""
        for obj in self.orphaned_objects:
            self.add_object_to_cell(obj, obj.x, obj.y)
        self.orphaned_objects.clear()

    def _cells_in_range(self, x_min, y_min, x_max, y_max):
        """Yield all cells that overlap the given bounding box (x_min, y_min) to (x_max, y_max)."""
        # Handle world wrapping
        x_min = x_min % WORLD_SIZE
        y_min = y_min % WORLD_SIZE
        x_max = x_max % WORLD_SIZE
        y_max = y_max % WORLD_SIZE

        # Determine grid cell boundaries
        col_start = int(x_min // CELL_WIDTH)
        col_end = int(x_max // CELL_WIDTH)
        row_start = int(y_min // CELL_HEIGHT)
        row_end = int(y_max // CELL_HEIGHT)

        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                yield self.cells[row % GRID_SIZE][col % GRID_SIZE]

    def objects_in_radius(self, center_x, center_y, radius):
        """Return an iterator over all objects within a certain radius of (center_x, center_y)."""
        # Compute the bounding box that contains the circle
        x_min = center_x - radius
        y_min = center_y - radius
        x_max = center_x + radius
        y_max = center_y + radius

        radius_squared = radius**2

        for cell in self._cells_in_range(x_min, y_min, x_max, y_max):
            for obj in cell.nearby_occupants():
                # Check if the object is within the radius
                dx = (obj.x - center_x) % WORLD_SIZE
                dy = (obj.y - center_y) % WORLD_SIZE
                distance_squared = dx * dx + dy * dy
                if distance_squared <= radius_squared:
                    yield obj

    def check_group_for_escapes(self):
        """Check 1/8th of the grid cells for sprite escapes."""
        cells_per_group = len(self.cells) // 8
        start_idx = self.current_group * cells_per_group
        end_idx = start_idx + cells_per_group

        for cell in self.cells[start_idx:end_idx]:
            for obj in list(cell.occupants):  # Copy the list to allow safe removal
                if not cell.contains(obj.position):
                    self.orphaned_objects.append(obj)
                    cell.remove_object(obj)

        # Move to the next group of cells for the next frame
        self.current_group = (self.current_group + 1) % 8

    def all_objects(self):
        """Return an iterator that yields all objects in the grid."""
        for row in self.cells:
            for cell in row:
                for obj in cell.nearby_occupants():
                    yield obj
