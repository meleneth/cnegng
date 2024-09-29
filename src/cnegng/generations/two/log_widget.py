import pygame
import pygame.freetype
from collections import deque

class LogWidget:
    def __init__(self, x, y, width, height, font_size=24, max_messages=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.freetype.SysFont(None, font_size)  # Use freetype font
        self.messages = deque(maxlen=max_messages)
        self.bg_color = (0, 0, 0)  # Background color (black)
        self.text_color = (255, 255, 255)  # Text color (white)
        self.line_spacing = self.font.get_sized_height()  # Spacing between lines
        self.draw_background = False

    def add_message(self, message):
        """Add a new message to the log"""
        self.messages.append(message)

    def draw(self, surface):
        """Draw the log widget onto the surface"""
        if self.draw_background:
            pygame.draw.rect(surface, self.bg_color, self.rect)  # Draw background
        y_offset = 0
        for message in self.messages:
            self.font.render_to(surface, (self.rect.x + 10, self.rect.y + y_offset), message, self.text_color)
            y_offset += self.line_spacing  # Move to next line

    def __call__(self, message):
        self.add_message(message)
