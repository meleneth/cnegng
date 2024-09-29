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
        self.blur_map(map)
        self.blur_average(map)
        return map
    
    def blur_map(self, map, passes=10, blurriness=0.5):
        """Perform blurring passes to cluster similar difficulties."""
        for _ in range(passes):
            for x in range(self.width):
                for y in range(self.height):
                    # Get the current region's difficulty
                    current_region = map[x][y]
                    
                    # Choose a random neighboring region
                    neighbors = self.get_neighbors(x, y)
                    if neighbors:
                        neighbor_x, neighbor_y = random.choice(neighbors)
                        neighbor_region = map[neighbor_x][neighbor_y]
                        
                        # Swap difficulties based on the blurriness factor
                        if random.random() < blurriness:
                            current_region.difficulty, neighbor_region.difficulty = neighbor_region.difficulty, current_region.difficulty

    def blur_average(self, map, passes=5):
        """Perform averaging blur to smooth out difficulty values."""
        for _ in range(passes):
            # Create a copy of the current map difficulties
            new_difficulties = [[0 for _ in range(self.height)] for _ in range(self.width)]
            
            for x in range(self.width):
                for y in range(self.height):
                    # Get the current region and its neighbors
                    neighbors = self.get_neighbors(x, y, include_self=True)
                    
                    # Calculate the average difficulty of the neighbors, including the current cell
                    total_difficulty = 0
                    for nx, ny in neighbors:
                        total_difficulty += map[nx][ny].difficulty
                    
                    # Set the new difficulty to the rounded average
                    new_difficulties[x][y] = round(total_difficulty / len(neighbors))
            
            # Update the map with new smoothed difficulties
            for x in range(self.width):
                for y in range(self.height):
                    map[x][y].difficulty = new_difficulties[x][y]

    def get_neighbors(self, x, y, include_self=False):
        """Get the valid neighboring positions (up, down, left, right)."""
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))  # Left
        if x < self.width - 1:
            neighbors.append((x + 1, y))  # Right
        if y > 0:
            neighbors.append((x, y - 1))  # Up
        if y < self.height - 1:
            neighbors.append((x, y + 1))  # Down
        if include_self:
            neighbors.append((x, y))
        return neighbors

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
