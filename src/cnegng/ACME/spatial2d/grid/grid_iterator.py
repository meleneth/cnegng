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

    def __init__(self, grid : Grid, mod_number: int):
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
        """
        Creates a generator that yields cells from the grid based on their index modulo mod_number.
        
        Yields:
            The next cell in the grid whose index satisfies the condition index % mod_number == current_value.
        
        Increments the current_value after each full iteration over the grid.
        """
        for index, cell in enumerate(self.grid):
            if index % self.mod_number == self.current_value:
                yield cell
        self.current_value = (self.current_value + 1) % self.mod_number
        