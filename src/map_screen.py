""" All utilities and classes for Map and Character Graphical Display """

import pygame

from .file_loader import CharacterFileLoader, MapFileLoader
from .gui.screen import Screen
from .gui.utils import DraggableMixin, load_image


class MapAndCharacterScreen(Screen):
    """ Class to start Map and Character Screen """

    map_loader = MapFileLoader()
    character_loader = CharacterFileLoader()

    def __init__(self):
        super().__init__()
        self._characters = []
        self._map = None

    def _load_map(self):
        path = self.map_loader.file_dialog()
        self._map = load_image(path, scale=(self.screen_width, self.screen_height))

    def _load_charcter(self):
        path = self.character_loader.file_dialog()
        img = load_image(path, scale=(100, 100))
        self._characters.append(_Character(img))

    def _draw(self, screen):
        """ Draw function to draw all necessary maps and characters on the screen """
        if self._map:
            screen.blit(self._map, (0, 0))

        for character in self._characters:
            character.draw(screen)

    def _handle_events(self, events):
        """ Handle events in maps """
        super()._handle_events(events)

        for character in self._characters:
            character.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                if event.key == pygame.K_m:
                    self._load_map()
                if event.key == pygame.K_c:
                    self._load_charcter()

class _Character(DraggableMixin):

    def __init__(self, img, pos=(0, 0)):
        DraggableMixin.__init__(self, pos)
        self.img = img

    @property
    def rect(self):
        """Rect of the character"""
        rect = self.img.get_rect()
        rect.topleft = self.pos
        return rect

    def draw(self, screen):
        """Draw this element to screen."""
        screen.blit(self.img, self.pos)
