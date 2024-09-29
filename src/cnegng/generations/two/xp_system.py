class XPSystem:
    """
    A system to manage player XP and levels, with level-up notifications.

    The XP required to level up is determined by the following formula:

    .. math::
       XP_{toLevelUp} = base\_xp \times (level^{factor})

    Where:
    - base_xp is the base amount of XP required to level up from level 1.
    - factor controls how quickly the XP required increases.

    Example usage:
        >>> xp_system = XPSystem()
        >>> xp_system.add_xp(player, 250)  # Adds XP and handles level-up
    """

    MAX_LEVEL = 99
    BASE_XP = 100
    XP_FACTOR = 1.2

    def __init__(self, event_bus: EventBus):
        """
        Initialize the XPSystem with an event bus for level-up notifications.

        :param event_bus: The event bus to send level-up events.
        """
        self.event_bus = event_bus

    def calculate_xp_for_next_level(self, level: int) -> int:
        """
        Calculate the XP required to reach the next level based on the player's current level.

        :param level: The player's current level.
        :return: The XP required to level up to the next level.
        """
        if level >= self.MAX_LEVEL:
            return 0
        return int(self.BASE_XP * (level ** self.XP_FACTOR))

    def add_xp(self, player: 'Player', xp: int):
        """
        Add XP to a player and handle level-ups if the player reaches the required XP for the next level.

        :param player: The player object gaining XP.
        :param xp: The amount of XP to add.
        """
        if player.level >= self.MAX_LEVEL:
            return

        player.xp += xp

        # Check if the player has enough XP to level up
        while player.xp >= self.calculate_xp_for_next_level(player.level):
            self.level_up(player)

    def level_up(self, player: 'Player'):
        """
        Handle leveling up the player by increasing their level and broadcasting a LEVEL_UP event.

        :param player: The player object leveling up.
        """
        if player.level < self.MAX_LEVEL:
            player.level += 1
            player.xp = 0  # Reset XP after level up (or adjust as per preference)

            # Publish a LEVEL_UP event
            self.event_bus.publish('LEVEL_UP', player)
