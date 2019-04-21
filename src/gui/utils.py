"""Utilities for GUI related actions."""
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-branches

import math
import pygame


class Button:
    """Class to assist in creation of buttons."""

    def __init__(self, text, pos, size, action, params=None, enabled=True):
        """
        Initialize a single Button.

        :param text: Text to write on button.
        :parm pos: Position to place topleft corner of button (x, y).
        :parm size: Size of button (width, height).
        :parm action: Function to call when clicked.
        :parm params: Parameters to call action with when called.
        :parm enabled: Parameters to call action with when called.
        """
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.action = action
        self.params = params if params is not None else []
        self.enabled = enabled
        self._font = pygame.font.SysFont('comicsansms', 18)

    def draw(self, screen):
        """Draw this button to screen."""
        color = (255, 255, 255)
        text_color = (0, 0, 0) if self.enabled else (200, 200, 200)

        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.enabled:
            color = (220, 220, 220)

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, text_color, self.rect, 2)
        draw_text(screen, self._font, self.text, self.rect.center, center=True, color=text_color)

    def handle_events(self, events):
        """Handle events for this button."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
                if self.enabled:
                    self.action(*self.params)


class DragAndScaleMixin:
    """
    Mixin Class to allow objects to be draggable.

    Subclasses must have self.rect which is a pygame.Rect
    which will be used to know if the object has been clicked.

    Subclasses must have a self.img and self.full_res_img
    which are pygame.Surface in order to scale
    """

    def __init__(self, pos):
        self._draggable_selected = False
        self._draggable_offset = (0, 0)
        self._scalable_selected = False
        self._scalable_offset = (0, 0)
        self.pos = pos

    def handle_events(self, events):
        """Handle events for this element."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self._draggable_selected = False
                self._scalable_selected = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self._draggable_selected = True
                    self._draggable_offset = (self.pos[0] - event.pos[0],
                                              self.pos[1] - event.pos[1])

            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if self._draggable_selected:
                    self.pos = (self._draggable_offset[0] + event.pos[0],
                                self._draggable_offset[1] + event.pos[1])
                else:
                    self._draggable_selected = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.rect.collidepoint(event.pos) and not self._scalable_selected:
                    self._scalable_selected = True
                    self._scalable_offset = (event.pos[0], event.pos[1])

            elif event.type == pygame.MOUSEMOTION and event.buttons[2]:
                if self._scalable_selected:
                    new_width = math.floor(abs(self.size[0] +
                                               ((event.pos[0] - self._scalable_offset[0]) / 10)))
                    # so it doesnt shrink into nothingness
                    if new_width <= 25:
                        new_width = 25
                    # so it doesnt scale too big
                    elif new_width >= 800:
                        new_width = 800
                    new_height = new_width

                    self.size = (new_width, new_height)
                else:
                    self._scalable_selected = False


def load_font():
    """Ease of loading set font in"""
    myfont = pygame.font.SysFont('comicsansms', 18)
    return myfont


def draw_text(screen, font, text, pos, color=(0, 0, 0), *,
              background=None, center=False, split_char='\n'):
    """
    Draw text to screen.

    :param screen: Screen to draw text too.
    :param font: Font to use.
    :param text: Text to draw.
    :param pos: Position to draw text too.
    :param color: Color of the font.
    :param background: Color of the background.
    :param center: True if text should be centerd.
    :param split_char: Newline character.
    """
    # pylint: disable=invalid-name,too-many-locals
    x, y = pos
    max_width, total_height = (0, 0)

    for line in text.split(split_char):
        width, height = font.size(line)
        max_width = max(max_width, width)
        total_height += height

        surface = font.render(line, True, color, background)

        if center:
            screen.blit(surface, (x - int(width / 2), int(y - height / 2)))
        else:
            screen.blit(surface, (x, y))

        y += int(height)

    return max_width, total_height


def load_image(path, scale=None):
    """
    Load an image from some path.

    :param path: String path to the image.
    :param scale: Size (width, height) to scale image to.
    """
    image = pygame.image.load(path)
    if scale is not None:
        image = pygame.transform.smoothscale(image, scale)
    return image
