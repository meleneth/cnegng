from cnegng.ACME.spatial2d.grid.grid import Grid


class GridIterator:
    """
    A class to iterate over a grid of cells, returning cells based on a modular number pattern.

    Attributes:
        grid (list): The grid of cells to iterate over.
        mod_number (int): The modulus number used to determine which cells are yielded.
        current_value (int): Tracks the current modulus value, starting from 0.

    Methods:
        iterate():
            Returns a generator that yields cells whose index matches index % mod_number == current_value.
            After each full iteration, increments current_value and wraps around after reaching mod_number.
    """

    def __init__(self, grid: Grid, mod_number: int):
        """
        Initializes the GridIterator with a grid and a modulus number.

        Args:
            grid (list): A list or iterable of grid cells to iterate over.
            mod_number (int): The number to mod the current index of the grid with.
        """

        self.grid = grid  # Assuming grid is a list or iterable of cells
        self.mod_number = mod_number
        self.current_value = 0
        self.counter = 0

    def iterate(self):
        # Get the total number of rows and columns
        num_rows = len(self.grid.cells)
        num_cols = len(self.grid.cells[0])

        # Yield grid cells row by row
        current_row = 0
        current_col = 0
        while current_row < num_rows:
            if current_col < num_cols:
                # Yield the current grid cell
                yield self.grid.cells[current_row][current_col]
                current_col += 1
            else:
                # Move to the next row
                current_row += 1
                current_col = 0
