class AttributeModifier:
    def __init__(self, stat_name, modification_type, value):
        """
        Initializes an AttributeModifier that can modify a given stat by either adding a flat value or applying
        a percentage-based modification.


        :param stat_name: The name of the stat to modify (e.g., 'maximum_life').
        :param modification_type: The type of modification: 'flat' for flat additions, 'percent' for percentage-based buffs.
        :param value: The value of the modification (e.g., +20 for flat, or +0.5 for a 50% increase).
        """
        self.stat_name = stat_name
        self.modification_type = modification_type
        self.value = value

    def apply(self, base_value):
        """
        Applies the modifier to a base stat value.

        :param base_value: The current value of the stat before modification.
        :return: The modified stat value.
        """
        if self.modification_type == "flat":
            return base_value + self.value
        elif self.modification_type == "percent":

            return base_value * (1 + self.value)

        return base_value
