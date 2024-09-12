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
    
    while running:
        dt = clock.tick(FPS) / 1000.0  # Time passed per frame in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the gravity direction
        gravity.update(dt)
        current_gravity_direction = gravity.get_direction()
        
        screen.fill((30, 30, 30))  # Dark background
        
        # Update and render all sprites
        for sprite in sprites:
            sprite.update(dt, current_gravity_direction)
            sprite.render(screen)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

