""" All utilities and classes for Weather and Time graphical display """

import pygame
import thorpy

from .gui.screen import Screen
from .gui.utils import draw_text


class WeatherAndTimeScreen(Screen):
    """ Class to start weather and time screen """

    def __init__(self):
        super().__init__()
        self._weather_list = ["calm", "cold", "cold snap", "downpour", "warm",
                              "heat wave", "hot", "moderate", "windstorm",
                              "rain", "snow", "heavy snow", "sleet", "hail",
                              "blizzard", "hurricane", "tornado", "duststorm",
                              "snowstorm", "thunderstorm", "light wind",
                              "moderate wind", "strong wind", "severe wind",
                              "windstorm"]
        self._time_list = []
        self._init_time()

    def _init_time(self):
        for i in range(12):
            self._time_list.append(str(i + 1) + ":00")

    def _draw(self, screen):
        pass

    def _handle_events(self, events):
        pass
