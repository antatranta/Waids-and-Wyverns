""" All utilities and classes for Map and Character Graphical Display """
import pickle
import os

import pygame

from .file_loader import CharacterFileLoader, MapFileLoader
from .gui.screen import Screen
from .gui.utils import DraggableMixin, DragAndScaleMixin, load_image, draw_text


class MapAndCharacterScreen(Screen):
    """ Class to start Map and Character Screen """
    # pylint: disable=too-many-instance-attributes
    MAX_ZOOM = 5.0
    MIN_ZOOM = 1.0

    map_loader = MapFileLoader()
    character_loader = CharacterFileLoader()

    def __init__(self):
        super().__init__()
        self.path_save_char = os.path.join(".", "assets", "saves", "characters.pkl")
        self.path_save_maps = os.path.join(".", "assets", "saves", "maps.pkl")

        self._characters = pickle.load(open(self.path_save_char, "rb"))\
            if os.path.isfile(self.path_save_char) else []
        self._map = load_image(pickle.load(open(self.path_save_maps, "rb")),
                               scale=(self.screen_width, self.screen_height)) \
            if os.path.isfile(self.path_save_maps) else None
        self._remove_mode = False
        self.zoom = 1.0
        self._zoom_offset = (0, 0)
        self._buttons = self._init_buttons([("Add Character", self._load_character),
                                            ("Change Map", self._load_map),
                                            ("Toggle Remove", self._toggle_remove_mode)])

        def drag(pos):
            self.zoom_offset = pos

        DraggableMixin.__init__(self, self._get_rect, drag)

    def _get_rect(self):
        return pygame.Rect(self.zoom_offset,
                           (self.screen_width * self.zoom, self.screen_height * self.zoom))

    def _toggle_remove_mode(self):
        self._remove_mode = not self._remove_mode

    def _load_map(self):
        path = self.map_loader.file_dialog()
        if path != "":
            pickle.dump(path, open(self.path_save_maps, "wb+"))
            self._map = load_image(path, scale=(self.screen_width, self.screen_height))

    def _load_character(self):
        path = self.character_loader.file_dialog()
        if path != "":
            self._characters.append(_Character(path, zoom=self.zoom, zoom_offset=self.zoom_offset))

    def _draw(self, screen):
        """ Draw function to draw all necessary maps and characters on the screen """
        if self._map:
            img = pygame.transform.smoothscale(self._map, (int(screen.get_width() * self.zoom),
                                                           int(screen.get_height() * self.zoom)))
            screen.blit(img, self.zoom_offset)

        for character in self._characters:
            character.draw(screen)

        for button in self._buttons:
            button.draw(screen)

        if self._remove_mode:
            draw_text(screen, self._font, "remove mode", (0, 0), color=(255, 0, 0))

    @property
    def zoom_offset(self):
        """Get zoom offset"""
        return (self._zoom_offset[0] * self.zoom, self._zoom_offset[1] * self.zoom)

    @zoom_offset.setter
    def zoom_offset(self, zoom_offset):
        left = min(max(zoom_offset[0], self.screen_width * (1 - self.zoom)), 0)
        top = min(max(zoom_offset[1], self.screen_height * (1 - self.zoom)), 0)

        self._zoom_offset = (left / self.zoom, top / self.zoom)
        self._update_zooms(self.zoom, self.zoom_offset)

    def _update_zooms(self, zoom, offset):
        for character in self._characters:
            character.zoom = zoom
            character.zoom_offset = offset

    def _zoom_in(self):
        self.zoom = min(self.zoom * 1.2, self.MAX_ZOOM)
        self.zoom_offset = self.zoom_offset
        self._update_zooms(self.zoom, self.zoom_offset)

    def _zoom_out(self):
        self.zoom = max(self.zoom * 0.8, self.MIN_ZOOM)
        self.zoom_offset = self.zoom_offset
        self._update_zooms(self.zoom, self.zoom_offset)

    def _handle_events(self, events):
        """ Handle events in maps """
        super()._handle_events(events)

        char_selected = False
        for character in self._characters:
            character.handle_events(events)
            char_selected = char_selected or character.draggable_selected

        if not char_selected:
            DraggableMixin.handle_events(self, events)

        for button in self._buttons:
            button.handle_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self._remove_mode:
                for character in self._characters:
                    if character.rect.collidepoint(event.pos):
                        self._characters.remove(character)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pickle.dump(self._characters, open(self.path_save_char, "wb+"))
                    self.close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self._zoom_in()

                if event.button == 5:
                    self._zoom_out()


class _Character(DragAndScaleMixin):
    """ Allows characters to be dragged """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, img, pos=(0, 0), size=(100, 100), zoom=1.0, zoom_offset=(0, 0)):
        # pylint: disable=too-many-arguments
        self.full_res_img = load_image(img)
        self._zoom = None
        self._pos = pos

        self._size = size
        self._img_path = img
        self.img = load_image(img, size)
        self.zoom_offset = zoom_offset
        self.zoom = zoom

        DragAndScaleMixin.__init__(self, self._get_rect, self._update_pos)

    def _update_pos(self, pos):
        self.pos = pos

    def _get_rect(self):
        return self.rect

    @property
    def rect(self):
        """Rect of the character"""
        rect = self.img.get_rect()
        rect.topleft = self.pos
        return rect

    def draw(self, screen):
        """Draw this element to screen."""
        screen.blit(self.img, self.pos)

    @property
    def zoom(self):
        """Get the percentage zoomed."""
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        """Set the percentage zoomed."""
        self._zoom = zoom
        self._resize_img()

    @property
    def size(self):
        """Get the image width x height."""
        return self._size

    @size.setter
    def size(self, size):
        """Set the image width x height."""
        self._size = size
        self._resize_img()

    @property
    def pos(self):
        """Get the character's position."""
        return (self._pos[0] * self.zoom + self.zoom_offset[0],
                self._pos[1] * self.zoom + self.zoom_offset[1])

    @pos.setter
    def pos(self, pos):
        """Set the character's position."""
        self._pos = ((pos[0] - self.zoom_offset[0]) / self.zoom,
                     (pos[1] - self.zoom_offset[1]) / self.zoom)

    def _resize_img(self):
        self.img = pygame.transform.smoothscale(self.full_res_img,
                                                (int(self.size[0] * self.zoom),
                                                 int(self.size[1] * self.zoom)))

    def __getstate__(self):
        """Export function for pickle."""
        state = self.__dict__.copy()
        state['full_res_img'] = None
        state['img'] = None
        state['_zoom'] = 1.0
        state['_zoom_offset'] = (0, 0)
        return state

    def __setstate__(self, newstate):
        """Import function for pickle."""
        newstate['full_res_img'] = load_image(newstate['_img_path'])
        newstate['img'] = load_image(newstate['_img_path'], scale=newstate['_size'])
        self.__dict__.update(newstate)
        self._resize_img()
