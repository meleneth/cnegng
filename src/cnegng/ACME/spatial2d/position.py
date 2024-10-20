from typing import Tuple
import math
import random
import copy
from dataclasses import dataclass


@dataclass
class Position:
    """
    Represents a 2D position in space.

    :param x: The x coordinate
    :param y: The y coordinate
    """

    x: float
    y: float

    def randomize(
        self,
        x_range: Tuple[float, float] = (0, 1000),
        y_range: Tuple[float, float] = (0, 1000),
    ) -> None:
        """
        Randomizes the position within the given ranges.

        :param x_range: A tuple representing the min and max for the x coordinate
        :param y_range: A tuple representing the min and max for the y coordinate
        """
        self.x = random.uniform(*x_range)
        self.y = random.uniform(*y_range)

    def add(self, other):
        """
        Adds a motion vector (or position) to the position to update it.

        :param other: a Position or Motion
        """
        self.x += other.x
        self.y += other.y

    def wrap_within_area(self, area):
        """
        Wrap the x and y coordinates based on the area's dimensions using modulus
        """
        self.x = (self.x - area.left) % (area.right - area.left) + area.left
        self.y = (self.y - area.top) % (area.bottom - area.top) + area.top

    def clone(self):
        return copy.deepcopy(self)

    def distance(self, other: "Position") -> float:
        """
        Calculates the Euclidean distance between this position and another position.

        :param other: The other Position object
        :return: The distance between the two positions
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
