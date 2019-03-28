import unittest
from src.initiative import InitiativeTracker, CharacterInitiative

class TestInitiativeTracker(unittest.TestCase):

    def test_add_remove_character(self):
        john = CharacterInitiative("john", 1, 2)
        mary = CharacterInitiative("mary", 3, 4)

        tracker = InitiativeTracker()
        tracker.add_character(john)
        tracker.add_character(mary)

        self.assertListEqual(tracker._characters, [john, mary])

        tracker.remove_character(mary)

        self.assertListEqual(tracker._characters, [john])

    def test_character_order(self):
        alex = CharacterInitiative("Alex", 5, 4)
        anthony_h = CharacterInitiative("Anthony H", 9, 3)
        anthony_t = CharacterInitiative("Anthony T", 3, 4)
        antonio = CharacterInitiative("Antonio", 9, 3)
        jeff = CharacterInitiative("Jeff", 5, 6)
        seth = CharacterInitiative("Seth", 8, 3)

        characters = [alex, anthony_h, anthony_t, antonio, jeff, seth]

        tracker = InitiativeTracker()

        for character in characters:
            tracker.add_character(character)

        order = tracker.character_order()
        self.assertListEqual(order, [anthony_h, antonio, seth, alex, jeff, anthony_t])
