from cnegng.ACME.stats.player_wearing_stats import PlayerWearingStats
from cnegng.ACME.stats.basic_stats import BasicStats


class Player(BasicStats):
    def wearing(self, *items):
        """
        Calculates the player's stats while wearing the given items. Modifies the player's base stats by applying
        any modifiers from the items worn.

        :param items: A list of items (each containing modifiers) worn by the player.
        :return: A PlayerWearingStats object that represents the player's modified stats.

        """
        return PlayerWearingStats(self, *items)
