"""All utilities for Spell List"""

import json
import os
import pygame

from .gui.screen import Screen
from .gui.utils import draw_text
from .gui.textbox import TextBox


class SpellList(Screen):
    """Class for spells list"""

    def __init__(self):
        super().__init__()
        self.text_x = 0
        self.text_y = 0
        self.speed = 2
        self.spell_list = self._load_spell_list()
        self._search_bar = TextBox((380, 10), (200, 50), "", label="Filter Spell(s)")

    def _draw(self, screen):
        spell = ''
        for spellsname, info in self.spell_list.items():
            if self._search_bar.value.lower() in spellsname.lower() \
                    or self._search_bar.value == str(info['level']):
                spell += spellsname + ' ' + str(info['level']) + "\n"
        if self._search_bar.value:
            draw_text(screen, self._font, spell, (self.text_x, self.text_y))
        self._search_bar.draw(screen)

    @staticmethod
    def _load_spell_list():
        """Loads spell list from .json file"""

        spell_path = os.path.join(".", "assets", "spells.json")
        spell_file = json.load(open(spell_path, 'r', encoding='utf-8'))
        return spell_file

    def _handle_events(self, events):
        super()._handle_events(events)
        self._search_bar.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.text_y -= self.speed
                if event.button == 5:
                    self.text_y += self.speed
