"""Class for creating textboxes."""
import re

import pygame

from .utils import draw_text, load_font

ALPHA_KEYS = re.compile(r"[a-z]|[A-Z]")
NUMERIC_KEYS = re.compile(r"[0-9]")
ARITHMETIC_KEYS = re.compile(r"[0-9]|-")
PRINTABLE_KEYS = re.compile((r"[0-9]|[a-z]|[A-Z]|\!|\"|#|\$|%|&|'|\(|\)|\|\*|\+|,|-|\."
                             r"|\/|:|;|<|=|>|\?|@|\[|\]|\\|\^|\_|\`|\{|\}|\~| "))

class TextBox:
    """Class for including a GUI TextBox."""
    # pylint: disable=too-many-instance-attributes

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

        self._unselect_keys = [pygame.K_RETURN, pygame.K_ESCAPE]

    def _box_rect(self):
        box_rect = self.rect

        if self.label:
            label_width, _ = self.font.size(self.label)
            pos = (self.rect.left + label_width, self.rect.top)
            size = (self.rect.width - label_width, self.rect.height)
            box_rect = pygame.Rect(pos, size)

        return box_rect

    def _text_limit(self, text):
        width, _ = self.font.size(text)
        return width > self.rect.width

    def draw(self, screen): # pragma: no cover
        """Draw this element to screen."""
        box_rect = self._box_rect()

        if self.label:
            draw_text(screen, self.font, self.label, self.rect.topleft)

        border_color = (0, 0, 0) if self.selected else (220, 220, 220)
        pygame.draw.rect(screen, (255, 255, 255), box_rect)
        pygame.draw.rect(screen, border_color, box_rect, 1)

        text_pos = box_rect.center if self.center else (box_rect.left + 1, box_rect.top)
        self._draw_text(screen, self.value, text_pos)

    def _draw_text(self, screen, text, text_pos):
        draw_text(screen, self.font, text, text_pos, center=self.center)

    def _insert_character(self, character):
        self.value += character

    def _delete_character(self):
        self.value = self.value[:-1]

    def handle_events(self, events):
        """Handle events for this element."""
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = self._box_rect().collidepoint(pygame.mouse.get_pos())

            if not self.selected:
                return

            if event.type == pygame.KEYDOWN:
                if event.key in self._unselect_keys:
                    self.selected = False
                elif event.key == pygame.K_BACKSPACE:
                    self._delete_character()
                elif self.allowed is None or self.allowed.match(event.unicode):
                    if not self._text_limit(self.value + event.unicode):
                        self._insert_character(event.unicode)


class TextArea(TextBox):
    """
    Class for including a GUI TextArea.

    TextAreas differ from TextBoxes in that they expect
    to contain multiple lines of text instead of a single line.
    """

    def __init__(self, pos, size, initial_value=None, font=None, *,
                 allowed=None, always_selected=False):
        """
        Create an instance of TextArea.

        :param pos: Position (x, y) of top left corner of textbox.
        :param size: Size (width, height) in pixels of the textbox.
        :param initial_value: Initial value to set textbox too.
        :param font: Font to use for textbox.
        :param allowed: Regex to match characters that can be typed in the textbox.
        :param always_selected: True if the textbox should always stay selected.
        """
        allowed = allowed if allowed is not None else PRINTABLE_KEYS
        super().__init__(pos, size, initial_value, font, allowed=allowed)
        self._always_selected = always_selected
        self.selected = always_selected
        self._unselect_keys = [pygame.K_ESCAPE]
        self._cursor_pos = len(self.value)

    def _text_limit(self, text):
        return False

    def _draw_text(self, screen, text, text_pos):
        char_x, char_y = text_pos
        for i, char in enumerate(text):
            char_width, char_height = self.font.size(char)

            if char == "\n" or char_x + char_width > self.rect.width:
                char_x = self.rect.left
                char_y += char_height

            if char != "\n":
                draw_text(screen, self.font, char, (char_x, char_y))
                char_x += char_width

            if i == self._cursor_pos - 1 and self.selected:
                pygame.draw.line(screen, (0, 0, 0),
                                 (char_x + 1, char_y), (char_x + 1, char_y + char_height))

    def _insert_character(self, character):
        self.value = self.value[:self._cursor_pos] + character + self.value[self._cursor_pos:]
        self._cursor_pos += 1

    def _delete_character(self):
        if self._cursor_pos > 0:
            self.value = self.value[:self._cursor_pos - 1] + self.value[self._cursor_pos:]
            self._cursor_pos -= 1

    def handle_events(self, events):
        super().handle_events(events)

        if self.selected and not self._always_selected:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN]:
                    self._insert_character("\n")

                if event.key == pygame.K_LEFT:
                    self._cursor_pos -= 1
                elif event.key == pygame.K_RIGHT:
                    self._cursor_pos += 1
                elif event.key == pygame.K_UP:
                    self._cursor_pos = 0
                elif event.key == pygame.K_DOWN:
                    self._cursor_pos = len(self.value)

        if self._always_selected:
            self.selected = True

        self._cursor_pos = min(self._cursor_pos, len(self.value))
        self._cursor_pos = max(self._cursor_pos, 0)
