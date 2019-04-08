"""All Utilities and Classes for Dice Roller Graphical Display"""

import pygame

from .gui.screen import Screen
from .gui.utils import load_font

class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""

    def __init__(self):
        super().__init__()
        self._font = load_font();

    def _draw(self, screen):
        """draw function to draw necessary objects on screen"""
