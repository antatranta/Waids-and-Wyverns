""" All utilities and classes for Map and Character Graphical Display """

import pygame

from .file_loader import MapFileLoader, CharacterFileLoader
from .gui.screen import Screen
from .gui.utils import DraggableMixin


class MapAndCharacterScreen(Screen):
    """ Class to start Map and Character Screen """

    def __init__(self):
        super().__init__()
        self.map_width = super().screen_width
        self.map_height = super().screen_height
        self.map_image = self._load_map()
        self._characters = []
        self.character_images = self._load_characters()
        self.character_dragging = False

    def _draw(self, screen):
        """ Draw function to draw all necessary maps and characters on the screen """
        self._draw_map(screen)
        self._draw_characters(screen)

    def _draw_map(self, screen):
        """ Draws the map to the screen """
        screen.blit(self.map_image, (0, 0))

    def _draw_characters(self, screen):
        """ Draws the character to the screen """
        for character in self._characters:
            character.draw(screen)

    def _load_map(self):
        """ Load the maps into an array of Surface (pygame) of images"""
        map_files = MapFileLoader().load_map_files()

        map_image = pygame.image.load(map_files[0])
        map_image = pygame.transform.smoothscale(map_image, (self.map_width, self.map_height))

        return map_image

    def _load_characters(self):
        """ Load the characters into an array of Surface (pygame) of images"""
        character_files = CharacterFileLoader().load_character_files()

        character_images = []
        for i, character_file_location in enumerate(character_files):
            img = pygame.image.load(character_file_location)
            img = pygame.transform.smoothscale(img, (100, 100))

            self._characters.append(_Character(img, (i * 100, 0)))

        return character_images

    def _update(self):
        """ Updates the screen when click and dragging """
        if self.character_dragging:
            for rect in self.character_rect:
                rect.center = pygame.mouse.get_pos()

    def _handle_events(self, events):
        """ Handle events in maps """
        super()._handle_events(events)

        for character in self._characters:
            character.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()

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
