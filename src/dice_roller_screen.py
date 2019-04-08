"""All Utilities and Classes for Dice Roller Graphical Display"""

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, NUMERIC_KEYS
from .gui.utils import draw_text
from .dice import roll_results, advantage_disadvantage

class DiceRollerScreen(Screen):
    """Class to start graphical dice roller"""

    def __init__(self):
        super().__init__()

        self._dice = [_Dice((0, 0), 4), _Dice((10, 10), 6)]
        self._dicesides = [4, 6, 8, 10, 12, 20, 100]
        self._dicemodifier = [4, 6, 8, 10, 12, 20, 100]
        self._dicenumber = []

        for i in range(len(self._dicesides)):
            self._dicesides[i] = TextBox((0, 0), (50, 30), "0",\
                 allowed=NUMERIC_KEYS, center=True)

        for i in range(len(self._dicemodifier)):
            self._dicemodifier[i] = TextBox((0, 0), (50, 30), "0",\
                 allowed=NUMERIC_KEYS, center=True)

        self._roll_button = pygame.Rect(0, 0, 0, 0)
        self._font = pygame.font.SysFont('comicsansms', 18)

    def _draw(self, screen):
        for die in self._dice:
            die.draw(screen)

    # def _draw(self, screen):
    #     """draw function to draw necessary objects on screen"""
    #     self._draw_input(screen)

    # def update(self):
    #     """ stuff """
    #     for sides in self._dice
    #     return True

    # def _handle_events(self, events):
    #     super()._handle_events(events)

    #     for i in range(len(self._dicesides)):
    #         self._dicesides[i].handle_events(events)

    #     for i in range(len(self._dicemodifier)):
    #         self._dicemodifier[i].handle_events(events)

    #     for event in events:
    #         if event.type == pygame.MOUSEBUTTONUP:
    #             if self._roll_button.collidepoint(pygame.mouse.get_pos()):
    #                 print("roll")
    #                 # for i in range(len(self._dicesides)):
    #                 #     print(self._dicesides[i].value)

    #         if event.type == pygame.KEYUP:
    #             if event.key == pygame.K_RETURN:
    #                 print("roll")
    #                 print(roll_results(3, "d4", False, 0))

    #             if event.key == pygame.K_ESCAPE:
    #                 self.close()

    def _valid_input(self):
        for i in range(len(self._dicesides)):
            if not self._dicesides[i].value:
                return False

            if not self._dicesides[i].value.isdigit():
                return False

        return True

    def _draw_input(self, screen):
        for i in range(len(self._dicesides)):
            self._dicesides[i].draw(screen)

        dice_width = [4, 6, 8, 10, 12, 20, 100]
        x_pos = 10
        y_pos = 0
        rect_bottom = 75

        for i in range(len(self._dicesides)):
            if i == 0:
                dice_string = "# of D4 dice: "
            elif i == 1:
                dice_string = "# of D6 dice: "
            elif i == 2:
                dice_string = "# of D8 dice: "
            elif i == 3:
                dice_string = "# of D10 dice: "
            elif i == 4:
                dice_string = "# of D12 dice: "
            elif i == 5:
                dice_string = "# of D20 dice: "
            elif i == 6:
                dice_string = "# of D100 dice: "

            dice_width[i], _ = draw_text(screen, self._font, dice_string, (x_pos, y_pos))
            self._dicesides[i].rect.left = dice_width[i] + x_pos
            y_pos += 50
            if i > 0:
                self._dicesides[i].rect.bottom = rect_bottom
                rect_bottom += 50

        self._roll_button = pygame.Rect(250, 400, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), self._roll_button)

        add_color = (0, 0, 0) if self._valid_input() else (200, 200, 200)
        draw_text(screen, self._font, "Roll", self._roll_button.center, add_color, center=True)

class _Dice:

    def __init__(self, pos, sides):
        self.pos = pos
        self.sides = sides
        self._font = pygame.font.SysFont('comicsansms', 18)

        self.label = f"# of D{sides} dice: "
        text_width, _ = self._font.size(self.label)

        self.input = TextBox((pos[0] + text_width, pos[1]), (50, 30), allowed=NUMERIC_KEYS, center=True)
        self.modifier = TextBox((self.input.rect.right, pos[1]), (50, 30), allowed=NUMERIC_KEYS, center=True)

    def draw(self, screen):
        """Draw this component to screen."""
        draw_text(screen, self._font, self.label, self.pos)
        self.input.draw(screen)
        self.modifier.draw(screen)

    def handle_events(self, events):
        """Handle events for this component."""
        self.input.handle_events(events)
        self.modifier.handle_events(events)