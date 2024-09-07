class StatModifierChain:

    def __init__(self, base_value):
        """
        Initializes a chain of stat modifiers starting from a base value.

        :param base_value: The base value of the stat before any modifiers are applied.
        """
        self.base_value = base_value
        self.modifiers = []

    def add_modifier(self, modifier_func):
        """
        Adds a new modifier function to the chain. Each modifier function should accept a base value and return
        the modified value.


        :param modifier_func: A function that takes the base value and modifies it.
        """
        self.modifiers.append(modifier_func)

    def get_value(self):
        """

        Calculates the final stat value after applying all the modifiers in the chain.

        :return: The modified stat value.
        """
        value = self.base_value

        for modifier in self.modifiers:
            value = modifier(value)  # Apply each modifier in the chain
        return value


class BasicStats:
    def __init__(self, **kwargs):
        """
        Initializes a BasicStats object with arbitrary keyword arguments as attributes. Each attribute corresponds
        to a stat like 'maximum_life', 'strength', etc.

        :param kwargs: Arbitrary stats provided as keyword arguments (e.g., maximum_life=60, strength=10).
        """
        self._specified_keys = set(kwargs.keys())  # Track only initialized attributes
        self.__dict__.update(kwargs)

    def __dir__(self):
        """

        Returns only the explicitly specified attributes in the object.

        :return: A list of the stat names that were explicitly initialized.
        """

        return list(self._specified_keys)


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


class Player(BasicStats):
    def wearing(self, *items):
        """
        Calculates the player's stats while wearing the given items. Modifies the player's base stats by applying
        any modifiers from the items worn.

        :param items: A list of items (each containing modifiers) worn by the player.
        :return: A PlayerWearingStats object that represents the player's modified stats.

        """
        return PlayerWearingStats(self, *items)


class PlayerWearingStats:
    def __init__(self, base_stats, *items):
        """
        Initializes a PlayerWearingStats object that combines the base stats of the player with the modifiers
        provided by the worn items.

        :param base_stats: The base stats of the player.
        :param items: A list of items, where each item contains modifiers to be applied to the player's stats.
        """

        self.base_stats = base_stats
        self.items = items
        self.modifier_chains = {}

        # For each stat in the base player, create a modifier chain starting from the base stat's value
        for stat in base_stats._specified_keys:
            self.modifier_chains[stat] = StatModifierChain(getattr(base_stats, stat))

        # Apply each item's modifiers to the appropriate stats
        for item in items:
            for modifier in item.get_modifiers():
                # If the stat doesn't exist in base stats, we initialize the modifier chain with 0
                if modifier.stat_name not in self.modifier_chains:
                    self.modifier_chains[modifier.stat_name] = StatModifierChain(0)

                self.modifier_chains[modifier.stat_name].add_modifier(
                    lambda base, mod=modifier: mod.apply(base)
                )

    def __getattr__(self, name):
        """
        Dynamically calculates and returns the value of a stat, including all modifications from worn items.

        :param name: The name of the stat to retrieve (e.g., 'maximum_life').
        :return: The final calculated value of the stat.
        :raises AttributeError: If the stat is not found.
        """
        if name in self.modifier_chains:

            return self.modifier_chains[name].get_value()

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __dir__(self):
        """
        Returns the list of stat names that have been initialized and are affected by modifiers.

        :return: A list of the stat names affected by modifiers.
        """
        return list(self.modifier_chains.keys())


class ItemWithModifiers:
    def __init__(self, modifiers):
        """
        Initializes an item that can modify the player's stats. Each item contains a list of AttributeModifier instances
        that apply modifications to the player's stats.

        :param modifiers: A list of AttributeModifier objects that define how the item's effects modify player stats.
        """

        self.modifiers = modifiers

    def get_modifiers(self):
        """
        Retrieves the list of modifiers associated with this item.

        :return: A list of AttributeModifier objects.
        """
        return self.modifiers

    def __dir__(self):
        """
        Declares the attributes (stat names) this item affects by looking at the stat names from its modifiers.

        :return: A list of stat names that the item affects.
        """
        return [modifier.stat_name for modifier in self.modifiers]
