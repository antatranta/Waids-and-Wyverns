"""All utilities and classes for Initiative Tracking Graphical Display"""

import sys
import pygame
import pygame.locals


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BACKGROUND_COLOR = (155, 155, 155)


class GUIScreen:
    """Class to Start GUI Main Screen"""
    def __init__(self, name, initiative, health):
        self.name = name
        self.initiative = initiative
        self.health = health

    def _handle_events(self):
        """ Handles the event input of mouse or keyboard """
        for event in pygame.event.get():
            # Handles main menu navigation with the mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # exit program when closing the window

    def _draw(self):
        # pylint: disable=arguments-differ
        """ Draws the main menu screen """
        self.screen.blit([0, 0])

        # Clock
        window_clock = pygame.time.Clock()

        stopped = False

        while not stopped:
            # Event Tasking
            # Add all your event tasking things here
            self._handle_events()

            pygame.display.update()
            window_clock.tick(60)

    def start_game(self):
        """Start Main Screen"""
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        while True:
            self._draw()
            self._handle_events()
            if self.end_game:
                self.quit()

            self._handle_events()

            # Clear screen
            screen.fill(BACKGROUND_COLOR)

    @classmethod
    def quit(cls):
        """Exit GUI Screen"""
        pygame.quit()
        sys.exit()
