"""All utilities and classes for initiative tracking."""

class CharacterInitiative:
    """Class to represent a single character's initiative."""

    def __init__(self, name, initiative, health):
        self.name = name
        self.initiative = initiative
        self.health = health

class InitiativeTracker:
    """Class to track intitative of players and monsters."""

    def __init__(self):
        self._characters = []

    def add_character(self, character):
        """
        Add a character to this initiative tracker.

        :param character: CharacterInitiative to add
        """
        self._characters.append(character)

    def remove_character(self, character):
        """
        Remove a character from this initiative tracker.

        :param character: CharacterInitiative to remove
        """
        self._characters.remove(character)

    def character_order(self):
        """
        Get list of chacters ordered by initiative score.

        ties will be broken by add order.

        :returns: List of CharacterInitiative
        """
        return sorted(self._characters, key=lambda c: c.initiative, reverse=True)
