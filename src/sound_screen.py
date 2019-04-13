""" All utilities and classes for Sound Player Graphical Display """
#pylint: disable=too-many-instance-attributes

import os.path
import pygame

from .file_loader import MusicFileLoader, SoundFileLoader
from .gui.screen import Screen
from .gui.utils import draw_text, Button


class SoundPlayerScreen(Screen):
    """ Class to start Sound Player Screen """

    music_loader = MusicFileLoader()
    sound_loader = SoundFileLoader()

    def __init__(self):
        super().__init__()
        self._music = None
        self._music_name = ""
        self._sounds = []
        self._sound_names = []
        self._sound_channels = []
        self._sound_iterator = 0
        self._music_pause = False
        self._sound_pause = False

        box_height = (super().screen_height * 0.05)
        box_width = (super().screen_width * 0.70)
        function_width_size = (super().screen_width - box_width) / 3
        button_size = (function_width_size, box_height)

        self._music_box = pygame.Rect(0, 0, box_width, box_height)
        self._sound_box = pygame.Rect(0, box_height, box_width, box_height)
        self._music_function_buttons = [
            Button("|>", (self._music_box.right, 0),
                   button_size, self._play_music),
            Button("||", (self._music_box.right + function_width_size, 0),
                   button_size, self._pause_music),
            Button("X", (self._music_box.right + 2*function_width_size, 0),
                   button_size, self._stop_music)]
        self._sound_play_buttons = []
        self._sound_pause_buttons = []
        self._sound_stop_buttons = []
        self._load_buttons = self._init_buttons([("Load Music", self._load_music),
                                                 ("Load Sound", self._load_sound)])

    def _init_sound_buttons_and_channels(self, size_of_button, button_height, button_width):
        """ Initializes the individual sound buttons and sound channels """
        for i in range(5):
            self._sound_play_buttons.append(Button("|>", (self._sound_box.right,
                                                          (i+1)*button_height),
                                                   size_of_button, self._play_sound(i)))
            self._sound_pause_buttons.append(Button("||", (self._sound_box.right + button_width,
                                                           (i+1)*button_height),
                                                    size_of_button, self._pause_sound(i)))
            self._sound_stop_buttons.append(Button("X", (self._sound_box.right + 2*button_width,
                                                         (i+1)*button_height),
                                                   size_of_button, self._stop_sound(i)))

            self._sound_channels.append(pygame.mixer.Channel(i))

    def _load_music(self):
        """ Loads the music file from a pop-up dialog box """
        path = self.music_loader.file_dialog()
        if path != "":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self._music = pygame.mixer.music.load(path)
            self._music_name = os.path.basename(path)

    def _load_sound(self):
        """" Loads the sound file from a pop-up dialog box """
        path = self.sound_loader.file_dialog()
        if path != "":
            if self._sound_iterator > 4:
                self._sound_iterator = 0

            self._sounds.pop(self._sound_iterator)
            self._sounds.insert(self._sound_iterator, pygame.mixer.Sound(path))
            self._sounds.pop(self._sound_iterator)
            self._sound_names.insert(self._sound_iterator, os.path.basename(path))

            self._sound_iterator += 1

    def _draw(self, screen):
        """ Draws to the screen """
        self._draw_music(screen, self._music_name)
        for music_button in self._music_function_buttons:
            music_button.draw(screen)

        self._draw_sound(screen, self._sound_name)
        for sound_button in self._sound_function_buttons:
            sound_button.draw(screen)

        for button in self._load_buttons:
            button.draw(screen)

    def _draw_music(self, screen, music_name):
        """ Draws the music box """
        pygame.draw.rect(screen, (255, 255, 255), self._music_box, 2)
        draw_text(screen, self._font, music_name, self._music_box.center, center=True)

    def _draw_sound(self, screen, sound_name):
        """ Draws the sound box """
        pygame.draw.rect(screen, (255, 255, 255), self._sound_box, 2)
        draw_text(screen, self._font, sound_name, self._sound_box.center, center=True)

    def _play_music(self):
        if self._music_pause:
            self._music_pause = False
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play()

    @staticmethod
    def _stop_music():
        pygame.mixer.music.stop()

    def _pause_music(self):
        self._music_pause = True
        pygame.mixer.music.pause()

    def _play_sound(self, i):
        if self._sound_pause:
            self._sound_pause = False
            self._sound_channel.unpause()
        else:
            self._sound_channels[i].play(self._sounds[i])

    def _pause_sound(self, i):
        self._sound_pause = True
        self._sound_channels[i].pause()

    def _stop_sound(self, i):
        self._sound_channels[i].stop()

    def _update(self):
        music_loaded = bool(self._music_name)
        for button in self._music_function_buttons:
            button.enabled = music_loaded

        #sound_loaded = bool(self._sound_names)
        #for button in self._sound_function_buttons:
        #    button.enabled = sound_loaded

    def _handle_events(self, events):
        """ Handle events in sound player """
        super()._handle_events(events)

        for music_button in self._music_function_buttons:
            music_button.handle_events(events)

        for sound_button in self._sound_function_buttons:
            sound_button.handle_events(events)

        for load_button in self._load_buttons:
            load_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
