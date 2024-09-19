from typing import Tuple
import math
import random

from cnegng.ACME.spatial2d.position import Position


class Motion:
    """
    Represents a 2D vector for motion with direction and speed.

    :param direction: The direction of the motion in radians
    :param speed: The speed of the motion
    """

    def __init__(self, direction: float = 0.0, speed: float = 1.0):
        self.direction = direction
        self.speed = speed

    def move(self, position: Position, dt: float = 1.0) -> None:
        """
        Moves the position according to the vector's direction and speed, scaled by the time delta.

        :param position: The position to move
        :param dt: The time delta (default is 1.0)
        """
        position.x += self.speed * dt * math.cos(self.direction)
        position.y += self.speed * dt * math.sin(self.direction)

    def x(self, dt: float = 1.0):
        return self.speed * dt * math.cos(self.direction)

    def y(self, dt: float = 1.0):
        return self.speed * dt * math.sin(self.direction)

    def updater(self, dt: float = 1.0):
        x = self.x(dt)
        y = self.y(dt)

        def apply(position: Position):
            position.x += x
            position.y += y

        return apply

    def randomize(
        self,
        direction_range: Tuple[float, float] = (0, 2 * math.pi),
        speed_range: Tuple[float, float] = (0, 10),
    ) -> None:
        """
        Randomizes the motion's direction and speed within the given ranges.

        :param direction_range: A tuple representing the min and max for the direction
        :param speed_range: A tuple representing the min and max for the speed
        """
        self.direction = random.uniform(*direction_range)
        self.speed = random.uniform(*speed_range)
