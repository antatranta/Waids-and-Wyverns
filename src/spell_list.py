"""All utilities for Spell List"""

import os
import json

from .gui.screen import Screen
from .gui.utils import draw_text


class SpellList(Screen):
    """Class for spells list"""

    def __init__(self):
        super().__init__()
        self.spell_list = self._load_spell_list()

    def _draw(self, screen):
        temp = ''
        for spellsname, info in self.spell_list.items():
            temp += spellsname + ' ' + str(info['level']) + "\n"
        draw_text(screen, self._font, temp, (0, 0))

    def _load_spell_list(self):
        spell_path = os.path.join(".", "assets", "spells.json")
        spell_file = json.load(open(spell_path, 'r'))
        return spell_file

    def search_spell(self, spell_name):
        """Returns searched spell"""
        error_msg = "No spell found"
        if spell_name in self.spell_list:
            return self.spell_list.get(spell_name)
        else:
            return error_msg

