class ObjectContainer:
    def __init__(self, owner, owner_attr_name="owner"):
        """
        Initializes the ObjectContainer with an owner and the attribute name
        used for owner tracking on the objects. Objects are stored in layers.

        :param owner: The owner of this container.
        :param owner_attr_name: The name of the attribute in each object for tracking ownership.
        """
        self._layers = {}  # Dictionary to store objects by layers
        self.owner = owner
        self.owner_attr_name = owner_attr_name

    def add(self, obj, layer="default"):
        """
        Add an object to a specific layer in the container. The object's owner attribute is set to the container's owner.
        An object with an existing (non-None) owner cannot be added.

        :param obj: The object to be added.
        :param layer: The layer to add the object to.
        :raises ValueError: If the object already has a non-None owner.
        """
        if getattr(obj, self.owner_attr_name, None) is not None:
            raise ValueError(f"Cannot add object {obj}. It already has an owner.")

        # Set the object's owner attribute to the container's owner
        setattr(obj, self.owner_attr_name, self.owner)

        # Add object to the specified layer
        if layer not in self._layers:

            self._layers[layer] = set()

        self._layers[layer].add(obj)

    def remove(self, obj, layer="default"):
        """
        Remove an object from a specific layer in the container and clear its owner attribute.

        :param obj: The object to be removed.
        :param layer: The layer to remove the object from.
        """

        if layer in self._layers and obj in self._layers[layer]:
            self._layers[layer].remove(obj)
            # Reset the object's owner attribute to None
            setattr(obj, self.owner_attr_name, None)

    def contains(self, obj, layer=None):
        """

        Check if an object is in a specific layer of the container.

        :param obj: The object to check.
        :param layer: The layer to check.
        :return: True if the object is in the layer, False otherwise.
        """
        return layer in self._layers and obj in self._layers[layer]

    def size(self, layer=None):
        """
        Get the number of objects in the container or in a specific layer.

        :param layer: The layer to count objects in. If None, return the total size across all layers.
        :return: The number of objects.
        """
        if layer is not None:
            return len(self._layers.get(layer, []))

        return sum(len(objects) for objects in self._layers.values())

    def clear(self, layer=None):
        """
        Remove all objects from a specific layer or from the entire container and reset their owner attributes.

        :param layer: The layer to clear. If None, clear all layers.
        """
        if layer is not None:
            for obj in self._layers.get(layer, []):
                setattr(obj, self.owner_attr_name, None)
            self._layers[layer] = set()
        else:
            for objects in self._layers.values():
                for obj in objects:
                    setattr(obj, self.owner_attr_name, None)
            self._layers.clear()

    def get_all(self, layer=None):
        """
        Return all objects in a specific layer or in the entire container.

        :param layer: The layer to get objects from. If None, return all objects from all layers.

        :return: A set of objects in the specified layer, or a set of all objects.

        """
        if layer is not None:
            return self._layers.get(layer, set()).copy()
        all_objects = set()
        for objects in self._layers.values():
            all_objects.update(objects)
        return all_objects

    def layers(self):
        return self._layers.keys()
