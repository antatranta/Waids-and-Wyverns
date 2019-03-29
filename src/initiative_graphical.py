"""All utilities and classes for Initiative Tracking Graphical Display"""

import sys
import pygame
import pygame.locals


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BACKGROUND_COLOR = (155, 155, 155)
run = True

class GraphicalInitiativeTracker:
    """Class to Start Graphical Initiative Tracker"""
    def __init__(self, name, initiative, health):
        self.name = name
        self.initiative = initiative
        self.health = health

    def start_game(self):
        """Start Initiative Graphical"""
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(BACKGROUND_COLOR)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #self._handle_events()

            # Clear screen
            screen.fill(BACKGROUND_COLOR)

    def decrement_health(self, health):
        self.input = input("How much damage was dealt?")
        self.health = self.health - self.input

    @classmethod
    def quit(cls):
        """Exit Initiative Graphical"""
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ig = GraphicalInitiativeTracker("Reeeee", 14, 10)
    ig.start_game()
