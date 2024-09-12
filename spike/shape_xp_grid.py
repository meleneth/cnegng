import pygame
import random
import hashlib
import math

# Initialize Pygame
pygame.init()

# Constants for tuning
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Display size
COORDINATE_SPACE = 1_000_000  # Virtual space 1 million by 1 million
SCALE = SCREEN_WIDTH / COORDINATE_SPACE  # Scaling factor from virtual space to screen
FPS = 60
SHAPE_SIZE = 24  # Size of each sprite
NUM_SPRITES = 20_000  # Total number of sprites to render
NUM_TEXTURES = 10_000  # Number of pre-generated textures
GRAVITY_FORCE = 5000

# Color palette (limited to a few colors)
PALETTE = [
    (255, 99, 71),   # Tomato
    (135, 206, 235), # SkyBlue
    (152, 251, 152), # PaleGreen
    (255, 182, 193), # LightPink
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (173, 216, 230), # LightBlue
    (240, 128, 128), # LightCoral
    (124, 252, 0),   # LawnGreen
    (255, 69, 0)     # OrangeRed
]

def hash_name(name: str) -> int:
    """Hashes the name and returns an integer."""
    return int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16)

def generate_shape_from_hash(hash_value: int, surface: pygame.Surface):
    """Generates multiple shapes (1-6) based on the hash value."""
    random.seed(hash_value)
    num_shapes = random.randint(1, 6)
    
    for _ in range(num_shapes):
        color = PALETTE[random.randint(0, len(PALETTE) - 1)]
        shape_type = random.choice(['rect', 'circle', 'triangle'])

        if shape_type == 'rect':
            rect = pygame.Rect(random.randint(0, SHAPE_SIZE//2), random.randint(0, SHAPE_SIZE//2), 
                               random.randint(8, SHAPE_SIZE), random.randint(8, SHAPE_SIZE))
            pygame.draw.rect(surface, color, rect)
        
        elif shape_type == 'circle':
            radius = random.randint(4, SHAPE_SIZE//2)
            center = (random.randint(radius, SHAPE_SIZE - radius), random.randint(radius, SHAPE_SIZE - radius))
            pygame.draw.circle(surface, color, center, radius)
        
        elif shape_type == 'triangle':
            point1 = (random.randint(0, SHAPE_SIZE), random.randint(0, SHAPE_SIZE))
            point2 = (random.randint(0, SHAPE_SIZE), random.randint(0, SHAPE_SIZE))
            point3 = (random.randint(0, SHAPE_SIZE), random.randint(0, SHAPE_SIZE))
            pygame.draw.polygon(surface, color, [point1, point2, point3])

def create_sprite_from_name(name: str) -> pygame.Surface:
    """Creates a 24x24 sprite based on the given name."""
    sprite_surface = pygame.Surface((SHAPE_SIZE, SHAPE_SIZE), pygame.SRCALPHA)
    sprite_surface.fill((0, 0, 0, 0))  # Transparent background
    hash_value = hash_name(name)
    generate_shape_from_hash(hash_value, sprite_surface)
    return sprite_surface

class Position:
    """Represents the position of an object in 2D space (x, y)."""
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def add(self, other):
        """Adds a motion vector (or position) to the position to update it."""
        self.x += other.x
        self.y += other.y
    
    def __repr__(self):
        return f"Position(x={self.x:.2f}, y={self.y:.2f})"

class MotionVector:
    """Represents the motion of an object, including direction and speed."""
    def __init__(self, magnitude=0.0, direction=0.0):
        self._magnitude = float(magnitude)  # Speed of the vector
        self._direction = float(direction)  # Direction in radians
    
    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        """Sets the magnitude (speed), keeping direction the same."""
        self._magnitude = float(value)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        """Sets the direction in radians, keeping magnitude the same."""
        self._direction = float(value)
    
    @property
    def x(self):
        """Calculates the x component of the motion based on magnitude and direction."""
        return self._magnitude * math.cos(self._direction)
    
    @property
    def y(self):
        """Calculates the y component of the motion based on magnitude and direction."""
        return self._magnitude * math.sin(self._direction)
    
    def __repr__(self):
        return f"MotionVector(magnitude={self._magnitude:.2f}, direction={math.degrees(self._direction):.2f}°)"



class Grid:
    def __init__(self):
        self.cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.orphaned_objects = []
        self.current_group = 0  # Keeps track of which group of cells we're checking this frame

        # Initialize cells with bounds
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x_min = col * CELL_WIDTH
                x_max = (col + 1) * CELL_WIDTH
                y_min = row * CELL_HEIGHT
                y_max = (row + 1) * CELL_HEIGHT
                self.cells[row][col] = Cell(x_min, y_min, x_max, y_max)

        # Link neighbors for all cells
        self._link_neighbors()

    def _link_neighbors(self):
        """Link all neighboring cells for easier access."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.cells[row][col]

                # Wrapping indices for neighbors
                north_idx = (row - 1) % GRID_SIZE
                south_idx = (row + 1) % GRID_SIZE
                west_idx = (col - 1) % GRID_SIZE
                east_idx = (col + 1) % GRID_SIZE

                cell.north = self.cells[north_idx][col]
                cell.south = self.cells[south_idx][col]
                cell.west = self.cells[row][west_idx]
                cell.east = self.cells[row][east_idx]
                cell.northwest = self.cells[north_idx][west_idx]
                cell.northeast = self.cells[north_idx][east_idx]
                cell.southwest = self.cells[south_idx][west_idx]
                cell.southeast = self.cells[south_idx][east_idx]

    def get_cell(self, x, y):
        """Return the cell that contains point (x, y), wrapping coordinates."""
        x = x % WORLD_SIZE
        y = y % WORLD_SIZE
        col = int(x // CELL_WIDTH)
        row = int(y // CELL_HEIGHT)
        return self.cells[row][col]

    def add_object_to_cell(self, obj, x, y):
        """Add an object to the specified cell."""
        cell = self.get_cell(x, y)
        obj.current_cell = cell
        cell.add_object(obj)

    def remove_object_from_cell(self, obj):
        """Remove an object from its current cell."""
        if obj.current_cell is not None:
            obj.current_cell.remove_object(obj)

    def update_orphaned_objects(self):
        """Re-add orphaned objects to their correct cells after position updates."""
        for obj in self.orphaned_objects:
            self.add_object_to_cell(obj, obj.x, obj.y)
        self.orphaned_objects.clear()

    def _cells_in_range(self, x_min, y_min, x_max, y_max):
        """Yield all cells that overlap the given bounding box (x_min, y_min) to (x_max, y_max)."""
        # Handle world wrapping
        x_min = x_min % WORLD_SIZE
        y_min = y_min % WORLD_SIZE
        x_max = x_max % WORLD_SIZE
        y_max = y_max % WORLD_SIZE

        # Determine grid cell boundaries
        col_start = int(x_min // CELL_WIDTH)
        col_end = int(x_max // CELL_WIDTH)
        row_start = int(y_min // CELL_HEIGHT)
        row_end = int(y_max // CELL_HEIGHT)

        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                yield self.cells[row % GRID_SIZE][col % GRID_SIZE]

    def objects_in_radius(self, center_x, center_y, radius):
        """Return an iterator over all objects within a certain radius of (center_x, center_y)."""
        # Compute the bounding box that contains the circle
        x_min = center_x - radius
        y_min = center_y - radius
        x_max = center_x + radius
        y_max = center_y + radius

        radius_squared = radius ** 2

        for cell in self._cells_in_range(x_min, y_min, x_max, y_max):
            for obj in cell.nearby_occupants():
                # Check if the object is within the radius
                dx = (obj.x - center_x) % WORLD_SIZE
                dy = (obj.y - center_y) % WORLD_SIZE
                distance_squared = dx * dx + dy * dy
                if distance_squared <= radius_squared:
                    yield obj

    def check_group_for_escapes(self):
        """Check 1/8th of the grid cells for sprite escapes."""
        cells_per_group = GRID_SIZE * GRID_SIZE // 8
        start_idx = self.current_group * cells_per_group
        end_idx = start_idx + cells_per_group

        # Flatten the grid cells into a list for easier processing
        flat_cells = [cell for row in self.cells for cell in row]

        for cell in flat_cells[start_idx:end_idx]:
            for obj in list(cell.occupants):  # Copy the list to allow safe removal
                if not cell.contains(obj.x, obj.y):
                    self.orphaned_objects.append(obj)
                    cell.remove_object(obj)

        # Move to the next group of cells for the next frame
        self.current_group = (self.current_group + 1) % 8

    def all_objects(self):
        """Return an iterator that yields all objects in the grid."""
        for row in self.cells:
            for cell in row:
                for obj in cell.nearby_occupants():
                    yield obj


class Sprite:
    def __init__(self, texture: pygame.Surface):
        # Position in virtual coordinate space (1 million by 1 million)
        self.x = random.uniform(0, COORDINATE_SPACE)
        self.y = random.uniform(0, COORDINATE_SPACE)
        
        # Random direction (angle in radians)
        self.direction = random.uniform(0, 2 * math.pi)
        
        # Random speed
        self.speed = random.uniform(50, 4000)  # Virtual units per second
        
        # Sprite texture
        self.texture = texture
    
    def update(self, dt: float, gravity_direction: float):
        """Update the sprite's position based on its speed and direction."""
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

        # Apply gravity
        self.x += math.cos(gravity_direction) * GRAVITY_FORCE * dt
        self.y += math.sin(gravity_direction) * GRAVITY_FORCE * dt

        
        # Handle edge collision (wrapping by default)
        self.wrap()

    def wrap(self):
        """Wrap the sprite around when it goes off the edges."""
        if self.x < 0:
            self.x += COORDINATE_SPACE
        elif self.x > COORDINATE_SPACE:
            self.x -= COORDINATE_SPACE
        
        if self.y < 0:
            self.y += COORDINATE_SPACE
        elif self.y > COORDINATE_SPACE:
            self.y -= COORDINATE_SPACE

    def render(self, surface: pygame.Surface):
        """Render the sprite to the screen, scaling the virtual position to screen space."""
        screen_x = int(self.x * SCALE)
        screen_y = int(self.y * SCALE)
        surface.blit(self.texture, (screen_x, screen_y))

class Gravity:
    def __init__(self, switch_interval=4.0):
        self.current_direction = random.uniform(0, 2 * math.pi)  # Current gravity direction in radians
        self.target_direction = self.current_direction
        self.time_since_last_change = 0.0
        self.switch_interval = switch_interval  # How often to pick a new direction

    def update(self, dt: float):
        """Update the gravity direction, transitioning towards the target direction."""
        self.time_since_last_change += dt
        
        # Pick a new gravity direction every `switch_interval` seconds
        if self.time_since_last_change > self.switch_interval:
            self.target_direction = random.uniform(0, 2 * math.pi)
            self.time_since_last_change = 0.0
        
        # Smoothly transition to the new direction (linear interpolation)
        angle_diff = (self.target_direction - self.current_direction) % (2 * math.pi)
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        
        # Adjust the current direction based on the angle difference, at a rate of 0.5 radians per second
        self.current_direction += angle_diff * min(dt, 0.25)
        self.current_direction %= (2 * math.pi)

    def get_direction(self) -> float:
        """Return the current gravity direction."""
        return self.current_direction

class Cell:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.occupants = []  # List of sprites in the cell

    def add_object(self, obj):
        """Add an object (sprite) to this cell."""
        self.occupants.append(obj)

    def remove_object(self, obj):
        """Remove an object (sprite) from this cell."""
        self.occupants.remove(obj)

    def nearby_occupants(self):
        """Return an iterator over all occupants in this cell."""
        for occupant in self.occupants:
            yield occupant


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    
    # Generate 10,000 random textures
    textures = [create_sprite_from_name(f"item_{i}") for i in range(NUM_TEXTURES)]
    
    # Generate 20,000 sprites, each with a random texture from the 10,000
    sprites = [Sprite(random.choice(textures)) for _ in range(NUM_SPRITES)]

    # Initialize the global gravity system
    gravity = Gravity(switch_interval=4.0)
    center_gravity_direction = Gravity(switch_interval=6.0)

    grid = Grid()
    for sprite in sprites:
        grid.add_object_to_cell(sprite, sprite.x, sprite.y)
    
    while running:
        dt = clock.tick(FPS) / 1000.0  # Time passed per frame in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the gravity direction
        gravity.update(dt)
        center_gravity.update(dt)
        current_gravity_direction = gravity.get_direction()
        center_gravity_direction = center_gravity.get_direction()
        
        screen.fill((30, 30, 30))  # Dark background
        
        # Update and render all sprites
        for sprite in sprites:
            sprite.update(dt, current_gravity_direction)
            sprite.render(screen)

        for sprite in grid.objects_in_radius(COORDINATE_SPACE / 2, COORDINATE_SPACE / 2, COORDINATE_SPACE / 6):
            # technically a bug, since they get double updates but uh. shaddup
            sprite.update(dt, center_gravity_direction)

        grid.check_group_for_escapes()
        grid.update_orphaned_objects()
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

