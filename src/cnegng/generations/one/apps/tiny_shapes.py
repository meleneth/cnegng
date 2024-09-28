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
        self.special_direction = Motion(speed=GRAVITY_FORCE * 10)
        self.area = Area(
            position=Position(0, 0),
            dimensions=Dimensions(COORDINATE_SPACE, COORDINATE_SPACE),
        )
        self.area_to_screen = self.area.scale_by(
            Area(top=0, left=0, bottom=SCREEN_HEIGHT, right=SCREEN_WIDTH)
        )
        self.grid = Grid(self.area, grid_size=GridSize(GRID_CELLS, GRID_CELLS))
        shape_texture = ShapeTexture(palette=without_red(vibrant()), shape_size=SHAPE_SIZE)
        self.selected_shape_texture = ShapeTexture(palette=vibrant(), shape_size=SHAPE_SIZE)
        self.textures = {
            f"item_{i}": shape_texture.create_sprite_from_name(f"item_{i}")
            for i in range(NUM_TEXTURES)
        }
        self.selected_textures = {}
        self.selected_objects = set()
        self.every_few = GridIterator(grid=self.grid, mod_number=2)

        self.sprites = []
        # Generate 20,000 sprites, each with a random texture from the 10,000
        for _ in range(NUM_SPRITES):
            texture_name = random.choice(list(self.textures.keys()))
            sprite = Sprite(
                name=texture_name,
                position=self.area.random_position_inside(),
                texture=self.textures[texture_name],
            )

            self.grid.add_to_cell(obj=sprite, coords=sprite.position)
            self.sprites.append(sprite)
        self.outer_circle = Circle(
            center=Position(COORDINATE_SPACE / 2, COORDINATE_SPACE / 2), radius=200_000
        )

        self.inner_circle = Circle(
              center=Position(COORDINATE_SPACE / 2, COORDINATE_SPACE / 2), radius=100_000
        )

        self.change_global_motion()
        self.apply_extra_gravity()



    def change_global_motion(self):
        self.target_direction.randomize()
        self.timed_event_handler.add_event(4.0, self.change_global_motion)

    def apply_extra_gravity(self):
        down = Motion(direction=0, speed=100_000)
        updater = down.updater()
        circle_objects = set(self.grid.objects_in_circle(self.outer_circle))
        inner_circle_objects = {x for x in circle_objects if self.inner_circle.contains_position(x.position)}
        annulus_objects = circle_objects - inner_circle_objects
        self.update_selected_objects(annulus_objects)

        for cell in self.every_few.iterate():
            escaped_sprites = []
            for sprite in cell.all_members():
                if not cell.area.contains(sprite.position):
                    escaped_sprites.append(sprite)
            for sprite in escaped_sprites:
                cell.remove(sprite)
                if not self.grid.area.contains(sprite.position):
                    sprite.position = self.grid.area.wrap_within(sprite.position)
                self.grid.add_to_cell(obj=sprite, coords=sprite.position)
            
        self.timed_event_handler.add_event(0.1, self.apply_extra_gravity)

    def update_selected_objects(self, annulus_objects):
        objects_to_select = annulus_objects - self.selected_objects
        objects_to_unselect = self.selected_objects - annulus_objects
        for obj in objects_to_select:
            if obj.name not in self.selected_textures:
                self.create_selected_texture(obj)
            obj.texture = self.selected_textures[obj.name]
        for obj in objects_to_unselect:
            obj.texture = self.textures[obj.name]
        self.selected_objects = annulus_objects

    def create_selected_texture(self, obj):
        self.selected_textures[obj.name] = self.selected_shape_texture.create_sprite_from_name(obj.name)

    def update(self, dt: float) -> None:
        self.current_direction.lerp(self.target_direction, dt)
        global_motion_updater = self.current_direction.updater(dt)
        special_motion_updater = self.special_direction.updater(dt)
        special_area = Area(100_000, 100_000, 400_000, 400_000)
        for sprite in list(self.grid.objects_in_area(special_area)):
            sprite.position = special_motion_updater(sprite.position)
            sprite.position = special_area.wrap_within(sprite.position)
        for sprite in self.grid.all_objects():
            sprite.position = global_motion_updater(sprite.position)
            sprite.position = sprite.motion.move(sprite.position, dt)
        for sprite in self.selected_objects:
            sprite.position = self.outer_circle.move_along_arc(position=sprite.position, speed=5_000 * 8, dt=dt)


    def render(self) -> None:
        for sprite in self.sprites:
            # what happened to tell, don't ask?
            position = self.area_to_screen(sprite.position)
            self.surface.blit(sprite.texture, (position.x, position.y))


def main():
    game_handler = TinyShape()
    game_handler.run()
