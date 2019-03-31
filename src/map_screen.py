""" All utilities and classes for Map and Character Graphical Display """

import pygame

from .file_loader import MapFileLoader, CharacterFileLoader
from .gui.screen import Screen


class MapAndCharacterScreen(Screen):
    """ Class to start Map and Character Screen """

    def __init__(self):
        super().__init__()
        self.map_images = []
        self.character_images = []

    def _draw(self, screen):
        """ Draw function to draw all necessary maps and characters on the screen """
        self._draw_map(screen)
        self._draw_characters(screen)

    def _draw_map(self, screen):
        """ Load the maps into an array of Surface (pygame) of images"""
        map_files = MapFileLoader().get_map_files()

        for i, map_file_location in enumerate(map_files):
            self.map_images.append(pygame.image.load(map_file_location))
            screen.blit(self.map_images[i], (0, 50))

    def _draw_characters(self, screen):
        """ Load the characters into an array of Surface (pygame) of images"""
        character_files = CharacterFileLoader().get_character_files()

        for i, character_file_location in enumerate(character_files):
            self.character_images[i] = pygame.image.load(character_file_location)
            screen.blit(self.character_images[i], (i*5, i*5))
