"""All Utilities and Classes for Dice Roller Graphical Display"""

import pygame

from .dice_roller import DiceRoller
from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS
from .gui.utils import draw_text


class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""
    def __init__(self):
        super().__init__()
        self._font = pygame.font.SysFont('comicsansms', 18)

    def _draw(self, screen):
        self.screen = screen
