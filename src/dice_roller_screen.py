"""All Utilities and Classes for Dice Roller Graphical Display"""
import re

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS, ARITHMETIC_KEYS
from .gui.utils import draw_text, Button
from .dice import roll_results, advantage_disadvantage


class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""

    def __init__(self):
        super().__init__()

        y_pos = 0

        self._die_result = None
        self._advantage_result = None
        self._dice = [] # blank list
        self._dicesides = [4, 6, 8, 10, 12, 20, 100] # dices in order from smallest to largest

        for sides in self._dicesides:
            # increment so that you can append to blank list
            self._dice.append(_Dice((0, y_pos), sides))
            y_pos += 50 # increase the y position so it's spaced out between the boxes when printed

        advantage_x, _ = self._font.size("D20 with:  ")
        self._advantage_button = Button("Advantage", (advantage_x, 350), (120, 30),
                                        self._roll_advantage)
        self._disadvantage_button = Button("Disadvantage", (advantage_x + 120, 350), (120, 30),
                                           self._roll_disadvantage)

        self._roll_button = Button("Roll", (75, 400), (100, 50), self._die_roll)
        self._save_button = Button("Save?", (250, 400), (100, 50), self._save_macro)
        self.input = TextBox((380, 400), (200, 50), "Macro Name?")

    def _draw(self, screen):
        for die in self._dice:
            die.draw(screen)

        if self._die_result is not None:
            self._draw_results(screen, self._die_result, (350, 0))

        draw_text(screen, self._font, "D20 with:  ", (0, self._advantage_button.rect.top))
        self._advantage_button.draw(screen)
        self._disadvantage_button.draw(screen)

        if self._advantage_result:
            results_x = self._disadvantage_button.rect.right + 10
            self._draw_advantage_result(screen, self._advantage_result,
                                        (results_x, self._disadvantage_button.rect.top))

        self._roll_button.draw(screen)
        self._save_button.draw(screen)
        self.input.draw(screen)

    def _die_roll(self):
        self._die_result = []
        for die in self._dice:
            times = int(die.input.value if die.input.value != "" else 0)
            modifier = int(die.modifier.value) if re.search(r"^-?\d+$", die.modifier.value) else 0
            self._die_result.append(roll_results(times, f"d{die.sides}",
                                                 die.modifier.value != "", modifier))

    def _save_macro(self):
        self._die_result = []
        for die in self._dice:
            times = int(die.input.value if die.input.value != "" else 0)
            modifier = int(die.modifier.value) if re.search(r"^-?\d+$", die.modifier.value) else 0
            self._die_result.append(roll_results(times, f"d{die.sides}",
                                                 die.modifier.value != "", modifier))
        with open("macros.txt", 'w', encoding='utf-8') as f:
            f.write("my first file\n")
            f.write("This file\n\n")
            f.write("contains three lines\n")
            f.write(str(self._dice_results))

    def _roll_advantage(self):
        self._advantage_result = advantage_disadvantage(True, "d20")

    def _roll_disadvantage(self):
        self._advantage_result = advantage_disadvantage(False, "d20")

    def _handle_events(self, events):
        super()._handle_events(events)

        for die in self._dice:
            die.handle_events(events)

        self._roll_button.handle_events(events)
        #self._save_macro.handle_events(events)
        self._advantage_button.handle_events(events)
        self._disadvantage_button.handle_events(events)

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

    def _draw_advantage_result(self, screen, results, pos):
        rolls, value = results
        draw_text(screen, self._font, f"{rolls[0]} vs {rolls[1]} => {value}", pos)


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