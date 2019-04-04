""" All utilities and classes for dice functions """
"""Goal: https://www.wizards.com/dnd/dice/dice.htm"""
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

    def _modifier(self, choice, total):
        "Increments/Decrements dice as needed"
        positive = True
        negative = False
        mod_num = input("Enter modifier value")

        #Positive vs Negative selection button
        if (self.choice == positive):
            #find num value then add to dice roll
            total += mod_num
            return total

        elif (self.choice == negative):
            total += mod_num
            return total

    def _advantage_disadvantage(self, situation):
        "Advantage rolls same dice again and picks larger, disadvantage rolls again, picks lower"
        "Rules: https://5thsrd.org/rules/advantage_and_disadvantage/"
        advantage = True
        disadvantage = False
        compare1 = 0
        compare2 = 0
        if situation == advantage:
            "Use the same dice type that is picked, i.e roll d4 twice"
            compare1 = self.check_dice_type(self.dice_type)
            compare2 = self.check_dice_type(self.dice_type)
            if compare1 > compare2:
                return compare1
            else:
                return compare2
        elif situation == disadvantage:
            compare1 = self.check_dice_type(self.dice_type)
            compare2 = self.check_dice_type(self.dice_type)
            if compare1 > compare2:
                return compare2
            else:
                return compare1

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

if __name__ == "__main__":
    DiceRoll.check_dice_type()