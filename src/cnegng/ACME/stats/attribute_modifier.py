from typing import List, Dict, Any, Optional


class ApplyNotInitialized(Exception):
    pass


class AttributeModifier:
    """
    Represents a modifier, such as found on a piece of gear.

    Attributes
    ==========
    stat_name : str
        The name of the stat the modifier effects
    value : Any
        the value the apply function will use to compute the answer when combined with the base_stat that is passed in
    """

    def __init__(self, stat_name, value):
        """
        Initializes an AttributeModifier that can modify a given stat by either adding a flat value or applying
        a percentage-based modification.


        :param stat_name: The name of the stat to modify (e.g., 'maximum_life').
        :param value: The value of the modification (e.g., +20 for flat, or +0.5 for a 50% increase).
        """
        self.stat_name = stat_name
        self.value = value
        self.apply = self.apply_not_initialized

    def apply_not_initialized(self):
        raise ApplyNotInitialized()

    def apply_flat(self, base_value):
        return base_value + self.value

    def apply_percent(self, base_value):
        return base_value * (1 + self.value)

    @classmethod
    def create_flat(cls, stat_name, value):
        modifier = cls(stat_name, value)
        modifier.apply = modifier.apply_flat
        return modifier

    @classmethod
    def create_percent(cls, stat_name, value):
        modifier = cls(stat_name, value)
        modifier.apply = modifier.apply_percent
        return modifier
