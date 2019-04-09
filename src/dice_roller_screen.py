"""All Utilities and Classes for Dice Roller Graphical Display"""
import re

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS, ARITHMETIC_KEYS
from .gui.utils import draw_text, Button
from .dice import roll_results


class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""

    def __init__(self):
        super().__init__()

        y_pos = 0

        self._die_result = None
        self._dice = [] # blank list
        self._dicesides = [4, 6, 8, 10, 12, 20, 100] # dices in order from smallest to largest
        for sides in self._dicesides:
            # increment so that you can append to blank list
            self._dice.append(_Dice((0, y_pos), sides))
            y_pos += 50 # increase the y position so it's spaced out between the boxes when printed

        self._roll_button = Button("Roll", (275, 400), (100, 50), self._die_roll)
        self._font = pygame.font.SysFont('comicsansms', 18)

    def _draw(self, screen):
        for die in self._dice:
            die.draw(screen)

        if self._die_result is not None:
            self._draw_results(screen, self._die_result, (350, 0))

        self._roll_button.draw(screen)

    def _die_roll(self):
        self._die_result = []
        for die in self._dice:
            times = int(die.input.value if die.input.value != "" else 0)
            modifier = int(die.modifier.value) if re.search(r"^-?\d+$", die.modifier.value) else 0
            self._die_result.append(roll_results(times, f"d{die.sides}",
                                                 die.modifier.value != "", modifier))

    def _valid_input(self):
        for i in range(len(self._dicesides)):
            if not self._dicesides[i].value:
                return False

            if not self._dicesides[i].value.isdigit():
                return False

        return True

    def _handle_events(self, events):
        super()._handle_events(events)

        for die in self._dice:
            die.handle_events(events)

        self._roll_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP: # if key is released
                self._roll_button.handle_events(events)
                if event.key == pygame.K_ESCAPE: # to check if it was the escape key
                    self.close()

    def _draw_results(self, screen, results, pos):
        output = ""
        for rolls, mod, total in results:
            if rolls:
                roll_sum = " + ".join([str(roll) for roll in rolls])
                output += f"{roll_sum} + ({mod}) = {total}"
            output += "\n\n"
        draw_text(screen, self._font, output, pos)


class _Dice:

    def __init__(self, pos, sides):
        self.pos = pos
        self.sides = sides
        self._font = pygame.font.SysFont('comicsansms', 18)

        self._mod_width, _ = self._font.size("Modifier:")  # returns something

        self.label = f"# of D{sides} dice: "
        text_width, _ = self._font.size(self.label)

        self.input = TextBox((pos[0] + text_width, pos[1]), (50, 30),
                             allowed=NUMERIC_KEYS, center=True)
        self.modifier = TextBox((self.input.rect.right + self._mod_width,
                                 pos[1]), (50, 30), allowed=ARITHMETIC_KEYS, center=True)

    def draw(self, screen):
        """Draw this component to screen."""
        draw_text(screen, self._font, self.label, self.pos)
        self.input.draw(screen)
        draw_text(screen, self._font, "Modifier:",
                  (self.modifier.rect.left - self._mod_width, self.pos[1]))
        self.modifier.draw(screen)

    def handle_events(self, events):
        """Handle events for this component."""
        self.input.handle_events(events)
        self.modifier.handle_events(events)
