class Dimensions:
    """
    Represents a 2D dimension with width and height.

    :param width: The width of the dimension
    :param height: The height of the dimension
    """

    def __init__(self, width: float = 0.0, height: float = 0.0):
        self.width = width
        self.height = height

    def area(self):
        """
        calculates width * height
        """
        return self.width * self.height
