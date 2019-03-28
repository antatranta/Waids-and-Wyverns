"""All utilities and classes for Initiative Tracking Graphical Display"""

import sys
import pygame
import pygame.locals


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BACKGROUND_COLOR = (155, 155, 155)

class GraphicalInitiativeTracker:
    """Class to Start Graphical Initiative Tracker"""
    def __init__(self, name, initiative, health):
        self.name = name
        self.initiative = initiative
        self.health = health

    def start_game(self):
        """Start Initiative Graphical"""
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        while True:
            if self.end_game:
                self.quit()

            self._handle_events()

            # Clear screen
            screen.fill(BACKGROUND_COLOR)

    @classmethod
    def quit(cls):
        """Exit Initiative Graphical"""
        pygame.quit()
        sys.exit()
