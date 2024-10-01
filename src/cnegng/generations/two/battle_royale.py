import random
from functools import lru_cache
from cnegng.ACME.spatial2d import Position

from cnegng.generations.two.region import RegionMap
from cnegng.generations.two.name_generators import ElvishNameGenerator
from cnegng.ACME.spatial2d.dimensions import Dimensions

class BattleRoyale:
    def __init__(self, dimensions : Dimensions):
        self.dimensions = dimensions
        self.critters = set()  # Critters in the map
        self.chests = set()  # Chests for loot
        self.consumables = set()  # Consumables like potions
        self.projectiles = set()  # Projectiles like arrows, bullets, etc.
        self.region_map = RegionMap(100, 100)  # 100x100 grid map for terrain

    @lru_cache(maxsize=None)
    def bus_path(self):
        z1 = random.randint(200_000, 800_000) # YES OFFICER THIS HARDCODE RIGHT HERE
        z2 = random.randint(200_000, 800_000)
        
        is_vertical = random.choice([True, False])
        
        if is_vertical:
            start_pos = Position(z1, 0)
            end_pos = Position(z2, self.dimensions.height)
        else:
            start_pos = Position(0, z1)
            end_pos = Position(self.dimensions.width, z2)
        
        if random.choice([True, False]):
            start_pos, end_pos = end_pos, start_pos

        return start_pos, end_pos


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
