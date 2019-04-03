"""Main Menu Screen"""

import pygame

from .gui.utils import draw_text
from .gui.screen import Screen
from .initiative_screen import InitiativeTrackerScreen
from .map_screen import MapAndCharacterScreen
from .dice_roller_screen import DiceRollerScreen


class MainMenuScreen(Screen):
    """Class to create a main menu screen."""

    def __init__(self):
        super().__init__()
        self._font = pygame.font.SysFont('comicsansms', 18)
        self._buttons = [
            ("Maps", pygame.Rect(super().screen_width / 2 - 200, 10, 400, 30),
             MapAndCharacterScreen().open),
            ("Initiative",
             pygame.Rect(super().screen_width / 2 - 200, 50, 400, 30),
             InitiativeTrackerScreen().open),
            ("Dice Roller",
             pygame.Rect(super().screen_width / 2 - 200, 90, 400, 30),
             DiceRollerScreen().open)]

    def _draw(self, screen):
        for text, rect, _ in self._buttons:
            pygame.draw.rect(screen, (255, 255, 255), rect)
            draw_text(screen, self._font, text, rect.center, center=True)

    def _handle_events(self, events):
        super()._handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for _, rect, action in self._buttons:
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        action()
                        break
