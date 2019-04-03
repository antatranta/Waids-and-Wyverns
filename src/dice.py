""" All utilities and classes for dice functions """

import random


class DiceRoll:
    """ Class to create dice """

    def __init__(self, times, dice_type):
        self.times = times
        self.dice_type = dice_type
        self._roll(self.times, self.dice_type)

    def _roll(self, times, dice_type):
        """ Rolls dice x amount of times """
        count = 0
        total = 0
        while count < times:
            print(self.check_dice_type(dice_type))
            count += 1

    @staticmethod
    def check_dice_type(self, dice_type):
        list_dice_types = ["d4", "d6", "d8", "d10", "d12",
                           "d20", "d100"]
        error_message = "Dice does not exist"

        if dice_type in list_dice_types:
            if dice_type == "d4":
                return random.randint(1, 4)
            elif dice_type == "d6":
                return random.randint(1, 6)
            elif dice_type == "d8":
                return random.randint(1, 8)
            elif dice_type == "d10":
                return random.randint(1, 10)
            elif dice_type == "d12":
                return random.randint(1, 12)
            elif dice_type == "d20":
                return random.randint(1, 20)
            elif dice_type == "d100":
                return random.randint(1, 100)
            else:
                print("TEST")
        else:
            print(error_message)

