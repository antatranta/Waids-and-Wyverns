""" All utilities and classes for Map and Character Graphical Display """

import pygame

from .file_loader import MapFileLoader, CharacterFileLoader
from .gui.screen import Screen


class MapAndCharacterScreen(Screen):
    """ Class to start Map and Character Screen """

    def __init__(self):
        super().__init__()
        self.map_width = super().screen_width
        self.map_height = super().screen_height
        self.map_image = self._load_map()
        self.character_rect = []
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
        for i, character in enumerate(self.character_images):
            screen.blit(character, self.character_rect[i])

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
            character_images.append(pygame.image.load(character_file_location))
            character_images[i] = pygame.transform.smoothscale(character_images[i], (100, 100))

            self.character_rect.append(character_images[i].get_rect())
            self.character_rect[i] = self.character_rect[i].move(i * 100, 0)

        return character_images

    def _update(self):
        """ Updates the screen when click and dragging """

        # Collision detection #
        # character_rect_collision = self.character_rect

        # for rect in self.character_rect:
        #    if rect.collidepoint(pygame.mouse.get_pos()):
        #        for rect_collision in character_rect_collision:
        #            if character_rect_collision.index(rect_collision)
        #               != self.character_rect.index(rect):
        #                if rect.colliderect(rect_collision):
        #                    rect.move_ip(rect.x + 50, rect.y + 50)

        if self.character_dragging:
            for rect in self.character_rect:
                rect.center = pygame.mouse.get_pos()

    def _handle_events(self, events):
        """ Handle events in maps """
        super()._handle_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # iterate through the character rects to see which collides with mouse
                    for rect in self.character_rect:
                        if rect.collidepoint(event.pos):
                            self.character_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.character_dragging = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
