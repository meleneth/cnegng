import random

from cnegng.ACME.spatial2d import Area
from cnegng.ACME.spatial2d import Dimensions
from cnegng.ACME.spatial2d import Position
from cnegng.ACME.spatial2d import Motion
from cnegng.ACME import GameHandler
from cnegng.generations.one.palette import vibrant
from cnegng.generations.one import ShapeTexture
from cnegng.generations.one import Sprite

# Constants for tuning
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Display size
COORDINATE_SPACE = 1_000_000  # Virtual space 1 million by 1 million
SCALE = SCREEN_WIDTH / COORDINATE_SPACE  # Scaling factor from virtual space to screen
FPS = 60
SHAPE_SIZE = 24  # Size of each sprite
NUM_SPRITES = 20_000  # Total number of sprites to render
NUM_TEXTURES = 10_000  # Number of pre-generated textures
GRAVITY_FORCE = 5000


class TinyShape(GameHandler):
    def __init__(self):
        super().__init__(screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.target_direction = Motion()
        self.current_direction = Motion(speed=GRAVITY_FORCE)
        self.area = Area(
            position=Position(0, 0),
            dimensions=Dimensions(COORDINATE_SPACE, COORDINATE_SPACE),
        )
        shape_texture = ShapeTexture(palette=vibrant(), shape_size=SHAPE_SIZE)
        textures = [
            shape_texture.create_sprite_from_name(f"item_{i}")
            for i in range(NUM_TEXTURES)
        ]

        # Generate 20,000 sprites, each with a random texture from the 10,000
        self.sprites = [
            Sprite(
                position=self.area.random_position_inside(),
                texture=random.choice(textures),
            )
            for _ in range(NUM_SPRITES)
        ]
        # self.grid = Grid(area=Area(), dimensions=Dimensions())
        # skip grid, it makes things hard

    def change_global_motion(self):
        self.target_direction.randomize()
        self.timed_event_handler.add_event(4.0, self.change_global_motion)

    def update(self, dt: float) -> None:
        self.current_direction.lerp(self.target_direction, dt)
        global_motion_updater = self.current_direction.updater(dt)
        for sprite in self.sprites:
            global_motion_updater(sprite.position)
            sprite.motion.move(sprite.position, self.dt)

    def render(self) -> None:
        for sprite in self.sprites:
            # what happened to tell, don't ask?
            screen_x = int(sprite.position.x * SCALE)
            screen_y = int(sprite.position.y * SCALE)
            self.surface.blit(sprite.texture, (screen_x, screen_y))


def main():
    game_handler = TinyShape()
    game_handler.run()
