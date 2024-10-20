class ImplementMe(Exception):
    pass


class LootChest:
    def __init__(self, position):
        self.position = position
        self.is_open = False
        self.loot = []

    def open(self):
        if not self.is_open:
            self.is_open = True
            self.loot = self.spawn_loot()

    def spawn_loot(self):
        # Use the existing loot table logic to generate loot based on difficulty
        # For example, fetch terrain difficulty to scale loot rewards
        terrain = self.get_terrain_difficulty()
        raise ImplementMe("Chest opened")
        return generate_loot_table(terrain.difficulty)

    def get_terrain_difficulty(self):
        # Get the difficulty of the terrain where this chest is placed
        pass
