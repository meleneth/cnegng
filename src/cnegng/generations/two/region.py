import random

from cnegng.generations.two.terrain import Terrain

class RegionMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = self.generate_map(width, height)

    def generate_map(self, width, height):
        # Create a 2D grid of terrain, start with difficulty 1 everywhere
        map = [[Terrain("grassland", 1) for _ in range(width)] for _ in range(height)]

        # Randomly paint regions with arcs and splatters to add variety
        for _ in range(100):  # Number of splatters
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            difficulty = random.randint(2, 9)
            self.spray_paint(map, x, y, difficulty)
        
        return map

    def spray_paint(self, map, x, y, difficulty):
        # Paint terrain around the given point in random arcs
        radius = random.randint(5, 15)  # Size of the arc
        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    if random.random() > 0.5:  # Random splatter effect
                        map[x + dx][y + dy] = Terrain("forest", difficulty)

    def terrain_at(self, position):
        # Return the terrain at a given (x, y) position
        x, y = position
        grid_x = min(max(0, int(x / 10000)), self.width - 1)
        grid_y = min(max(0, int(y / 10000)), self.height - 1)
        return self.map[grid_x][grid_y]

    def all_regions(self):
        """Generator to iterate over all regions in the map."""
        for grid_x in range(self.width):
            for grid_y in range(self.height):
                region = self.map[grid_y][grid_x]
                yield grid_x, grid_y, region.terrain_type, region.difficulty
