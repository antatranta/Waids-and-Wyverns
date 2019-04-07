""" All utilities and classes for Map and Character Graphical Display """

import pygame

from .file_loader import CharacterFileLoader, MapFileLoader
from .gui.screen import Screen
from .gui.utils import DraggableMixin, load_image, draw_text, Button


class MapAndCharacterScreen(Screen):
    """ Class to start Map and Character Screen """

    map_loader = MapFileLoader()
    character_loader = CharacterFileLoader()

    def __init__(self):
        super().__init__()
        self._characters = []
        self._map = None
        self._remove_mode = False

        self._buttons = self._init_buttons([("Add Character", self._load_character),
                                            ("Change Map", self._load_map),
                                            ("Toggle Remove", self._toggle_remove_mode)])

    def _toggle_remove_mode(self):
        self._remove_mode = not self._remove_mode

    def _load_map(self):
        path = self.map_loader.file_dialog()
        if path != "":
            self._map = load_image(path, scale=(self.screen_width, self.screen_height))

    def _load_character(self):
        path = self.character_loader.file_dialog()
        if path != "":
            img = load_image(path, scale=(100, 100))
            self._characters.append(_Character(img))

    def _draw(self, screen):
        """ Draw function to draw all necessary maps and characters on the screen """
        if self._map:
            screen.blit(self._map, (0, 0))

        for character in self._characters:
            character.draw(screen)

        for button in self._buttons:
            button.draw(screen)

        if self._remove_mode:
            draw_text(screen, self._font, "remove mode", (0, 0), color=(255, 0, 0))

    def _handle_events(self, events):
        """ Handle events in maps """
        super()._handle_events(events)

        for character in self._characters:
            character.handle_events(events)

        for button in self._buttons:
            button.handle_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self._remove_mode:
                for character in self._characters:
                    if character.rect.collidepoint(event.pos):
                        self._characters.remove(character)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()


class _Character(DraggableMixin):
    """ Allows characters to be dragged """

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
