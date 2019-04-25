"""All Utilities and Classes for Dice Roller Graphical Display"""
# pylint: disable=too-many-instance-attributes

import re
import os
import pickle

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS, ARITHMETIC_KEYS
from .gui.utils import draw_text, Button, load_font
from .dice import roll_results, advantage_disadvantage


class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""

    macro_path = os.path.join(".", "assets", "macros", "macros.txt")
    custom_macro_path = os.path.join(".", "assets", "macros", "custom_macros.pkl")

    def __init__(self):
        super().__init__()

        y_pos = 0
        self._macro_output = None
        self._die_result = None
        self._advantage_result = None
        self._dice = [] # blank list
        self._dicesides = [4, 6, 8, 10, 12, 20, 100] # dices in order from smallest to largest
        self._macros = self._load_macros()

        if os.path.isfile(self.custom_macro_path):
            self._macros.update(pickle.load(open(self.custom_macro_path, "rb")))

        for sides in self._dicesides:
            # increment so that you can append to blank list
            self._dice.append(_Dice((0, y_pos), sides))
            y_pos += 50  # increase the y position so it's spaced out between the boxes when printed

        advantage_x, _ = self._font.size("D20 with:  ")
        self._advantage_button = Button("Advantage", (advantage_x, 350), (120, 30),
                                        self._roll_advantage)
        self._disadvantage_button = Button("Disadvantage", (advantage_x + 120, 350), (120, 30),
                                           self._roll_disadvantage)

        self._roll_button = Button("Roll", (50, 400), (150, 60), self._die_roll)
        self._reset_button = Button("Clear", (200, 400), (70, 60), self._reset_dice)

        self._macro_button = Button("Use", (300, 430), (150, 30), self._use_macro)
        self._save_macro_button = Button("Save", (450, 430), (150, 30), self._save_macro)
        self._macro_input = TextBox((300, 400), (300, 30), label="Macro: ")

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

        if self._macro_output is not None:
            self._draw_macro_result(screen, (480, 390))

        self._roll_button.draw(screen)
        self._reset_button.draw(screen)
        self._macro_button.draw(screen)
        self._save_macro_button.draw(screen)
        self._macro_input.draw(screen)

    def _die_roll(self):
        self._die_result = []
        for die in self._dice:
            times = int(die.input.value if die.input.value != "" else 0)
            modifier = int(die.modifier.value) if re.search(r"^-?\d+$", die.modifier.value) else 0
            self._die_result.append(roll_results(times, f"d{die.sides}",
                                                 die.modifier.value != "", modifier))

    def _reset_dice(self):
        self._die_result = None
        for die in self._dice:
            die.input.value = ""
            die.modifier.value = ""

    def _load_macros(self):
        macros = {}
        with open(self.macro_path, "r") as filestream:
            for line in filestream:
                macro_data = line.split(",")

                name = macro_data[0]
                dice_counts = [int(d) for d in macro_data[1:-1]]
                modifier = int(macro_data[-1])

                macros[name] = _Macro(name, dice_counts, modifier)
        return macros

    def _save_macro(self):
        name = self._macro_input.value
        dice_counts = [int(die.input.value or 0) for die in self._dice]
        modifier = sum([int(die.modifier.value) if re.search(r"^-?\d+$", die.modifier.value) else 0
                        for die in self._dice])

        if any(dice_counts):
            self._macros[name] = _Macro(name, dice_counts, modifier)
            pickle.dump(self._macros, open(self.custom_macro_path, "wb+"))
            self._macro_output = f'saved macro "{name}"'

    def _use_macro(self):
        macro_name = self._macro_input.value
        self._macro_output = f'Invalid macro "{macro_name}"'

        if macro_name in self._macros:
            self._macro_output = self._macros[macro_name].roll()

    def _roll_advantage(self):
        self._advantage_result = advantage_disadvantage(True, "d20")

    def _roll_disadvantage(self):
        self._advantage_result = advantage_disadvantage(False, "d20")

    def _handle_events(self, events):
        super()._handle_events(events)

        for die in self._dice:
            die.handle_events(events)

        self._roll_button.handle_events(events)
        self._reset_button.handle_events(events)
        self._macro_button.handle_events(events)
        self._save_macro_button.handle_events(events)
        self._advantage_button.handle_events(events)
        self._disadvantage_button.handle_events(events)
        self._macro_input.handle_events(events)

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

    def _draw_macro_result(self, screen, pos):
        draw_text(screen, self._font, self._macro_output, pos, center=True)


class _Dice:

    def __init__(self, pos, sides):
        self.pos = pos
        self.sides = sides
        self._font = load_font()

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

class _Macro:

    die_sides = [4, 6, 8, 10, 12, 20, 100]

    def __init__(self, name, dice_count, mod):
        self.name = name
        self.dice_count = dice_count
        self.mod = mod

    def roll(self):
        """Get string representing result of rolling this macro."""
        dice_rolls = []
        for times, sides in zip(self.dice_count, self.die_sides):
            dice_rolls.extend(roll_results(times, f"d{sides}", False, 0)[0])

        dice_rolls_string = " + ".join([str(roll) for roll in dice_rolls])
        return f"{dice_rolls_string} + ({self.mod}) = {sum(dice_rolls) + self.mod}"
