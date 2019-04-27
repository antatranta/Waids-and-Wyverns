""" All utilities and classes for Weather and Time graphical display """

import pygame
import tkinter as tk

from tkinter import ttk
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
        self._am_pm = ["A.M.", "P.M."]
        self._init_time()
        self._pop_up_window = tk.Tk()
        self._pop_up_window.geometry('100x100')

    def _init_time(self):
        for i in range(12):
            self._time_list.append(str(i + 1) + ":00")

    def _draw(self, screen):
        pass

    def _weather_pop_up(self):
        weather_label = tk.Label(self._pop_up_window, text="Choose the weather")
        weather_label.grid(column=0, row=0)

        weather_drop_down = ttk.Combobox(self._pop_up_window, values=self._weather_list)
        weather_drop_down.grid(column=0, row=1)
        weather_drop_down.current(0)


    def _handle_events(self, events):
        super()._handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
