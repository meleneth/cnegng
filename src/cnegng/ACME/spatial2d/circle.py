from cnegng.ACME.spatial2d.position import Position

class Circle:
    def __init__(self, center: Position, radius: float):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius})"
