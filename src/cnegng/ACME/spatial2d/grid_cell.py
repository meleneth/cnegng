import math

from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.circle import Circle

class GridCell:
    def __init__(self, area: Area):
        """Each cell knows its area and stores its contents as a dictionary."""
        self.area = area
        self.contents = {}

    def add(self, item):
        """Add an item to the cell's contents"""
        self.contents[item] = True

    def remove(self, item):
        """Remove an item from the cell's contents"""
        del self.contents[item]

    def members(self):
        """Return an iterator over all inmates in this cell."""
        for member in self.contents.keys():
            yield member
    def is_in_radius(self, circle: Circle):
        """Check if the cell is within the radius of a given circle."""
        closest_x = max(self.area.left, min(circle.center.x, self.area.right))
        closest_y = max(self.area.top, min(circle.center.y, self.area.bottom))

        # Calculate the distance from the closest point to the circle's center
        distance = math.sqrt((closest_x - circle.center.x) ** 2 + (closest_y - circle.center.y) ** 2)

        return distance <= circle.radius

    def objects_in_radius(self, circle: Circle):
        """Yield objects that are inside the circle's radius."""
        if self.is_in_radius(circle):
            for obj in self.contents:
                obj_position = obj.position  # Assuming objects have a `position` attribute
                distance_to_center = math.sqrt((obj_position.x - circle.center.x) ** 2 +
                                               (obj_position.y - circle.center.y) ** 2)
                if distance_to_center <= circle.radius:
                    yield obj

    def __repr__(self):
        return f"GridCell({self.area}, contents={self.contents})"
