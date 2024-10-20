class CollisionQuery:
    """
    Handles collision-based queries in the grid.

    Attributes
    ----------
    grid : Grid
        The grid on which to perform the queries.
    """

    def __init__(self, grid):
        self.grid = grid

    def objects_in_circle(self, circle):
        """
        Yield all objects in the grid that are within the given circle.

        Parameters
        ----------
        circle : Circle
            The circle to check for intersections.

        Yields
        ------
        object
            Objects that are within the circle.
        """
        for cell in self.grid.cells_in_range(circle):
            if SpatialUtils.intersects(cell.area, circle):
                yield from cell.container.get_objects()
