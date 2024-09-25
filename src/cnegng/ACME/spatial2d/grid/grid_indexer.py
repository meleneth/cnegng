class GridIndexer:
    """
    Handles conversion between world coordinates and grid indices.
    
    Attributes
    ----------
    grid_width : int
        The width of the grid in terms of number of cells.
    grid_height : int
        The height of the grid in terms of number of cells.
    cell_width : float
        The width of each cell.
    cell_height : float
        The height of each cell.
    """

    def __init__(self, grid_width, grid_height, cell_width, cell_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_width = cell_width
        self.cell_height = cell_height

    def to_grid_coord(self, position):
        """
        Convert a world position to grid coordinates.

        Parameters
        ----------
        position : Position
            The position to convert.

        Returns
        -------
        tuple
            A tuple of (row, col) representing the grid coordinates.
        """
        row = int(position.y // self.cell_height)
        col = int(position.x // self.cell_width)
        return (row, col)

    def cell_index(self, row, col):
        """
        Convert grid coordinates to a flat list index.

        Parameters
        ----------
        row : int
            The row index.
        col : int
            The column index.

        Returns
        -------
        int
            The index of the cell in a flat list.
        """
        return row * self.grid_width + col
