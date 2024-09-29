class Terrain:
    def __init__(self, type, difficulty):
        self.type = type  # Type of terrain, e.g., forest, mountain
        self.difficulty = difficulty  # Difficulty rating (1-10)
    
    def apply_effect(self, entity):
        # Apply effects based on the type of terrain
        pass
