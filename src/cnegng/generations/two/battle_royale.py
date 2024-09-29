import random

class BattleRoyale:
    def __init__(self):
        self.critters = set()  # Critters in the map
        self.chests = set()  # Chests for loot
        self.consumables = set()  # Consumables like potions
        self.projectiles = set()  # Projectiles like arrows, bullets, etc.
        self.region_map = RegionMap(100, 100)  # 100x100 grid map for terrain

    def _sets_to_update(self):
        return [self.critters, self.projectiles, self.players]

    def update(self, dt):
        # Update all game objects like critters, chests, etc.
        for updateable in self._sets_to_update:
            for thing_to_update in updateable:
                thing_to_update.update(dt)
        # Update region-specific logic based on events

    def spawn_loot(self, chest):
        # Call to loot table to generate loot for the chest
        chest.spawn_loot()

    def terrain_at(self, position):
        # Returns the terrain at a given position
        return self.region_map.terrain_at(position)
