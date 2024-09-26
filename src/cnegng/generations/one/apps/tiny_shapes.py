import random

from cnegng.ACME.spatial2d.grid import GridSize
from cnegng.ACME.spatial2d import Grid
from cnegng.ACME.spatial2d import Area
from cnegng.ACME.spatial2d import Circle
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
GRID_CELLS = 20


class TinyShape(GameHandler):
    def __init__(self):
        super().__init__(screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.target_direction = Motion()
        self.current_direction = Motion(speed=GRAVITY_FORCE)
        self.area = Area(
            position=Position(0, 0),
            dimensions=Dimensions(COORDINATE_SPACE, COORDINATE_SPACE),
        )
        self.area_to_screen = self.area.scale_by(
            Area(top=0, left=0, bottom=SCREEN_HEIGHT, right=SCREEN_WIDTH)
        )
        self.grid = Grid(self.area, grid_size=GridSize(GRID_CELLS, GRID_CELLS))
        shape_texture = ShapeTexture(palette=vibrant(), shape_size=SHAPE_SIZE)
        textures = [
            shape_texture.create_sprite_from_name(f"item_{i}")
            for i in range(NUM_TEXTURES)
        ]

        # Generate 20,000 sprites, each with a random texture from the 10,000
        for _ in range(NUM_SPRITES):
            sprite = Sprite(
                position=self.area.random_position_inside(),
                texture=random.choice(textures),
            )

            self.grid.add_to_cell(obj=sprite, coords=sprite.position)

        self.change_global_motion()
        self.apply_extra_gravity()

    def change_global_motion(self):
        self.target_direction.randomize()
        self.timed_event_handler.add_event(4.0, self.change_global_motion)

    def apply_extra_gravity(self):
        down = Motion(direction=0, speed=100_000)
        updater = down.updater()
        circle = Circle(
            center=Position(COORDINATE_SPACE / 2, COORDINATE_SPACE / 2), radius=200_000
        )
        for chosen_one in self.grid.objects_in_circle(circle):
            # DEMETER SAYS HWHAT
            chosen_one.owning_cell.remove(chosen_one)

        area = Area(top=500_000, left=500_000, right=600_000, bottom=600_000)
        # for chosen_one in self.grid.objects_in_area(area):
        #    chosen_one.current_cell.remove(chosen_one)
        #    chosen_one.position = updater(chosen_one.position)
        self.timed_event_handler.add_event(0.1, self.apply_extra_gravity)

    def update(self, dt: float) -> None:
        self.current_direction.lerp(self.target_direction, dt)
        global_motion_updater = self.current_direction.updater(dt)
        for sprite in self.grid.all_objects():
            sprite.position = global_motion_updater(sprite.position)
            sprite.position = sprite.motion.move(sprite.position, dt)

    def render(self) -> None:
        for sprite in self.grid.all_objects():
            # what happened to tell, don't ask?
            position = self.area_to_screen(sprite.position)
            self.surface.blit(sprite.texture, (position.x, position.y))


def main():
    game_handler = TinyShape()
    game_handler.run()
