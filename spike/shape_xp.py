import pygame
import random
import hashlib

# Initialize Pygame
pygame.init()


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
SHAPE_SIZE = 24

# Color palette (limited to a few colors)
PALETTE = [
    (255, 99, 71),  # Tomato
    (135, 206, 235),  # SkyBlue
    (152, 251, 152),  # PaleGreen
    (255, 182, 193),  # LightPink
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (173, 216, 230),  # LightBlue
    (240, 128, 128),  # LightCoral
    (124, 252, 0),  # LawnGreen
    (255, 69, 0),  # OrangeRed
]


def hash_name(name: str) -> int:
    """Hashes the name and returns an integer."""
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16)


def generate_shape_from_hash(hash_value: int, surface: pygame.Surface):
    """Generates multiple shapes (1-6) based on the hash value."""
    random.seed(hash_value)

    # Decide how many shapes (between 1 and 6) to draw for the sprite
    num_shapes = random.randint(1, 6)

    for _ in range(num_shapes):
        color = PALETTE[random.randint(0, len(PALETTE) - 1)]
        shape_type = random.choice(["rect", "circle", "triangle"])

        if shape_type == "rect":
            rect = pygame.Rect(
                random.randint(0, SHAPE_SIZE // 2),
                random.randint(0, SHAPE_SIZE // 2),
                random.randint(8, SHAPE_SIZE),
                random.randint(8, SHAPE_SIZE),
            )
            pygame.draw.rect(surface, color, rect)

        elif shape_type == "circle":
            radius = random.randint(4, SHAPE_SIZE // 2)
            center = (
                random.randint(radius, SHAPE_SIZE - radius),
                random.randint(radius, SHAPE_SIZE - radius),
            )
            pygame.draw.circle(surface, color, center, radius)

        elif shape_type == "triangle":
            point1 = (random.randint(0, SHAPE_SIZE), random.randint(0, SHAPE_SIZE))
            point2 = (random.randint(0, SHAPE_SIZE), random.randint(0, SHAPE_SIZE))
            point3 = (random.randint(0, SHAPE_SIZE), random.randint(0, SHAPE_SIZE))
            pygame.draw.polygon(surface, color, [point1, point2, point3])


def create_sprite_from_name(name: str) -> pygame.Surface:
    """Creates a 24x24 sprite based on the given name."""

    sprite_surface = pygame.Surface((SHAPE_SIZE, SHAPE_SIZE))
    sprite_surface.fill((0, 0, 0))  # Black background
    hash_value = hash_name(name)
    generate_shape_from_hash(hash_value, sprite_surface)
    return sprite_surface


# Demo Application
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    running = True

    # Generate 10,000 random sprites
    sprites = [create_sprite_from_name(f"item_{i}") for i in range(10000)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))  # Dark background

        # Draw the sprites randomly on the screen
        for i in range(10000):
            x = random.randint(0, SCREEN_WIDTH - SHAPE_SIZE)
            y = random.randint(0, SCREEN_HEIGHT - SHAPE_SIZE)

            screen.blit(sprites[i], (x, y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
