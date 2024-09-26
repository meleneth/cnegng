import math

from cnegng.ACME.spatial2d.position import Position

class Circle:
    def __init__(self, center: Position, radius: float):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def contains_position(self, position: Position) -> bool:
        # Calculate the distance between the center of the circle and the position
        distance = math.sqrt((position.x - self.center.x) ** 2 + (position.y - self.center.y) ** 2)
        
        # Check if the distance is less than or equal to the radius
        return distance <= self.radius
