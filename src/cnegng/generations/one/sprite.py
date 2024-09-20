import pygame
from typing import Optional

from cnegng.ACME.spatial2d import Position
from cnegng.ACME.spatial2d import Motion


class Sprite:
    def __init__(self, texture: pygame.Surface, position: Optional[Position] = None):
        self.position = position
        if self.position is None:
            self.position = Position()
        self.motion = Motion()
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
