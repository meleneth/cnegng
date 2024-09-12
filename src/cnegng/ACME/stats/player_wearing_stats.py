from collections import defaultdict


class PlayerWearingStats:
    def __init__(self, base_stats, *items):
        """
        Initializes a PlayerWearingStats object that combines the base stats of the player with the modifiers
        provided by the worn items.

        :param base_stats: The base stats of the player.
        :param items: A list of items, where each item contains modifiers to be applied to the player's stats.
        """

        # autovivify dict values as empty arrays
        self.modifier_chains = defaultdict(list)
        self.base_stats = base_stats

        for item in items:
            for modifier in item.modifiers:
                self.modifier_chains[modifier.stat_name].append(modifier)

    def __getattr__(self, name):
        """
        Dynamically calculates and returns the value of a stat, including all modifications from worn items.

        :param name: The name of the stat to retrieve (e.g., 'maximum_life').
        :return: The final calculated value of the stat.
        :raises AttributeError: If the stat is not found.
        """

        value = 0
        if hasattr(self.base_stats, name):
            value = getattr(self.base_stats, name)
        for modifier in self.modifier_chains[name]:
            value = modifier.apply(value)
        return value

    def __dir__(self):
        """
        Returns the list of stat names that have been initialized and are affected by modifiers.

        :return: A list of the stat names affected by modifiers.
        """
        return list(self.modifier_chains.keys())
