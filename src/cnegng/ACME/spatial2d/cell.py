class Cell:
    def __init__(self, area):
        self.area = area
        self.inmates = []  # List of sprites in the cell

    def add_object(self, obj):
        """Add an object (sprite) to this cell.

        set_owning_cell will be called on the object with this as the first argument
        """
        self.inmates.append(obj)
        obj.set_owning_cell(self)

    def remove_object(self, obj):
        """Remove an object (sprite) from this cell."""
        self.inmates.remove(obj)
        obj.set_owning_cell(None)

    def members(self):
        """Return an iterator over all inmates in this cell."""
        for inmate in self.inmates:
            yield inmate
