""" All utilities and classes for Weather and Time graphical display """

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, ALPHA_KEYS, NUMERIC_KEYS
from .gui.utils import draw_text, Button


class WeatherAndTimeScreen(Screen):
    """ Class to start weather and time screen """

    def __init__(self):
        super().__init__()
        self._weather = "calm"
        self._hour = "12"
        self._minute = "00"
        self._time_of_day = "P.M."

        self._weather_box = TextBox((0, 0), (200, 30), "calm", allowed=ALPHA_KEYS)
        self._hour_box = TextBox((0, 0), (60, 30), "12", allowed=NUMERIC_KEYS, center=True)
        self._minute_box = TextBox((0, 0), (60, 30), "00", allowed=NUMERIC_KEYS, center=True)

        self._am_pm_buttons = [Button("A.M.", (0, 0), (0, 0), self._set_am_pm, params=["A.M."]),
                               Button("P.M.", (0, 0), (0, 0), self._set_am_pm, params=["P.M."])]
        self._change_button = Button("Change", (0, 0), (0, 0), self._change_weather_and_time)

    def _valid_input(self):
        if not (self._weather_box.value or self._hour_box or self._minute_box):
            return False
        if self._hour_box > 12:
            pass

        return True

    def _set_am_pm(self, time_of_day):
        self._time_of_day = time_of_day

    def _change_weather_and_time(self):
        if self._valid_input:
            pass

    def _draw(self, screen):
        for choose_button in self._choose_buttons:
            choose_button.draw(screen)

    def _handle_events(self, events):
        super()._handle_events(events)

        for choose_button in self._choose_buttons:
            choose_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.close()
