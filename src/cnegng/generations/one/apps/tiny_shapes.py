import random

from cnegng.generations.one.base.tiny_shapes_base import TinyShapesBase
from cnegng.ACME.spatial2d.grid.grid_iterator import GridIterator
from cnegng.ACME.spatial2d.grid import GridSize
from cnegng.ACME.spatial2d import Grid
from cnegng.ACME.spatial2d import Area
from cnegng.ACME.spatial2d import Circle
from cnegng.ACME.spatial2d import Dimensions
from cnegng.ACME.spatial2d import Position
from cnegng.ACME.spatial2d import Motion
from cnegng.generations.one.palette import vibrant, without_red
from cnegng.generations.one import ShapeTexture
from cnegng.generations.one import Sprite

SHAPE_SIZE = 24  # Size of each sprite
NUM_SPRITES = 20_000  # Total number of sprites to render
NUM_TEXTURES = 10_000  # Number of pre-generated textures
GRAVITY_FORCE = 5000
GRID_CELLS = 20

class TinyShape(TinyShapesBase):
    def run_initial_timed_events(self):
        self.change_global_motion()
        self.update_annulus_selection()

    def setup_basic_helpers(self):
        self.target_direction = Motion()
        self.current_direction = Motion(speed=GRAVITY_FORCE)
        self.special_direction = Motion(speed=GRAVITY_FORCE * 10)
        self.area = Area(
            position=Position(0, 0),
            dimensions=Dimensions(self.COORDINATE_SPACE, self.COORDINATE_SPACE),
        )
        self.grid = Grid(self.area, grid_size=GridSize(GRID_CELLS, GRID_CELLS))
        self.selected_textures = {}
        self.selected_objects = set() # The Annulus
        self.every_few = GridIterator(grid=self.grid, mod_number=2)
        self.outer_circle = Circle(
            center=Position(self.COORDINATE_SPACE / 2, self.COORDINATE_SPACE / 2), radius=200_000
        )

        self.inner_circle = Circle(
              center=Position(self.COORDINATE_SPACE / 2, self.COORDINATE_SPACE / 2), radius=100_000
        )

        super().setup_basic_helpers()

    def setup_basic_textures(self):
        shape_texture = ShapeTexture(palette=without_red(vibrant()), shape_size=SHAPE_SIZE)
        self.selected_shape_texture = ShapeTexture(palette=vibrant(), shape_size=SHAPE_SIZE)
        self.textures = {
            f"item_{i}": shape_texture.create_sprite_from_name(f"item_{i}")
            for i in range(NUM_TEXTURES)
        }

    def setup_basic_sprites(self):
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

    def change_global_motion(self):
        self.target_direction.randomize()
        self.timed_event_handler.add_event(4.0, self.change_global_motion)

    def update_annulus_selection(self):
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
            
        self.timed_event_handler.add_event(0.1, self.update_annulus_selection)

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
        # The rectangular scrolling region
        for sprite in list(self.grid.objects_in_area(special_area)):
            sprite.position = special_motion_updater(sprite.position)
            sprite.position = special_area.wrap_within(sprite.position)
        # global and sprite-local movements
        for sprite in self.grid.all_objects():
            sprite.position = global_motion_updater(sprite.position)
            sprite.position = sprite.motion.move(sprite.position, dt)
        # annulus selection spinning
        for sprite in self.selected_objects:
            sprite.position = self.outer_circle.move_along_arc(position=sprite.position, speed=5_000 * 8, dt=dt)


def main():
    game_handler = TinyShape()
    game_handler.run()
