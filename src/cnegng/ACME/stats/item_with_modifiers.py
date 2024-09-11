class ItemWithModifiers:
    def __init__(self, *modifiers):
        """
        Initializes an item that can modify the player's stats. Each item contains a list of AttributeModifier instances
        that apply modifications to the player's stats.

        :param modifiers: A list of AttributeModifier objects that define how the item's effects modify player stats.
        """

        self.modifiers = modifiers

    def __dir__(self):
        """
        Declares the attributes (stat names) this item affects by looking at the stat names from its modifiers.

        :return: A list of stat names that the item affects.
        """
        # TODO what is this garbage, modifiers should at least be typed
        return [modifier.stat_name for modifier in self.modifiers]
