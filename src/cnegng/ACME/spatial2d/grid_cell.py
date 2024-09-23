import math
from collections import defaultdict

from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.circle import Circle

class AlreadyInACell(Exception):
    pass

class SanityError(Exception):
    pass

class ItemNotFound(Exception):
    pass
class GridCell:
    def __init__(self, area: Area, cell_index: int):
        """Each cell knows its area and stores its contents as a dictionary."""
        self.area = area
        self.contents = defaultdict(lambda: defaultdict(bool))
        self.cell_index = cell_index

    def add(self, item, layer: str = "default"):
        """Add an item to the cell's contents"""
        if item.current_cell is not None:
            raise AlreadyInACell()
        item.current_cell = self
        self.contents[layer][item] = True
    
    def __repr__(self):
        return f"GridCell(cell_index={self.cell_index}, area={self.area})"

    def remove(self, obj, layer='default'):
        """Remove an object from a specific layer."""
        if obj in self.contents[layer]:
            obj.current_cell = None
            del self.contents[layer][obj]
            # Clean up the layer if it's empty
            if not self.contents[layer]:
                del self.contents[layer]
            return
        raise ItemNotFound()

    def members(self, layer: str = "default"):
        """Return an iterator over all inmates in this cell."""
        for member in self.contents[layer].keys():
            yield member

    def is_in_circle(self, circle: Circle):
        """Check if the cell is within the radius of a given circle."""
        closest_x = max(self.area.left, min(circle.center.x, self.area.right))
        closest_y = max(self.area.top, min(circle.center.y, self.area.bottom))

        # Calculate the distance from the closest point to the circle's center
        distance = math.sqrt((closest_x - circle.center.x) ** 2 + (closest_y - circle.center.y) ** 2)

        return distance <= circle.radius

    def objects_in_circle(self, circle: Circle, label: str = "default"):
        """Yield objects that are inside the circle's radius."""
        if self.is_in_radius(circle):
            for obj in self.contents[label]:
                obj_position = obj.position  # Assuming objects have a `position` attribute
                distance_to_center = math.sqrt((obj_position.x - circle.center.x) ** 2 +
                                               (obj_position.y - circle.center.y) ** 2)
                if distance_to_center <= circle.radius:
                    yield obj

    def objects_in_area(self, area: Area, layer: str = "default"):
        obj_key = list(self.contents[layer].keys())
        for member in obj_key:
            if area.contains(member.position):
                yield member
