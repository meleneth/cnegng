import pygame
import pygame.freetype
import re
from collections import deque

from cnegng.ACME.spatial2d import Position

class LogWidget:
    PLAYER_TAG_REGEX = r"\{player:(.*?)\}"  # Regex to match {player:playername}

    def __init__(self, x, y, width, height, player_lookup = None, font_size=24, max_messages=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.freetype.SysFont(None, font_size)  # Use freetype font
        self.messages = deque(maxlen=max_messages)
        self.bg_color = (0, 0, 0)  # Background color (black)
        self.text_color = (220, 220, 220)  # Text color (white)
        self.line_spacing = self.font.get_sized_height()  # Spacing between lines
        self.draw_background = False
        self.player_lookup = player_lookup

    def add_message(self, message):
        """Add a new message to the log"""
        self.messages.append(message)

    def draw(self, surface):
        """Draw the log widget onto the surface"""
        if self.draw_background:
            pygame.draw.rect(surface, self.bg_color, self.rect)  # Draw background
        y_offset = 0
        for message in self.messages:
            self._draw_message(surface, message, self.rect.x, self.rect.y + y_offset)
            y_offset += self.line_spacing  # Move to next line

    def _draw_message(self, surface, message, x, y):
        """Draw a message with potential player sprites onto the surface"""
        remaining_message = message
        cursor_x = x

        # Use regex to find all {player:playername} tags
        while True:
            match = re.search(self.PLAYER_TAG_REGEX, remaining_message)
            if not match:
                # If no match, just render the rest of the message
                self.font.render_to(surface, (cursor_x, y), remaining_message, self.text_color)
                break

            # Draw the text before the player tag
            pre_tag_text = remaining_message[:match.start()]
            if pre_tag_text:
                self.font.render_to(surface, (cursor_x, y), pre_tag_text, self.text_color)
                cursor_x += self.font.get_rect(pre_tag_text).width

            # Handle the player tag and fetch the player sprite
            player_name = match.group(1)
            player_sprite = self.player_lookup.player_for_name(player_name)
            print(f"player sprite is {player_sprite.name}")
            if player_sprite:
                # Draw the player's sprite before their name
                player_sprite.draw_at(surface, Position(cursor_x, y))  # Assuming the sprite has a `draw` method
                cursor_x += player_sprite.get_width()  # Adjust cursor for sprite width

            # Draw the player name text
            self.font.render_to(surface, (cursor_x, y), player_name, self.text_color)
            cursor_x += self.font.get_rect(player_name).width

            # Continue processing the rest of the message after the tag
            remaining_message = remaining_message[match.end():]


    def __call__(self, message):
        self.add_message(message)
