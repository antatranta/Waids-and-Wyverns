""" All utilities and classes for dice functions"""
# Goal: https://www.wizards.com/dnd/dice/dice.htm
import random


def roll_results(times, dice_type, choice, mod_num):
    """Returns roll results"""
    count = 0
    total = 0
    if choice:
        total += _modifier(total, mod_num)
    while count < times:
        roll_dice(dice_type)
        total += roll_dice(dice_type)
        count += 1
    return total


def _modifier(total, mod_num):
    """Increments/Decrements dice as needed"""
    # mod_num = input("Enter modifier value")
    # Positive vs Negative selection button
    total += mod_num
    return total


def advantage_disadvantage(advantage, dice_type):
    """Advantage rolls same dice again and picks larger,
    disadvantage rolls again, picks lower"""
    # Rules: https://5thsrd.org/rules/advantage_and_disadvantage/
    # Use the same dice type that is picked, i.e roll d4 twice
    dice1 = roll_dice(dice_type)
    dice2 = roll_dice(dice_type)
    if advantage:
        value = max(dice1, dice2)
    else:
        value = min(dice1, dice2)
    return value


def roll_dice(dice_type):
    """Returns dice value"""
    value = None

    if dice_type == "d4":
        value = random.randint(1, 4)
    elif dice_type == "d6":
        value = random.randint(1, 6)
    elif dice_type == "d8":
        value = random.randint(1, 8)
    elif dice_type == "d10":
        value = random.randint(1, 10)
    elif dice_type == "d12":
        value = random.randint(1, 12)
    elif dice_type == "d20":
        value = random.randint(1, 20)
    elif dice_type == "d100":
        value = random.randint(1, 100)
    return value


# TEMP TEST
print("Min: " + str(advantage_disadvantage(False, 'd4')))
print("Max: " + str(advantage_disadvantage(True, 'd4')))
print("Roll Result: " + str(roll_results(1, 'd4', True, 2)))
# if __name__ == "__main__":
# DiceRoll.check_dice_type()
