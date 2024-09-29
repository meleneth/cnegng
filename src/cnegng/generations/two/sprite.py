class Sprite:
    def __init__(self, position, motion, texture, layer):
        self.position = position  # Position in the world
        self.motion = motion  # Motion vector or movement logic
        self.texture = texture  # Visual representation
        self.layer = layer  # Rendering layer
        self.enemies = set()  # Set of enemies currently interacting with
        self.lookers = set() # why you over there looking at me
        self.nearby_friends = set()
        self.current_target = None  # Current target (could be an enemy, object, etc.)

    def update(self, dt):
        # Apply motion updates to position
        self.position = self.motion.move(self.position, dt)
    
    def set_target(self, target):
        self.current_target = target
    
    def remove_target(self):
        self.current_target = None
