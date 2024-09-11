import random
import bisect


class LootTable:
    def __init__(self):
        self.cumulative_ranges = []
        self.actions = []
        self.total_chance = 0

    def add_entry(self, chance, action):
        """
        Add an entry to the loot table.

        :param chance: Probability of triggering the action (value between 0 and 1).

        :param action: A callable action to trigger.
        """
        if not callable(action):
            raise ValueError("Action must be a callable")
        if not 0 <= chance <= 1:
            raise ValueError("Chance must be between 0 and 1")
        if self.total_chance + chance > 1:
            raise ValueError("Total chances in the loot table exceed 1")

        self.total_chance += chance

        self.cumulative_ranges.append(self.total_chance)
        self.actions.append(action)

    def roll(self):
        """
        Roll once for the entire loot table using bisect and select an action based on the ranges.

        :return: Result of the triggered action, or None if no action is triggered.
        """

        if not self.actions:
            return None

        roll_value = random.random()  # Roll once between 0 and 1
        idx = bisect.bisect_right(
            self.cumulative_ranges, roll_value
        )  # Binary search for the range
        if idx < len(self.actions):
            return self.actions[idx]()
        return None

    def copy_loot_to(self, other_table):
        """
        Copy all of the loot in this loot table to other_table.

        :param other_table: A LootTable instance to copy entries to.
        """
        current_chance = 0
        for idx, action in enumerate(self.actions):
            current_chance = other_table.cumulative_ranges[idx] - current_chance
            other_table.add_entry(current_chance, action)
            current_chance = other_table.cumulative_ranges[idx]
