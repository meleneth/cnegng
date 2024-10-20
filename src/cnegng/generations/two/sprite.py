from cnegng.ACME.spatial2d import Position, Motion


class Sprite:
    def __init__(
        self,
        position: Position,
        motion: Motion,
        texture=None,
        layer="default",
        name="defaultName",
    ):
        self.name = name
        self.position = position  # Position in the world
        self.motion = motion  # Motion vector or movement logic
        self.texture = texture  # Visual representation
        self.layer = layer  # Rendering layer
        self.enemies = set()  # Set of enemies currently interacting with
        self.lookers = set()  # why you over there looking at me
        self.nearby_friends = set()
        self.current_target = None  # Current target (could be an enemy, object, etc.)

    def get_width(self):
        return 24  # oh you ARE a naughty boy

    def update(self, dt):
        # Apply motion updates to position
        self.position = self.motion.move(self.position, dt)

    def set_target(self, target):
        self.current_target = target

    def remove_target(self):
        self.current_target = None

    def draw_at(self, surface, position):
        surface.blit(self.texture, (position.x, position.y))
