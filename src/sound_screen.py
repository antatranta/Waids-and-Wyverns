""" All utilities and classes for Sound Player Graphical Display """
#pylint: disable=too-many-instance-attributes

import os.path
import math
import pickle
import pygame

from .file_loader import MusicFileLoader, SoundFileLoader
from .gui.screen import Screen
from .gui.utils import draw_text, Button

NUM_OF_SOUND_CHANNELS = int(math.floor(Screen.screen_height / (Screen.screen_height * 0.05)) - 2)
BOX_HEIGHT = Screen.screen_height * 0.05
BOX_WIDTH = Screen.screen_width * 0.70
BUTTON_WIDTH = (Screen.screen_width - BOX_WIDTH) / 3
BUTTON_SIZE = (BUTTON_WIDTH, BOX_HEIGHT)


class SoundPlayerScreen(Screen):
    """ Class to start Sound Player Screen """

    music_loader = MusicFileLoader()
    sound_loader = SoundFileLoader()

    def __init__(self):
        super().__init__()
        pygame.mixer.set_num_channels(NUM_OF_SOUND_CHANNELS)
        #self._save_music = pickle.load(open("save.p", "rb+"))
        self._save_music = {} # a list to keep track of what was loaded in
        #self._save_sounds = pickle.load(open("save.waid", "rb+"))
        #1. run with this first if you can
        self._save_sounds = {}
        self._music = None
        self._music_name = ""
        self._music_pause = False
        self._sounds = []
        self._sound_names = []
        self._sound_channels = []
        self._sound_iterator = 0
        self._sound_pauses = []
        print(pickle.load(open("save.waid", "rb")))
        print(pickle.load(open("save.p", "rb")))

        self._sound_boxes = []
        self._sound_play_buttons = []
        self._sound_pause_buttons = []
        self._sound_stop_buttons = []
        self._init_sounds()
        self._init_music()

        self._load_buttons = self._init_buttons([("Load Music", self._load_music),
                                                 ("Load Sound", self._load_sound)])

    def _init_sounds(self):
        """ Initializes the individual sounds """
        for i in range(NUM_OF_SOUND_CHANNELS):
            self._sound_names.append("")
            self._sounds.append("")
            self._sound_boxes.append(pygame.Rect(0, (i+1) * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT))

            self._sound_play_buttons.append(Button("|>", (self._sound_boxes[i].right,
                                                          (i+1) * BOX_HEIGHT),
                                                   BUTTON_SIZE, self._play_sound, [i]))
            self._sound_pause_buttons.append(Button("||", (self._sound_boxes[i].right +
                                                           BUTTON_WIDTH, (i + 1) * BOX_HEIGHT),
                                                    BUTTON_SIZE, self._pause_sound, [i]))
            self._sound_stop_buttons.append(Button("X", (self._sound_boxes[i].right + 2 *
                                                         BUTTON_WIDTH, (i + 1) * BOX_HEIGHT),
                                                   BUTTON_SIZE, self._stop_sound, [i]))

            self._sound_channels.append(pygame.mixer.Channel(i))
            self._sound_pauses.append(False)
        for sound_name in pickle.load(open("save.waid", "rb")):
            path = os.path.join(self.sound_loader.root, sound_name)
            if sound_name:
                self._pickle_sound(path)

    def _init_music(self):
        """ initialize the individual music chosen earlier """
        self._music_box = pygame.Rect(0, 0, BOX_WIDTH, BOX_HEIGHT)
        self._music_function_buttons = [
            Button("|>", (self._music_box.right, 0),
                   BUTTON_SIZE, self._play_music),
            Button("||", (self._music_box.right + BUTTON_WIDTH, 0),
                   BUTTON_SIZE, self._pause_music),
            Button("X", (self._music_box.right + 2*BUTTON_WIDTH, 0),
                   BUTTON_SIZE, self._stop_music)]

        path = os.path.join(self.music_loader.root, pickle.load(open("save.p", "rb")))
        self._pickle_music(path)
        print(path + "from init")

    def _load_music(self):
        """ Loads the music file from a pop-up dialog box """
        path = self.music_loader.file_dialog()
        if path != "":
            self._pickle_music(path)
            print(path + "from load")

    def _load_sound(self):
        """" Loads the sound file from a pop-up dialog box """
        path = self.sound_loader.file_dialog()
        if path != "":
            self._pickle_sound(path)

    def _pickle_sound(self, path):
        """Pickle sound loader"""
        if self._sound_iterator > (NUM_OF_SOUND_CHANNELS - 1):
            self._sound_iterator = 0

        self._sounds.pop(self._sound_iterator)
        self._sounds.insert(self._sound_iterator, pygame.mixer.Sound(path))
        self._sound_names.pop(self._sound_iterator)
        self._sound_names.insert(self._sound_iterator, os.path.basename(path))
        pickle.dump(self._sound_names, open("save.waid", "wb"))
        self._sound_iterator += 1

    def _pickle_music(self, path):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self._music = pygame.mixer.music.load(path)
        self._music_name = os.path.basename(path)
        pickle.dump(self._music_name, open("save.p", "wb"))

    def _draw(self, screen):
        """ Draws to the screen """
        self._draw_music(screen)
        for music_button in self._music_function_buttons:
            music_button.draw(screen)

        self._draw_sounds(screen)
        self._draw_sound_buttons(screen)

        for button in self._load_buttons:
            button.draw(screen)

    def _draw_music(self, screen):
        """ Draws the music box """
        pygame.draw.rect(screen, (255, 255, 255), self._music_box, 2)
        draw_text(screen, self._font, self._music_name, self._music_box.center, center=True)

    def _draw_sounds(self, screen):
        """ Draws the sound box """
        for sound in self._sound_boxes:
            pygame.draw.rect(screen, (255, 255, 255), sound, 2)

        i = 0
        for sound_name in self._sound_names:
            draw_text(screen, self._font, sound_name, self._sound_boxes[i].center, center=True)
            i += 1

    def _draw_sound_buttons(self, screen):
        """ Draws the sounds' buttons """
        for sound_play in self._sound_play_buttons:
            sound_play.draw(screen)

        for sound_pause in self._sound_pause_buttons:
            sound_pause.draw(screen)

        for sound_stop in self._sound_stop_buttons:
            sound_stop.draw(screen)

    def _play_music(self):
        """ Function to play music """
        if self._music_pause:
            self._music_pause = False
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play()

    def _pause_music(self):
        """ Function to pause music """
        self._music_pause = True
        pygame.mixer.music.pause()

    @staticmethod
    def _stop_music():
        """ Function to stop music """
        pygame.mixer.music.stop()

    def _play_sound(self, i):
        """
        Function to play sound in a specific channel

        :param i: the index / iterator for the channel
        """
        if self._sound_pauses[i]:
            self._sound_pauses[i] = False
            self._sound_channels[i].unpause()
        else:
            self._sound_channels[i].play(self._sounds[i])

    def _pause_sound(self, i):
        """
        Function to pause sound in a specific channel

        :param i: the index / iterator for the channel
        """
        self._sound_pauses[i] = True
        self._sound_channels[i].pause()

    def _stop_sound(self, i):
        """
        Function to stop sound in a specific channel

        :param i: the index / iterator for the channel
        """
        self._sound_channels[i].stop()

    def _update(self):
        """ Make the play, pause, and stop buttons gray out or not """
        music_loaded = bool(self._music_name)
        for button in self._music_function_buttons:
            button.enabled = music_loaded

        i = 0
        for sound_name in self._sound_names:
            sound_loaded = bool(sound_name)
            self._sound_play_buttons[i].enabled = sound_loaded
            self._sound_pause_buttons[i].enabled = sound_loaded
            self._sound_stop_buttons[i].enabled = sound_loaded
            i += 1

    def _handle_events(self, events):
        """ Handle events in sound player """
        super()._handle_events(events)

        for music_button in self._music_function_buttons:
            music_button.handle_events(events)

        for sound_play in self._sound_play_buttons:
            sound_play.handle_events(events)

        for sound_pause in self._sound_pause_buttons:
            sound_pause.handle_events(events)

        for sound_stop in self._sound_stop_buttons:
            sound_stop.handle_events(events)

        for load_button in self._load_buttons:
            load_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
