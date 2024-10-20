import random

from cnegng.ACME.spatial2d.grid.grid_iterator import GridIterator
from cnegng.ACME.spatial2d.grid import GridSize
from cnegng.ACME.spatial2d import Grid
from cnegng.ACME.spatial2d import Area
from cnegng.ACME.spatial2d import Circle
from cnegng.ACME.spatial2d import Dimensions
from cnegng.ACME.spatial2d import Position
from cnegng.ACME.spatial2d import Motion
from cnegng.ACME import GameHandler
from cnegng.generations.one.palette import vibrant, without_red
from cnegng.generations.one import ShapeTexture
from cnegng.generations.one import Sprite

# Constants for tuning
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Display size
COORDINATE_SPACE = 1_000_000  # Virtual space 1 million by 1 million
FPS = 60
SHAPE_SIZE = 24  # Size of each sprite
NUM_SPRITES = 20_000  # Total number of sprites to render
NUM_TEXTURES = 10_000  # Number of pre-generated textures
GRAVITY_FORCE = 5000
GRID_CELLS = 20


class TinyShapesBase(GameHandler):
    def __init__(self):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SHAPE_SIZE = SHAPE_SIZE
        self.NUM_SPRITES = NUM_SPRITES
        self.NUM_TEXTURES = NUM_TEXTURES
        self.GRID_CELLS = GRID_CELLS
        self.GRAVITY_FORCE = GRAVITY_FORCE
        self.FPS = FPS
        self.COORDINATE_SPACE = COORDINATE_SPACE
        super().__init__(screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.setup_basic_helpers()
        self.setup_basic_textures()
        self.setup_basic_sprites()
        self.run_initial_timed_events()

    def setup_basic_helpers(self):
        # area is expected to be setup by the time this is called
        self.area_to_screen = self.area.scale_by(
            Area(top=0, left=0, bottom=SCREEN_HEIGHT, right=SCREEN_WIDTH)
        )

    def setup_basic_textures(self):
        pass

    def setup_basic_sprites(self):
        pass

    def update(self, dt: float) -> None:
        pass

    def run_initial_timed_events(self):
        pass

    def render(self) -> None:
        for sprite in self.sprites:
            # what happened to tell, don't ask?
            position = self.area_to_screen(sprite.position)
            self.surface.blit(sprite.texture, (position.x, position.y))
