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

        self._buttons = self._init_buttons([("Add Character", self._load_charcter),
                                            ("Change Map", self._load_map),
                                            ("Toggle Remove", self._toggle_remove_mode)])

    @classmethod
    def _init_buttons(cls, options):
        buttons = []
        button_size = (cls.screen_width / len(options), 30)

        x_pos = 0
        for text, action in options:
            pos = (x_pos, cls.screen_height - button_size[1])
            buttons.append(Button(text, pos, button_size, action))
            x_pos += button_size[0]

        return buttons

    def _toggle_remove_mode(self):
        self._remove_mode = not self._remove_mode

    def _load_map(self):
        path = self.map_loader.file_dialog()
        if path != "":
            self._map = load_image(path, scale=(self.screen_width, self.screen_height))

    def _load_charcter(self):
        path = self.character_loader.file_dialog()
        if path != "":
            img = load_image(path, scale=(100, 100))
            self._characters.append(_Character(img))

    def _draw(self, screen):
        """ Draw function to draw all necessary maps and characters on the screen """
        if self._map:
            screen.blit(self._map, (0, 0))
        else:
            draw_text(screen, self._font, "Press \"m\" to open up the maps folder",
                      (0, 0), color=(0, 0, 0))
            draw_text(screen, self._font, "Press \"c\" to open up the characters folder",
                      (0, 25), color=(0, 0, 0))
            draw_text(screen, self._font, "Press \"d\" to toggle character removal",
                      (0, 50), color=(0, 0, 0))

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
                if event.key == pygame.K_m:
                    self._load_map()
                if event.key == pygame.K_c:
                    self._load_charcter()
                if event.key == pygame.K_d:
                    self._remove_mode = not self._remove_mode


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
