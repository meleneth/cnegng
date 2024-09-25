class ObjectContainer:
    """
    Manages objects within a grid cell.

    Attributes
    ----------
    objects : dict
        A dictionary that stores objects, separated by layers.
    """

    def __init__(self):
        self.objects = {}

    def add_object(self, obj, layer='default'):
        """
        Add an object to a specific layer in the container.

        Parameters
        ----------
        obj : object
            The object to add.
        layer : str
            The layer in which to add the object (default is 'default').
        """
        if layer not in self.objects:
            self.objects[layer] = []
        self.objects[layer].append(obj)

    def remove_object(self, obj, layer='default'):
        """
        Remove an object from a specific layer.

        Parameters
        ----------
        obj : object
            The object to remove.
        layer : str
            The layer from which to remove the object.
        """
        if layer in self.objects and obj in self.objects[layer]:
            self.objects[layer].remove(obj)

    def get_objects(self, layer='default'):
        """
        Get all objects from a specific layer.

        Parameters
        ----------
        layer : str
            The layer from which to get the objects.

        Returns
        -------
        list
            A list of objects in the specified layer.
        """
        return self.objects.get(layer, [])
