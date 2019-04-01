"""Main Menu Screen"""

import pygame

from .gui.utils import draw_text
from .gui.screen import Screen
from .initiative_screen import InitiativeTrackerScreen
from .map_screen import MapAndCharacterScreen


class MainMenuScreen(Screen):
    """Class to create a main menu screen."""

    def __init__(self):
        super().__init__()
        self._font = pygame.font.SysFont('comicsansms', 18)
        self._buttons = [
            ("Maps", pygame.Rect(220, 10, 200, 30), MapAndCharacterScreen().open),
            ("Initiative", pygame.Rect(220, 50, 200, 30), InitiativeTrackerScreen().open)]

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
