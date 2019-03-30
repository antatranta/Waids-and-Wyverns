"""All utilities and classes for Initiative Tracking Graphical Display"""

import pygame

from .initiative import InitiativeTracker, CharacterInitiative
from .gui.screen import Screen
from .gui.textbox import TextBox
from .gui.utils import draw_text


class InitiativeTrackerScreen(Screen):
    """Class to Start Graphical Initiative Tracker"""

    def __init__(self, tracker=None):
        super().__init__()
        self.tracker = tracker if tracker is not None else InitiativeTracker()

        self._namebox = TextBox((0, 0), (200, 30), "Bilbo")
        self._initiativebox = TextBox((0, 0), (60, 30), "1")
        self._healthbox = TextBox((0, 0), (60, 30), "2")

        self._font = pygame.font.SysFont('comicsansms', 18)

    def _draw(self, screen):
        self._draw_input(screen, (10, 10))
        self._draw_initiative_order(screen, (10, 20 + self._namebox.rect.height))

    def _handle_events(self, events):
        super()._handle_events(events)
        self._namebox.handle_events(events)
        self._initiativebox.handle_events(events)
        self._healthbox.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self._add_character()

    def _draw_input(self, screen, pos):
        self._namebox.draw(screen)
        self._initiativebox.draw(screen)
        self._healthbox.draw(screen)

        self._namebox.rect.top = pos[1]
        self._initiativebox.rect.top = pos[1]
        self._healthbox.rect.top = pos[1]

        name_width, _ = draw_text(screen, self._font, "Name:", pos)
        self._namebox.rect.left = pos[0] + name_width

        initiative_width, _ = draw_text(
            screen, self._font, "Initiative:", (self._namebox.rect.right, pos[1]))
        self._initiativebox.rect.left = self._namebox.rect.right + initiative_width

        health_width, _ = draw_text(screen, self._font, "Health:",
                                    (self._initiativebox.rect.right, pos[1]))
        self._healthbox.rect.left = self._initiativebox.rect.right + health_width


    def _draw_initiative_order(self, screen, pos):
        text = "Initiative Order:\n"
        for char in self.tracker.character_order():
            text += f"Initiative: {char.initiative}, Name: {char.name}, Health: {char.health}\n"
        draw_text(screen, self._font, text, pos)

    def _add_character(self):
        if self._namebox.value and self._initiativebox.value and self._healthbox.value:
            char = CharacterInitiative(self._namebox.value,
                                       self._initiativebox.value,
                                       self._healthbox.value)

            self._namebox.value, self._initiativebox.value, self._healthbox.value = ('', '', '')
            self.tracker.add_character(char)
