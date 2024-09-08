from cnegng.ACME.stats.stat_modifier_chain import StatModifierChain

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
        if (modifier_chain := self.modifier_chains.get(name)) is not None:
            return modifier_chain.get_value()

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __dir__(self):
        """
        Returns the list of stat names that have been initialized and are affected by modifiers.

        :return: A list of the stat names affected by modifiers.
        """
        return list(self.modifier_chains.keys())
