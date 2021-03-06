"""All Utilities and Classes for Notes Graphical Display"""
import os
import pygame

from .gui.screen import Screen
from .gui.textbox import TextArea


class NotesScreen(Screen):
    """Class to open a notes screen"""

    def __init__(self):
        super().__init__()
        self.notes_path = os.path.join(".", "assets", "media", "notes", "notes.txt")
        self.file = open(self.notes_path, "r" if os.path.exists(self.notes_path) else "w+")
        self._textarea = TextArea((0, 0), (self.screen_width, self.screen_height),
                                  always_selected=True, initial_value=self.file.read())
        self.file.close()

    def _draw(self, screen):
        self._textarea.draw(screen)

    def _handle_events(self, events):
        super()._handle_events(events)
        self._textarea.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.file = open(self.notes_path, "w")
                    self.file.write(self._textarea.value)
                    self.file.close()
                    self.close()
