from typing import Tuple
import math
import random
import copy
from dataclasses import dataclass
from typing import NewType

from cnegng.ACME.spatial2d.basic_types import Radian, Speed, DeltaTime
from cnegng.ACME.spatial2d.position import Position

@dataclass
class Motion:
    """
    Represents a 2D vector for motion with direction and speed.

    :param direction: The direction of the motion in radians
    :param speed: The speed of the motion
    """
    direction: Radian
    speed: Speed

    def clone(self):
        return copy.deepcopy(self)

    def move(self, position: Position, dt: DeltaTime) -> None:
        """
        Moves the position according to the vector's direction and speed, scaled by the time delta.
        Returns a new position, which makes this method itself non destructive

        :param position: The position to move
        :param dt: The time delta (default is 1.0)
        """
        return Position(x=position.x + self.speed * dt * math.cos(self.direction), y= position.y + self.speed * dt * math.sin(self.direction))

    def x(self, dt: DeltaTime):
        return self.speed * dt * math.cos(self.direction)

    def y(self, dt: DeltaTime):
        return self.speed * dt * math.sin(self.direction)

    def updater(self, dt: DeltaTime):
        """
        Creates a method to cache the results of the movement update calculation for application to multiple positions without having to redo the math.
        """
        x = self.x(dt)
        y = self.y(dt)

        def apply(position: Position):
            new_position = Position(position.x + x, position.y + y)
            return new_position

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

    def lerp(self, target, dt: DeltaTime):
        # Smoothly transition to the new direction (linear interpolation)
        angle_diff = (target.direction - self.direction) % (2 * math.pi)
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        # Adjust the current direction based on the angle difference, at a rate of 0.5 radians per second
        self.direction += angle_diff * min(dt, 0.25)
        self.direction %= 2 * math.pi
