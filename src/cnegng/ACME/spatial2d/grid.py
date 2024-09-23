from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.circle import Circle
from cnegng.ACME.spatial2d.grid_cell import GridCell
from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.adapter import DimensionsToArea, AreaToPosition
from cnegng.ACME.spatial2d.coordinates import GlobalCoord, GridCoord

class PositionOutsideGrid(Exception):
    pass

class Grid:
    """
    Represents a 2D grid using a single-dimensional list of cells.

    :param area: The area covered by the grid
    :param dimensions: The number of rows and columns (width, height)
    :param cell_class: class to construct cells out of, defaults to GridCell
    """

    def __init__(self, area: Area, dimensions: Dimensions, cell_class=GridCell):
        """Create a grid with an overall area and divide it into cells based on dimensions."""
        self.area = area.clone()
        self.dimensions = dimensions.clone()
        self.global_to_local = self.area.scale_by(DimensionsToArea(self.dimensions))
        self.local_to_global = DimensionsToArea(self.dimensions).scale_by(self.area)
        self.cell_width = int(self.area.width) // int(self.dimensions.width)
        self.cell_height = int(self.area.height) // int(self.dimensions.height)
        self.cell_dimensions = Dimensions(width=self.cell_width, height=self.cell_height)
        self.cell_class = cell_class
        self.group_call_counts = {}  # Dictionary to track call counts for different groups
        self.orphaned_objects = []
        self.cells = self._create_cells()


    @property
    def width(self):
        return self.area.right - self.area.left

    @property
    def height(self):
        return self.area.bottom - self.area.top

    def _create_cells(self):
        """Initialize the grid by dividing the area into cells based on dimensions."""
        cells = []
        cell_index = 0
        for row_index in range(self.dimensions.height):
            for col_index in range(self.dimensions.width):
                # Calculate the top-left corner for this cell
                top = self.area.top + row_index * self.dimensions.height
                left = self.area.left + col_index * self.dimensions.width

                # Calculate the bottom-right corner for this cell
                bottom = top + self.dimensions.height
                right = left + self.dimensions.width

                # Clone the area and create a new cell with the calculated area
                cell_area = Area(top, left, bottom, right)
                cells.append(self.cell_class(cell_area, cell_index))
                cell_index += 1
        return cells

    def cell_for(self, global_coord: GlobalCoord) -> GridCell:
        """
        Finds the cell corresponding to the given position.

        :param global_coord: The position to find the cell for
        :return: The corresponding cell object
        """
        if not self.area.contains(global_coord):
            raise ValueError("Position out of bounds")
        x_index = int(global_coord.x // self.cell_dimensions.width)
        y_index = int(global_coord.y // self.cell_dimensions.height)
        index = y_index * int(self.dimensions.width) + x_index
        return self.cells[index]

    def add_to_cell(self, position: Position, item):
        """Add an item to the cell at the specified position."""
        cell = self.cell_for(position)
        cell.add(item)

    def remove_from_cell(self, position: Position, item):
        """Remove an item from the cell at the specified position."""
        cell = self.cell_for(position)
        cell.remove(item)

    def get_cells_in_group(self, name: str, number_of_groups: int):
        """Divide the cells into number_of_groups groups, and yield the cells that match 'this time'."""
        if name not in self.group_call_counts:
            self.group_call_counts[name] = 0  # Initialize the counter for this group name

        counter = self.group_call_counts[name]
        total_cells = len(self.cells) * len(self.cells[0])  # Total number of cells
        group_size = total_cells // number_of_groups
        group_index = counter % number_of_groups

        # Increment the counter for the next call
        self.group_call_counts[name] += 1

        # Yield cells that are part of this group
        for y in range(len(self.cells)):
            for x in range(len(self.cells[0])):
                # Determine the group for this cell based on its linear index
                linear_index = y * len(self.cells[0]) + x
                if linear_index // group_size == group_index:
                    yield self.cells[y][x]

    def __repr__(self):
        return f"Grid(area={self.area}, dimensions={self.dimensions}, cell_class={self.cell_class.__name__})"
    


    def update_orphaned_objects(self):
        """Re-add orphaned objects to their correct cells after position updates."""
        for obj in self.orphaned_objects:
            self.add_object_to_cell(obj, obj.x, obj.y)
        self.orphaned_objects.clear()

    def cells_in_range(self, area: Area):
        """Yield all cells that overlap the given area."""
        for cell in self.cells:
            if self.areas_overlap(cell.area, area):
                yield cell

    @staticmethod
    def areas_overlap(area1: Area, area2: Area) -> bool:
        """Check if two areas overlap."""
        return not (area1.right <= area2.left or
                    area1.left >= area2.right or
                    area1.bottom <= area2.top or
                    area1.top >= area2.bottom)
   

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
    
    def cells_in_range(self, area: Area):
        """Yield all cells that overlap the given area."""
        for row in self.cells:
            for cell in row:
                if self.areas_overlap(cell.area, area):
                    yield cell
    
    def all_objects(self, layer='default'):
        """Return an iterator that yields all objects in the grid."""
        for cell in self.cells:
            # I member
            yield from cell.members(layer=layer)

    def objects_in_area(self, area: Area, layer='default'):
        """Yield all objects in the grid that are within the area."""
        for cell in self.cells_in_range(area=area):
            yield from cell.objects_in_area(area, layer=layer)

    def objects_in_circle(self, circle: Circle, layer='default'):
        """Yield all objects in the grid that are within the circle's radius."""
        for cell in self.cells:
            if cell.is_in_circle(circle):
                yield from cell.objects_in_radius(circle, layer=layer)

    def flat_index(self, row: int, col: int):
        """Convert a (row, col) pair to a flat index in the flat list of cells."""
        return row * self.dimensions.width + col

    def cells_in_range(self, area: Area):
        """Yield cells that overlap with the given global Area using flat index."""
        start_global = GlobalCoord(area.left, area.top)
        end_global = GlobalCoord(area.right, area.bottom)

        start_grid = self.to_grid_coord(start_global)
        end_grid = self.to_grid_coord(end_global)

        for row in range(start_grid.y, end_grid.y + 1):
            for col in range(start_grid.x, end_grid.x + 1):
                if 0 <= row < self.dimensions.height and 0 <= col < self.dimensions.width:
                    flat_idx = self.flat_index(row, col)
                    yield self.cells[flat_idx]
        
    def to_grid_coord(self, position: "Position") -> "GridCoord":
        """Convert global coordinates to grid-local coordinates."""
        # Ensure the position is within the bounds of the grid area
        if not self.area.contains(position):
            raise PositionOutsideGrid()
        #    raise ValueError(f"Position {position} is out of bounds of the grid area {self.area}")

        # Translate the global coordinates to local grid coordinates
        x_local = int((position.x - self.area.left) // self.cell_width)
        y_local = int((position.y - self.area.top) // self.cell_height)

        # Ensure the coordinates stay within bounds of the grid
        if x_local < 0 or x_local >= self.dimensions.width or y_local < 0 or y_local >= self.dimensions.height:
            raise ValueError(f"Converted grid coordinates ({x_local}, {y_local}) are out of bounds")

        return GridCoord(x=x_local, y=y_local, grid=self)
