class GlobalCoord:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_grid_coord(self, grid_size: int):
        """Convert a global coordinate to a grid coordinate by dividing by grid size."""
        return GridCoord(int(self.x // grid_size), int(self.y // grid_size))

    def __repr__(self):
        return f"GlobalCoord(x={self.x}, y={self.y})"

class GridCoord:
    def __init__(self, grid: "Grid", x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Grid coordinates must be integers.")
        self.grid = grid  # Store a reference to the associated Grid
        self.x = x
        self.y = y

    def to_flat_index(self):
        """Convert the grid coordinates to a flat index using the grid's width."""
        return self.y * self.grid.dimensions.width + self.x

    def to_global_coord(self):
        """Convert this grid coordinate back to a global coordinate using the grid's dimensions."""
        return GlobalCoord(self.x * self.grid.cell_width(), self.y * self.grid.cell_height())

    def __repr__(self):
        return f"GridCoord(grid=Grid({self.grid.dimensions.width}x{self.grid.dimensions.height}), x={self.x}, y={self.y})"
