import pygame

from cnegng.generations.two.log_widget import LogWidget
from cnegng.generations.two.battle_royale import BattleRoyale
from cnegng.generations.one.base.tiny_shapes_base import TinyShapesBase
from cnegng.ACME.spatial2d.grid.grid_iterator import GridIterator
from cnegng.ACME.spatial2d.grid import GridSize
from cnegng.ACME.spatial2d import Grid
from cnegng.ACME.spatial2d import Area
from cnegng.ACME.spatial2d import Circle
from cnegng.ACME.spatial2d import Dimensions
from cnegng.ACME.spatial2d import Position
from cnegng.generations.one.palette import vibrant, without_red
from cnegng.generations.one import ShapeTexture
from cnegng.generations.one import Sprite
from cnegng.generations.two.name_generators import ElvishNameGenerator

SHAPE_SIZE = 24  # Size of each sprite
GRID_CELLS = 20
NUM_PLAYERS = 100

class DuplicateName(Exception):
    pass

# Colors to interpolate between
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Number of difficulty levels (9 or 10)
DIFFICULTY_LEVELS = 9  # Change to 10 if necessary

# Hardcoded color palette for difficulty levels 1 to 9
DIFFICULTY_COLORS = {
    1: (0, 255, 0),     # Green
    2: (128, 255, 0),   # Light Green
    3: (192, 255, 0),   # Yellow-Green
    4: (255, 255, 0),   # Yellow
    5: (255, 192, 0),   # Light Yellow
    6: (255, 128, 64),  # Purple-Yellow
    7: (192, 64, 192),  # Light Purple
    8: (128, 0, 128),   # Purple
    9: (255, 0, 0)      # Red
}
class MyBattleRoyale(TinyShapesBase):
    def setup_basic_helpers(self):
        self.logger = LogWidget(10, 10, 780, 200)
        self.logger("Reticulating Splines")
        self.textures = {}

        self.area = Area(
            position=Position(0, 0),
            dimensions=Dimensions(self.COORDINATE_SPACE, self.COORDINATE_SPACE),
        )
        self.grid = Grid(self.area, grid_size=GridSize(GRID_CELLS, GRID_CELLS))
        self.contest = BattleRoyale()

        super().setup_basic_helpers()

    def setup_basic_textures(self):
        pass

    def setup_basic_sprites(self):
        self.sprites = []

        shape_texture = ShapeTexture(palette=without_red(vibrant()), shape_size=SHAPE_SIZE)
        namer = ElvishNameGenerator()
        # Generate 20,000 sprites, each with a random texture from the 10,000
        for _ in range(NUM_PLAYERS):
            name = f"{namer.generate_name()} {namer.generate_name()}"
            self.logger(f'creating a Player named {name}')
            if name not in self.textures:
                self.textures[name] = shape_texture.create_sprite_from_name(name)
            else:
                raise DuplicateName(f"Duplicate name({name}) that you never handled")
            sprite = Sprite(
                name=name,
                position=self.area.random_position_inside(),
                texture=self.textures[name],
            )

            self.grid.add_to_cell(obj=sprite, coords=sprite.position)

            self.sprites.append(sprite)

    def render(self) -> None:
        self.draw_background()
        for sprite in self.sprites:
            # what happened to tell, don't ask?
            position = self.area_to_screen(sprite.position)
            self.surface.blit(sprite.texture, (position.x, position.y))
        self.logger.draw(self.surface)

    # Function to draw the background
    def draw_background(self):
        for x, y, terrain, difficulty in self.contest.region_map.all_regions():
            color = DIFFICULTY_COLORS[difficulty]
            pygame.draw.rect(self.surface, 
                             color, 
                             pygame.Rect(x*10, 
                                         y*10, 
                                         10, 
                                         10))    

# Example usage of LogWidget
def main():
    br = MyBattleRoyale()
    br.run()
