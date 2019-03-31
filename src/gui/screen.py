"""Base class for creating a GUI screen."""

import sys
from abc import ABC, abstractmethod

import pygame


class Screen(ABC):
    """Base class for GUI screens."""

    screen_width = 640
    screen_height = 480
    frames_per_second = 60
    background_color = (155, 155, 155)

    def __init__(self):
        self.running = False

    def open(self):
        """Open this screen."""
        self.running = True
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Waids & Wyverns")
        frame_clock = pygame.time.Clock()

        while self.running:
            screen.fill(self.background_color)

            self._handle_events(pygame.event.get())
            self._draw(screen)

            pygame.display.flip()
            frame_clock.tick(self.frames_per_second)

    def close(self):
        """Close this screen."""
        self.running = False

    def _handle_events(self, events):
        """Handles the event input of mouse or keyboard."""
        # pylint: disable=no-self-use
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

    @abstractmethod
    def _draw(self, screen):
        """Draws this screen."""
        raise NotImplementedError


class ComponentScreen(Screen):
    """Screen implementation that includes all components."""

    def __init__(self, components):
        """
        Create an instance of ComponentScreen.

        Note:
        ALL components MUST implement:
        * draw(self, screen)
        * handle_events(self, events)

        Components will be drawn and handled in the
        same order they are added to the list.

        :param components: List of components to include in screen.
        """
        super().__init__()
        self.components = components

    def _draw(self, screen):
        for obj in self.components:
            obj.draw(screen)

    def _handle_events(self, events):
        super()._handle_events(events)
        for obj in self.components:
            obj.handle_events(events)
