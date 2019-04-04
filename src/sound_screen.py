""" All utilities and classes for Sound Player Graphical Display """
#pylint: disable=no-self-use

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
        self._sound_function_buttons = [
            Button("|>", (self._sound_box.right, box_height),
                   button_size, self._play_sound),
            Button("||", (self._sound_box.right + function_width_size, box_height),
                   button_size, self._pause_sound),
            Button("X", (self._sound_box.right + 2*function_width_size, box_height),
                   button_size, self._stop_sound)]

    def _load_music(self):
        pass

    def _load_sound(self):
        pass

    def _draw(self, screen):
        self._draw_music(screen, "placeholder.mp3")
        for music_button in self._music_function_buttons:
            music_button.draw(screen)

        self._draw_sound(screen, "placeholder.wav")
        for sound_button in self._sound_function_buttons:
            sound_button.draw(screen)

    def _draw_music(self, screen, music_name):
        pygame.draw.rect(screen, (255, 255, 255), self._music_box, 2)
        draw_text(screen, self._font, music_name, self._music_box.center, center=True)

    def _draw_sound(self, screen, sound_name):
        pygame.draw.rect(screen, (255, 255, 255), self._sound_box, 2)
        draw_text(screen, self._font, sound_name, self._sound_box.center, center=True)

    def _play_music(self):
        print("Playing music!")

    def _play_sound(self):
        print("Playing sound!")

    def _pause_music(self):
        print("Paused music!")

    def _pause_sound(self):
        print("Paused sound!")

    def _stop_music(self):
        print("Stopped music!")

    def _stop_sound(self):
        print("Stopped sound!")

    def _handle_events(self, events):
        """ Handle events in sound player """
        super()._handle_events(events)

        for music_button in self._music_function_buttons:
            music_button.handle_events(events)

        for sound_button in self._sound_function_buttons:
            sound_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
