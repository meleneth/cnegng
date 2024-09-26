import pygame
import math
from typing import Optional

from cnegng.ACME.spatial2d import Position
from cnegng.ACME.spatial2d import Motion


class Sprite:
    def __init__(self, name: str, texture: pygame.Surface, position: Optional[Position] = None):
        self.position = position
        if self.position is None:
            self.position = Position()
        self.motion = Motion()
        self.texture = texture
        self.current_cell = None
        self.name = name

    def __repr__(self):
        return f"Sprite(position={self.position}, motion={self.motion})"
