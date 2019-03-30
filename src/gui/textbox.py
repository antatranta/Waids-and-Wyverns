"""Class for creating textboxes."""

import pygame

from .utils import draw_text


class TextBox:
    """Class for including a GUI TextBox."""

    def __init__(self, pos, size, initial_value=None, font=None):
        """
        Create an instance of TextBox.

        :param pos: Position (x, y) of top left corner of textbox.
        :param size: Size (width, height) in pixels of the textbox.
        :param initial_value: Initial value to set textbox too.
        :param font: Font to use for textbox.
        """
        self.rect = pygame.Rect(pos, size)
        self.value = initial_value if initial_value is not None else ""
        self.font = font if font is not None else pygame.font.SysFont('comicsansms', 18)
        self.selected = False

    def draw(self, screen):
        """Draw this element to screen."""
        border_color = (0, 0, 0) if self.selected else (220, 220, 220)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 1)

        draw_text(screen, self.font, self.value, (self.rect.left + 1, self.rect.top))

    def handle_events(self, events):
        """Handle events for this element."""
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = self.rect.collidepoint(pygame.mouse.get_pos())

            if not self.selected:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]
                elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    self.selected = False
                else:
                    width, _ = self.font.size(self.value + event.unicode)
                    if width < self.rect.width:
                        self.value += event.unicode
