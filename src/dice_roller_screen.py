"""All Utilities and Classes for Dice Roller Graphical Display"""

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS
from .gui.utils import draw_text


class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""

    def __init__(self):
        super().__init__()

        self._d4box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d6box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d8box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d10box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d100box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d12box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d20box = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)

        self._d4_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d6_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d8_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d10_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d100_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d12_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)
        self._d20_modifier = TextBox((0, 0), (50, 30), "0", allowed=NUMERIC_KEYS, center=True)

        self._roll_button = pygame.Rect(0, 0, 0, 0)
        self._font = pygame.font.SysFont('comicsansms', 18)

    def _draw(self, screen):
        """draw function to draw necessary objects on screen"""
        self._draw_input(screen, (10, 10))

    def _handle_events(self, events):
        super()._handle_events(events)
        
        self._d4box.handle_events(events)
        self._d6box.handle_events(events)
        self._d8box.handle_events(events)
        self._d10box.handle_events(events)
        self._d12box.handle_events(events)
        self._d20box.handle_events(events)
        self._d100box.handle_events(events)

        self._d4_modifier.handle_events(events)
        self._d6_modifier.handle_events(events)
        self._d8_modifier.handle_events(events)
        self._d10_modifier.handle_events(events)
        self._d12_modifier.handle_events(events)
        self._d20_modifier.handle_events(events)
        self._d100_modifier.handle_events(events)


        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self._roll_button.collidepoint(pygame.mouse.get_pos()):
                    print("roll")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self._roll_result(1, 2, 3, 4, 5, 6)
                if event.key == pygame.K_ESCAPE:
                    self.close()

    def _valid_input(self):
        if not (self._d4box.value and self._d6box.value and self._d8box.value and self._d10box and self._d100box and self._d12box and self._d20box):
            return False

        if not (self._d4box.value.isdigit() or self._d6box.value.isdigit() or self._d10box.value.isdigit() or self._d100box.value.isdigit() or self._d12box.value.isdigit() or self._d20box.value.isdigit()):
            return False

        return True

    def _roll_result(d4_val, d6_val, d8_val, d10_val, d12_val, d20_val, d100_val):
        print("test")

    def _draw_input(self, screen, pos):
        self._d4box.draw(screen)
        self._d6box.draw(screen)
        self._d8box.draw(screen)
        self._d10box.draw(screen)
        self._d100box.draw(screen)
        self._d12box.draw(screen)
        self._d20box.draw(screen)

        d4_width, _ = draw_text(screen, self._font, "# of D4 dice: ", (10, 0))
        self._d4box.rect.left = d4_width + 10

        d6_width, _ = draw_text(screen, self._font, "# of D6 dice: ", (10, 50))
        self._d6box.rect.left = d6_width + 10
        self._d6box.rect.bottom = 75

        d8_width, _ = draw_text(screen, self._font, "# of D8 dice: ", (10, 100))
        self._d8box.rect.left = d8_width + 10
        self._d8box.rect.bottom = 125

        d10_width, _ = draw_text(screen, self._font, "# of D10 dice: ", (10, 150))
        self._d10box.rect.left = d10_width + 10
        self._d10box.rect.bottom = 175

        d12_width, _ = draw_text(screen, self._font, "# of D12 dice: ", (10, 200))
        self._d12box.rect.left = d12_width  + 10
        self._d12box.rect.bottom = 225

        d20_width, _ = draw_text(screen, self._font, "# of D20 dice: ", (10, 250))
        self._d20box.rect.left = d20_width + 10
        self._d20box.rect.bottom = 275

        d100_width, _ = draw_text(screen, self._font, "# of D100 dice: ", (10, 300))
        self._d100box.rect.left = d100_width + 10
        self._d100box.rect.bottom = 325

        self._roll_button = pygame.Rect(250, 400, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), self._roll_button)

        add_color = (0, 0, 0) if self._valid_input() else (200, 200, 200)
        draw_text(screen, self._font, "Roll", self._roll_button.center, add_color, center=True)
    
    def _roll_result(d4_val, d6_val, d8_val, d10_val, d12_val, d20_val, d100_val):
        if self._valid_input():
            print("valid")