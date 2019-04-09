""" All utilities and classes for dice functions"""
# Goal: https://www.wizards.com/dnd/dice/dice.htm
import random


def roll_results(times, dice_type, enable_modifier, mod_num):
    """Returns roll results"""
    count = 0
    total = 0
    rolls = []
    if enable_modifier:
        total += _modifier(total, mod_num)
    while count < times:
        value = roll_dice(dice_type)
        rolls.append(value)
        total += value
        count += 1
    return [rolls, mod_num, total]


def _modifier(total, mod_num):
    """Increments/Decrements dice as needed"""
    # Positive vs Negative selection button
    total += mod_num
    return total


def advantage_disadvantage(advantage, dice_type):
    """Advantage rolls same dice again and picks larger,
    disadvantage rolls again, picks lower"""
    # Rules: https://5thsrd.org/rules/advantage_and_disadvantage/
    # Use the same dice type that is picked, i.e roll d4 twice
    roll1, roll2 = roll_dice(dice_type), roll_dice(dice_type)
    if advantage:
        value = max(roll1, roll2)
    else:
        value = min(roll1, roll2)
    return ([roll1, roll2], value)


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
