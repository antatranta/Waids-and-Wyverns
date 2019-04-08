"""All utilities and classes for Initiative Tracking Graphical Display"""

import pygame

from .initiative import InitiativeTracker, CharacterInitiative
from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS
from .gui.utils import draw_text, Button
from .gui.utils import load_font


class InitiativeTrackerScreen(Screen):
    """Class to Start Graphical Initiative Tracker"""

    def __init__(self, tracker=None):
        super().__init__()
        self.tracker = tracker if tracker is not None else InitiativeTracker()

        self._namebox = TextBox((0, 0), (200, 30), "Bilbo")
        self._initiativebox = TextBox((0, 0), (60, 30), "1", allowed=NUMERIC_KEYS, center=True)
        self._healthbox = TextBox((0, 0), (60, 30), "2", allowed=NUMERIC_KEYS, center=True)
        self._add_button = Button("Add", (0, 0), (0, 0), self._add_character)
        self._entries = {}

    def _update(self):
        for char in self.tracker.character_order():
            if char not in self._entries:
                self._entries[char] = _InitiativeEntry(self.tracker, char)

        for char in self._entries:
            if char not in self._entries:
                del self._entries[char]

        self._add_button.enabled = self._valid_input()

    def _draw(self, screen):
        self._draw_initiative_order(screen, (10, 10))
        self._draw_input(screen, (10, screen.get_height() - self._namebox.rect.height - 10))

    def _handle_events(self, events):
        super()._handle_events(events)

        for char in self.tracker.character_order():
            self._entries[char].handle_events(events)

        self._namebox.handle_events(events)
        self._initiativebox.handle_events(events)
        self._healthbox.handle_events(events)
        self._add_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self._add_character()
                if event.key == pygame.K_ESCAPE:
                    self.close()

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

        self._add_button.rect = pygame.Rect(self._healthbox.rect.right + 10, pos[1], 100, 30)
        self._add_button.draw(screen)

    def _draw_initiative_order(self, screen, pos):
        x_pos, y_pos = pos
        for char in self.tracker.character_order():
            if char in self._entries:
                self._entries[char].pos = (x_pos, y_pos)
                self._entries[char].draw(screen)
                y_pos += 35

    def _valid_input(self):
        if not (self._namebox.value and self._initiativebox.value and self._healthbox.value):
            return False

        if not self._initiativebox.value.isdigit() or not self._healthbox.value.isdigit():
            return False

        return True

    def _add_character(self):
        if self._valid_input():
            char = CharacterInitiative(self._namebox.value,
                                       int(self._initiativebox.value),
                                       int(self._healthbox.value))

            self._namebox.value, self._initiativebox.value, self._healthbox.value = ('', '', '')
            self.tracker.add_character(char)

class _InitiativeEntry:
    # pylint: disable=too-many-instance-attributes

    def __init__(self, tracker, character):
        self.pos = (0, 0)
        self.tracker = tracker
        self.character = character
        self.remove_button = Button("remove", self.pos, (100, 30),
                                    self.tracker.remove_character, [self.character])

        self._namebox = _NameAttrBox(character, self.pos, (200, 30))
        self._initiativebox = _InitiativeAttrBox(character, self.pos, (60, 30), center=True)
        self._healthbox = _HealthAttrBox(character, self.pos, (60, 30), center=True)

        #self._font = pygame.font.SysFont('comicsansms', 18)
        self._font = load_font()

    def handle_events(self, events):
        """Handle pygame events for this object."""
        self._namebox.handle_events(events)
        self._initiativebox.handle_events(events)
        self._healthbox.handle_events(events)
        self.remove_button.handle_events(events)

    def draw(self, screen):
        """Draw this element to screen."""
        self._namebox.draw(screen)
        self._initiativebox.draw(screen)
        self._healthbox.draw(screen)

        self._namebox.rect.top = self.pos[1]
        self._initiativebox.rect.top = self.pos[1]
        self._healthbox.rect.top = self.pos[1]

        name_width, _ = draw_text(screen, self._font, "Name:", self.pos)
        self._namebox.rect.left = self.pos[0] + name_width

        initiative_width, _ = draw_text(
            screen, self._font, "Initiative:", (self._namebox.rect.right, self.pos[1]))
        self._initiativebox.rect.left = self._namebox.rect.right + initiative_width

        health_width, _ = draw_text(screen, self._font, "Health:",
                                    (self._initiativebox.rect.right, self.pos[1]))
        self._healthbox.rect.left = self._initiativebox.rect.right + health_width

        self.remove_button.rect.top = self.pos[1]
        self.remove_button.rect.left = self._healthbox.rect.right + 10
        self.remove_button.draw(screen)


class _AttributeBox(TextBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = str(self._get_attribute())

    def _get_attribute(self):
        raise NotImplementedError

    def _set_attribute(self, value):
        raise NotImplementedError

    def handle_events(self, events):
        super().handle_events(events)

        if not self.selected:
            self._set_attribute(self.value)


class _HealthAttrBox(_AttributeBox):

    def __init__(self, character, *args, **kwargs):
        self.character = character
        super().__init__(*args, allowed=NUMERIC_KEYS, **kwargs)

    def _get_attribute(self):
        return self.character.health

    def _set_attribute(self, value):
        self.character.health = int(value) if value != "" else 0


class _InitiativeAttrBox(_AttributeBox):

    def __init__(self, character, *args, **kwargs):
        self.character = character
        super().__init__(*args, allowed=NUMERIC_KEYS, **kwargs)

    def _get_attribute(self):
        return self.character.initiative

    def _set_attribute(self, value):
        self.character.initiative = int(value) if value != "" else 0


class _NameAttrBox(_AttributeBox):

    def __init__(self, character, *args, **kwargs):
        self.character = character
        super().__init__(*args, **kwargs)

    def _get_attribute(self):
        return self.character.name

    def _set_attribute(self, value):
        self.character.name = value
