import pygame
from functools import lru_cache

from cnegng.generations.two.region import RegionMap
from cnegng.generations.two.log_widget import LogWidget
from cnegng.generations.two.battle_royale import BattleRoyale
from cnegng.generations.one.base.tiny_shapes_base import TinyShapesBase
from cnegng.ACME.spatial2d.grid import GridSize
from cnegng.ACME.spatial2d import Grid
from cnegng.ACME.spatial2d import Area
from cnegng.ACME.spatial2d import Dimensions
from cnegng.ACME.spatial2d import Position, Motion
from cnegng.generations.one.palette import vibrant, without_red
from cnegng.generations.one import ShapeTexture
from cnegng.generations.two.sprite import Sprite
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
BRIGHT_BLUE = (0, 150, 255)
WHITE = (255, 255, 255)

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
class CachedDifficultyRenderer:
    def __init__(self, region_map : RegionMap, font_size=24):
        self.region_map = region_map
        self.difficulty_cache = None
        self.font_size = font_size
        self.font = pygame.freetype.SysFont(None, self.font_size)

    @lru_cache(maxsize=None)
    def difficulty_counts(self):
        """Calculate the difficulty counts and cache the results."""
        return self.region_map.difficulty_count()
            
    def render(self, screen, position : Position):
        """Render the difficulty list on the given screen."""
        
        # Render the list of difficulties
        for difficulty, count in self.difficulty_counts():
            # Get the color for the difficulty
            color = DIFFICULTY_COLORS.get(difficulty, (255, 255, 255))  # Default to white

            # Render the text using the freetype module
            text = f"Difficulty {difficulty}: {count} occurrences"
            self.font.render_to(screen, (position.x, position.y), text, color)

            # Move the next line down
            position.y += self.font_size + 5

    def clear_cache(self):
        """Clear the cached difficulty counts."""
        self.difficulty_cache = None

class MyBattleRoyale(TinyShapesBase):
    def setup_basic_helpers(self):
        self.logger = LogWidget(10, 10, 780, 200, player_lookup=self)
        self.logger("Reticulating Splines")
        self.textures = {}
        self.players = set()

        self.area = Area(
            position=Position(0, 0),
            dimensions=Dimensions(self.COORDINATE_SPACE, self.COORDINATE_SPACE),
        )
        self.grid = Grid(self.area, grid_size=GridSize(GRID_CELLS, GRID_CELLS))
        self.contest = BattleRoyale(self.area.dimensions)
        self.players_by_name = {}
        super().setup_basic_helpers()
        # area is expected to be setup by the time this is called
        self.area_to_minimap = self.area.scale_by(
            Area(top=400, left=0, bottom=900, right=500)
        )


    @lru_cache(maxsize=None)
    def difficulty_renderer(self):
        return CachedDifficultyRenderer(self.contest.region_map)

    def player_for_name(self, player_name):
        return self.players_by_name[player_name]

    def setup_basic_textures(self):
        pass

    def setup_basic_sprites(self):
        self.sprites = []

        shape_texture = ShapeTexture(palette=vibrant(), shape_size=SHAPE_SIZE)
        namer = ElvishNameGenerator()
        for _ in range(NUM_PLAYERS):
            name = f"{namer.generate_name()} {namer.generate_name()}"
            self.logger("".join(['creating a Player named {player:', name, '}']))
            if name not in self.textures:
                self.textures[name] = shape_texture.create_sprite_from_name(name)
            else:
                raise DuplicateName(f"Duplicate name({name}) that you never handled")
            sprite = Sprite(
                name=name,
                position=self.area.random_position_inside(),
                texture=self.textures[name],
                motion = Motion(direction=0, speed=0)
            )

            self.grid.add_to_cell(obj=sprite, coords=sprite.position, layer="player")
            self.players_by_name[sprite.name] = sprite
            self.players.add(sprite)
            self.sprites.append(sprite)

    def render(self) -> None:
        self.frame_no+=1
        self.draw_background()
        for sprite in self.sprites:
            # what happened to tell, don't ask?
            position = self.area_to_screen(sprite.position)
            self.surface.blit(sprite.texture, (position.x, position.y))
        self.logger.draw(self.surface)
        self.difficulty_renderer().render(self.surface, Position(860, 0))
        self.draw_bus_path()
        self.draw_minimap_player_dots()
        self.draw_bus()

    
    def draw_bus_path(self):
        if self.frame_no % 5 == 0:
            color = RED
        else:
            color = BRIGHT_BLUE
        start_pos, end_pos = self.contest.bus_path()
        self.draw_dashed_line(self.surface, color, self.area_to_minimap(start_pos), self.area_to_minimap(end_pos))

    def draw_bus(self):
        pass

    # Function to draw the background
    def draw_background(self):
        for x, y, terrain, difficulty in self.contest.region_map.all_regions():
            color = DIFFICULTY_COLORS[difficulty]
            pygame.draw.rect(self.surface, 
                             color, 
                             pygame.Rect(x*5, 
                                         y*5 + 400, 
                                         3, 
                                         3))  
            
    def draw_minimap_player_dots(self):
        for player in self.players:
            area_coords = self.area_to_minimap(player.position)
            pygame.draw.rect(self.surface, 
                    WHITE, 
                    pygame.Rect(area_coords.x, 
                                area_coords.y, 
                                4, 
                                4))

    # Function to draw a dashed line
    def draw_dashed_line(self, screen, color, start_pos : Position, end_pos : Position, dash_length=20):
        # Compute total distance and number of dashes
        dist_x = abs(end_pos.x - start_pos.x)
        dist_y = abs(end_pos.y - start_pos.y)
        
        dashes = int(start_pos.distance(end_pos) // dash_length)
        
        # Iterate through dashes
        for i in range(dashes):
            start_x = start_pos.x + (dist_x / dashes) * i
            start_y = start_pos.y + (dist_y / dashes) * i
            end_x = start_pos.x + (dist_x / dashes) * (i + 0.5)
            end_y = start_pos.y + (dist_y / dashes) * (i + 0.5)
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)


# Example usage of LogWidget
def main():
    br = MyBattleRoyale()
    br.run()
