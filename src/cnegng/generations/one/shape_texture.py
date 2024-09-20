import random
import hashlib
import pygame


class ShapeTexture:
    def __init__(self, palette, min_shapes=1, max_shapes=5, shape_size=24):
        self.palette = palette
        self.min_shapes = min_shapes
        self.max_shapes = max_shapes
        self.shape_size = shape_size

    def hash_name(self, name: str) -> int:
        """Hashes the name and returns an integer."""
        return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16)

    def generate_shape_from_hash(self, hash_value: int, surface: pygame.Surface):
        """Generates multiple shapes (1-6) based on the hash value."""
        random.seed(hash_value)
        num_shapes = random.randint(self.min_shapes, self.max_shapes + 1)

        for _ in range(num_shapes):
            color = random.choice(self.palette)
            shape_type = random.choice(["rect", "circle", "triangle"])

            if shape_type == "rect":
                rect = pygame.Rect(
                    random.randint(0, self.shape_size // 2),
                    random.randint(0, self.shape_size // 2),
                    random.randint(8, self.shape_size),
                    random.randint(8, self.shape_size),
                )
                pygame.draw.rect(surface, color, rect)

            elif shape_type == "circle":
                radius = random.randint(4, self.shape_size // 2)
                center = (
                    random.randint(radius, self.shape_size - radius),
                    random.randint(radius, self.shape_size - radius),
                )
                pygame.draw.circle(surface, color, center, radius)

            elif shape_type == "triangle":
                point1 = (
                    random.randint(0, self.shape_size),
                    random.randint(0, self.shape_size),
                )
                point2 = (
                    random.randint(0, self.shape_size),
                    random.randint(0, self.shape_size),
                )
                point3 = (
                    random.randint(0, self.shape_size),
                    random.randint(0, self.shape_size),
                )
                pygame.draw.polygon(surface, color, [point1, point2, point3])

    def create_sprite_from_name(self, name: str) -> pygame.Surface:
        """Creates a 24x24 sprite based on the given name."""
        sprite_surface = pygame.Surface(
            (self.shape_size, self.shape_size), pygame.SRCALPHA
        )
        sprite_surface.fill((0, 0, 0, 0))  # Transparent background
        hash_value = self.hash_name(name)
        self.generate_shape_from_hash(hash_value, sprite_surface)
        return sprite_surface
