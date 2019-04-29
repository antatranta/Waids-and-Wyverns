""" All utilities and classes for Weather and Time graphical display """
# pylint: disable=too-many-instance-attributes

import pygame

from .gui.screen import Screen
from .gui.textbox import TextBox, ALPHA_KEYS, NUMERIC_KEYS
from .gui.utils import draw_text, Button

CENTER_OF_SCREEN = (Screen.screen_width / 2, Screen.screen_height / 2)


class WeatherAndTimeScreen(Screen):
    """ Class to start weather and time screen """

    def __init__(self):
        super().__init__()
        self._weather = "calm"
        self._hour = "12"
        self._minute = "00"
        self._time_of_day = "P.M."

        self._weather_box = TextBox((0, 0), (200, 30), "calm", allowed=ALPHA_KEYS)
        self._hour_box = TextBox((0, 0), (50, 30), "12", allowed=NUMERIC_KEYS, center=True)
        self._minute_box = TextBox((0, 0), (50, 30), "00", allowed=NUMERIC_KEYS, center=True)

        self._am_pm_buttons = [Button("A.M.", (0, 0), (0, 0), self._set_am_pm, params=["A.M."]),
                               Button("P.M.", (0, 0), (0, 0), self._set_am_pm, params=["P.M."])]
        self._change_button = Button("Change", (0, 0), (0, 0), self._change_weather_and_time)

    def _set_am_pm(self, time_of_day):
        """ Set the AM or PM of the time """
        self._time_of_day = time_of_day

    def _change_weather_and_time(self):
        """ Change the weather and time if the input is valid """
        if self._valid_input:
            # if its blank input then keep the same value shown already
            if self._weather_box.value == '':
                self._weather_box.value = self._weather
            if self._hour_box.value == '':
                self._hour_box.value = self._hour
            if self._minute_box.value == '':
                self._minute_box.value = self._minute

            self._weather = self._weather_box.value
            # casting a string to int back to string to get a whole number and remove leading 0s
            self._hour = str(int(self._hour_box.value))
            self._minute = str(int(self._minute_box.value))

            # add a leading 0 if its a single digit for minutes
            if 0 <= int(self._minute) <= 9:
                self._minute = "0" + self._minute

            self._weather_box.value, self._hour_box.value, self._minute_box.value = ('', '', '')

    def _valid_input(self):
        """ Checks to see if the textbox input is valid """
        # need at least one input
        if not (self._weather_box.value or self._hour_box.value or self._minute_box.value):
            return False

        # check integer bounds for hour
        if self._hour_box.value != '':
            if int(self._hour_box.value) < 1 or int(self._hour_box.value) > 12:
                return False

        # check integer bounds for minutes
        if self._minute_box.value != '':
            if int(self._minute_box.value) > 59:
                return False

        return True

    def _update(self):
        """ Update the change button to gray it out or not """
        self._change_button.enabled = self._valid_input()

    def _draw(self, screen):
        """ Draw the textbox input and text on screen """
        self._draw_input(screen, (0, self.screen_height - self._weather_box.rect.height))
        self._draw_text(screen)

    def _draw_input(self, screen, pos):
        """ Draw the textbox input on the bottom """
        self._weather_box.rect.top = pos[1]
        self._hour_box.rect.top = pos[1]
        self._minute_box.rect.top = pos[1]

        weather_width, _ = draw_text(screen, self._font, "Weather:", pos)
        self._weather_box.rect.left = pos[0] + weather_width

        hour_width, _ = draw_text(screen, self._font, "Time:",
                                  (self._weather_box.rect.right, pos[1]))
        self._hour_box.rect.left = self._weather_box.rect.right + hour_width

        minute_width, _ = draw_text(screen, self._font, ":", (self._hour_box.rect.right, pos[1]))
        self._minute_box.rect.left = self._hour_box.rect.right + minute_width

        self._am_pm_buttons[0].rect = pygame.Rect(self._minute_box.rect.right, pos[1],
                                                  50, 30)
        self._am_pm_buttons[1].rect = pygame.Rect(self._am_pm_buttons[0].rect.right, pos[1],
                                                  50, 30)
        self._change_button.rect = pygame.Rect(self._am_pm_buttons[1].rect.right + 10, pos[1],
                                               100, 30)

        for am_pm_button in self._am_pm_buttons:
            am_pm_button.draw(screen)

        self._change_button.draw(screen)

        self._weather_box.draw(screen)
        self._hour_box.draw(screen)
        self._minute_box.draw(screen)

    def _draw_text(self, screen):
        """ Draw the weather and time text in the center of the screen """
        weather_text = "Weather: " + self._weather
        time_text = "Time: " + self._hour + ":" + self._minute + " " + self._time_of_day

        text_loc = (CENTER_OF_SCREEN[0], CENTER_OF_SCREEN[1] - 25)

        draw_text(screen, self._font, weather_text, text_loc, center=True)
        draw_text(screen, self._font, time_text, CENTER_OF_SCREEN, center=True)

    def _handle_events(self, events):
        """ Handle events on the screen """
        super()._handle_events(events)

        self._weather_box.handle_events(events)
        self._hour_box.handle_events(events)
        self._minute_box.handle_events(events)

        for am_pm_button in self._am_pm_buttons:
            am_pm_button.handle_events(events)

        self._change_button.handle_events(events)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self._change_weather_and_time()
                if event.key == pygame.K_ESCAPE:
                    self.close()
