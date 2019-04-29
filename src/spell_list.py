"""All utilities for Spell List"""

import os

from .gui.screen import Screen
from .gui.utils import draw_text


class SpellList(Screen):
    """Class for spells list"""

    def __init__(self):
        super().__init__()
        self.spell_list = {}

    def _draw(self, screen):
        for spells in self.spell_list:
            draw_text(screen, self._font, spells, (0, self._advantage_button.rect.top))

    def _load_spell_list(self):
        # spell_path = os.path.join("spellslist.txt")
        spell_path = os.path.join(".", "assets", "spellslist.txt")
        with open(spell_path, "r") as filestream:
            for line in filestream:
                spell, level = line.strip().split(",")
                self.spell_list[spell.strip()] = level.strip()
        filestream.close()
        # print(spell_list)

    def search_spell(self, spell_name):
        """Returns searched spell"""
        error_msg = "No spell found"
        if spell_name in self.spell_list:
            return self.spell_list.get(spell_name)
        else:
            return error_msg
