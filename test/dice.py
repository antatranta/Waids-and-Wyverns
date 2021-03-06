import unittest
import random
from unittest.mock import patch
from src.dice import roll_results, advantage_disadvantage, roll_dice


class TestDiceFunctions(unittest.TestCase):

    def test_roll_dice(self):
        self.assertTrue(1 <= roll_dice('d4') <= 4)
        self.assertTrue(1 <= roll_dice('d6') <= 6)
        self.assertTrue(1 <= roll_dice('d8') <= 8)
        self.assertTrue(1 <= roll_dice('d10') <= 10)
        self.assertTrue(1 <= roll_dice('d12') <= 12)
        self.assertTrue(1 <= roll_dice('d20') <= 20)
        self.assertTrue(1 <= roll_dice('d100') <= 100)

    def test_roll_results(self):
        random.seed(10)
        self.assertEqual(roll_results(1, 'd4', True, 2), [[1], 2, 3])
        self.assertEqual(roll_results(1, 'd6', True, 7), [[4], 7, 11])
        self.assertEqual(roll_results(1, 'd6', False, 7), [[4], 7, 4])

    def test_advantage_disadvantage(self):
        with patch('random.randint', side_effect=[3, 5]):
            self.assertEqual(advantage_disadvantage(True, 'd6'), ([3, 5], 5))

        with patch('random.randint', side_effect=[6, 4]):
            self.assertEqual(advantage_disadvantage(False, 'd4'), ([6, 4], 4))
