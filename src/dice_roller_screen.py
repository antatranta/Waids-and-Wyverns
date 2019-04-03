"""All Utilities and Classes for Dice Roller Graphical Display"""

import pygame

from .gui.screen import Screen


class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._font = pygame.font.SysFont('comicsansms', 18)

    def _draw(self, screen):
        self.screen = screen
