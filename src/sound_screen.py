""" All utilities and classes for Sound Player Graphical Display """

import pygame

from .file_loader import MusicFileLoader, SoundFileLoader
from .gui.screen import Screen
from .gui.utils import draw_text


class SoundPlayerScreen(Screen):
    """ Class to start Sound Player Screen """

    music_loader = MusicFileLoader()
    sound_loader = SoundFileLoader()

    def __init__(self):
        super().__init__()
        self._music_function_buttons = []
        self._sound_function_buttons = []

    def _load_music(self):
        pass

    def _load_sound(self):
        pass

    def _draw(self, screen):
        self._draw_music(screen, "placeholder.mp3")
        self._draw_sound(screen, "placeholder.wav")

    def _draw_music(self, screen, music_name):
        music_box_height = super().screen_height * 0.05
        music_box = pygame.Rect(0, 0,
                                super().screen_width * 0.70, music_box_height)

        function_buttons_width = (super().screen_width - music_box.width) / 3
        play_button = pygame.Rect(music_box.right, music_box.top,
                                  function_buttons_width, music_box_height)
        pause_button = pygame.Rect(play_button.right, play_button.top,
                                   function_buttons_width, music_box_height)
        stop_button = pygame.Rect(pause_button.right, pause_button.top,
                                  function_buttons_width, music_box_height)

        pygame.draw.rect(screen, (255, 255, 255), music_box)
        pygame.draw.rect(screen, (0, 255, 0), play_button)
        pygame.draw.rect(screen, (255, 165, 0), pause_button)
        pygame.draw.rect(screen, (255, 0, 0), stop_button)

        draw_text(screen, self._font, music_name, music_box.center, center=True)
        draw_text(screen, self._font, "|>", play_button.center, center=True)
        draw_text(screen, self._font, "||", pause_button.center, center=True)
        draw_text(screen, self._font, "X", stop_button.center, center=True)

    def _draw_sound(self, screen, sound_name):
        music_box_height = super().screen_height * 0.05
        sound_box = pygame.Rect(0, music_box_height,
                                super().screen_width * 0.70, music_box_height)

        function_buttons_width = (super().screen_width - sound_box.width) / 3
        play_button = pygame.Rect(sound_box.right, sound_box.top,
                                  function_buttons_width, music_box_height)
        pause_button = pygame.Rect(play_button.right, play_button.top,
                                   function_buttons_width, music_box_height)
        stop_button = pygame.Rect(pause_button.right, pause_button.top,
                                  function_buttons_width, music_box_height)

        pygame.draw.rect(screen, (255, 255, 255), sound_box)
        pygame.draw.rect(screen, (0, 255, 0), play_button)
        pygame.draw.rect(screen, (255, 165, 0), pause_button)
        pygame.draw.rect(screen, (255, 0, 0), stop_button)

        draw_text(screen, self._font, sound_name, sound_box.center, center=True)
        draw_text(screen, self._font, "|>", play_button.center, center=True)
        draw_text(screen, self._font, "||", pause_button.center, center=True)
        draw_text(screen, self._font, "X", stop_button.center, center=True)

    def _play_music(self):
        pass

    def _play_sound(self):
        pass

    def _handle_events(self, events):
        """ Handle events in sound player """
        super()._handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
