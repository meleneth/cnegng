from typing import Optional
import random
import copy

from cnegng.ACME.spatial2d.position import Position
from cnegng.ACME.spatial2d.dimensions import Dimensions


class Area:
    """
    Represents a rectangular area in 2D space.

    :param top: The top boundary of the area.
    :type top: float
    :param left: The left boundary of the area.
    :type left: float
    :param bottom: The bottom boundary of the area.
    :type bottom: float
    :param right: The right boundary of the area.
    :type right: float
    :param position: Optional position for the area.
    :type position: Position, optional
    :param dimensions: Optional dimensions for the area.
    :type dimensions: Dimensions, optional
    """

    def __init__(
        self,
        top: float = 0.0,
        left: float = 0.0,
        bottom: float = 0.0,
        right: float = 0.0,
        position: Optional[Position] = None,
        dimensions: Optional[Dimensions] = None,
    ):
        if position is not None and dimensions is not None:
            self.top = position.y
            self.left = position.x
            self.bottom = position.y + dimensions.height
            self.right = position.x + dimensions.width
        else:
            self.top = top
            self.left = left
            self.bottom = bottom
            self.right = right

    def clone(self):
        return copy.deepcopy(self)

    def contains(self, position: Position) -> bool:
        """
        Checks if the given position is inside the area (inclusive).

        :param position: The position to check
        :return: True if the position is inside the area, False otherwise
        """
        return (
            self.left <= position.x <= self.right
            and self.top <= position.y <= self.bottom
        )

    def overlap(self, other: "Area") -> "Optional[Area]":
        """
        Returns the overlapping area between two areas, or None if there is no overlap.

        :param other: The other area to check for overlap.
        :type other: Area
        :return: The overlapping Area, or None if no overlap exists.
        :rtype: Area or None
        """
        overlap_top = max(self.top, other.top)
        overlap_left = max(self.left, other.left)
        overlap_bottom = min(self.bottom, other.bottom)
        overlap_right = min(self.right, other.right)

        if overlap_top < overlap_bottom and overlap_left < overlap_right:
            return Area(overlap_top, overlap_left, overlap_bottom, overlap_right)
        else:
            return None

    def scale_by(self, other: "Area"):
        """
        Returns a callable that scales a given Position based on the scaling between two areas.

        As a destructive operation, this returns a new Position

        :param other: The other area used for scaling.
        :type other: Area
        :return: A callable that scales a Position.
        :rtype: Callable[[Position], Position]
        """
        scale_x = other.width / self.width
        scale_y = other.height / self.height

        def _scale(position: Position) -> Position:
            new_x = other.left + (position.x - self.left) * scale_x
            new_y = other.top + (position.y - self.top) * scale_y
            return Position(new_x, new_y)

        return _scale

    @property
    def height(self):
        """
        calculates the height of the area
        """
        return self.bottom - self.top
    
    def get_dimensions(self):
        return Dimensions(width=self.width, height = self.height)

    def random_position_inside(self):
        x = random.uniform(0, self.width()) + self.left
        y = random.uniform(0, self.height()) + self.top
        return Position(x, y)
    
    @property
    def width(self):
        """
        calculates the width of the area
        """
        return self.right - self.left
    
    def __truediv__(self, scalar: float) -> "Area":
        """
        Divides the area by a scalar value, scaling the boundaries accordingly.

        :param scalar: The scalar value to divide the area by.
        :type scalar: float
        :return: A new Area where each boundary is divided by the scalar.
        :rtype: Area
        """
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")

        return Area(
            self.top / scalar,
            self.left / scalar,
            self.bottom / scalar,
            self.right / scalar,
        )
