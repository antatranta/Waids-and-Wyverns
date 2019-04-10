"""All Utilities and Classes for Notes Graphical Display"""

import pygame

from .gui.screen import Screen
from .gui.textbox import TextArea


class NotesScreen(Screen):
    """Class to open a notes screen"""

    def __init__(self):
        super().__init__()
        self._textarea = TextArea((0, 0), (self.screen_width, self.screen_height),
                                  always_selected=True, initial_value=(
                                      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed"
                                      "diam nonumy eirmod tempor invidunt ut labore et dolore magna"
                                      "aliquyam erat, sed diam voluptua. At vero eos et accusam et"
                                      "justo duo dolores et ea rebum. Stet clita kasd gubergren, no"
                                      "sea takimata sanctus est Lorem ipsum dolor sit amet."))

    def _draw(self, screen):
        self._textarea.draw(screen)

    def _handle_events(self, events):
        super()._handle_events(events)
        self._textarea.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
