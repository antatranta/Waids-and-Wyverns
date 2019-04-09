"""Class for creating textboxes."""
import re

import pygame

from .utils import draw_text
from .utils import load_font

ALPHA_KEYS = re.compile(r"[a-z]|[A-Z]")
NUMERIC_KEYS = re.compile(r"[0-9]")

class TextBox:
    """Class for including a GUI TextBox."""

    def __init__(self, pos, size, initial_value=None, font=None, *,
                 label=None, allowed=None, center=False):
        """
        Create an instance of TextBox.

        :param pos: Position (x, y) of top left corner of textbox.
        :param size: Size (width, height) in pixels of the textbox.
        :param initial_value: Initial value to set textbox too.
        :param font: Font to use for textbox.
        :param label: Label to place left of the textbox.
        :param allowed: Regex to match characters that can be typed in the textbox.
        :param center: If True center text in textbox.
        """
        self.rect = pygame.Rect(pos, size)
        self.value = initial_value if initial_value is not None else ""
        self.font = font if font is not None else load_font()
        self.label = label
        self.allowed = allowed
        self.center = center
        self.selected = False

    def _box_rect(self):
        box_rect = self.rect

        if self.label:
            label_width, _ = self.font.size(self.label)
            pos = (self.rect.left + label_width, self.rect.top)
            size = (self.rect.width - label_width, self.rect.height)
            box_rect = pygame.Rect(pos, size)

        return box_rect

    def draw(self, screen): # pragma: no cover
        """Draw this element to screen."""
        box_rect = self._box_rect()

        if self.label:
            draw_text(screen, self.font, self.label, self.rect.topleft)

        border_color = (0, 0, 0) if self.selected else (220, 220, 220)
        pygame.draw.rect(screen, (255, 255, 255), box_rect)
        pygame.draw.rect(screen, border_color, box_rect, 1)

        text_pos = box_rect.center if self.center else (box_rect.left + 1, box_rect.top)
        draw_text(screen, self.font, self.value, text_pos, center=self.center)

    def handle_events(self, events):
        """Handle events for this element."""
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = self._box_rect().collidepoint(pygame.mouse.get_pos())

            if not self.selected:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]
                elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    self.selected = False
                elif self.allowed is None or self.allowed.match(event.unicode):
                    width, _ = self.font.size(self.value + event.unicode)
                    if width < self.rect.width:
                        self.value += event.unicode
