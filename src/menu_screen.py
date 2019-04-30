"""Main Menu Screen"""

from .gui.screen import Screen
from .gui.utils import Button
from .initiative_screen import InitiativeTrackerScreen
from .map_screen import MapAndCharacterScreen
from .dice_roller_screen import DiceRollerScreen
from .sound_screen import SoundPlayerScreen
from .notes_screen import NotesScreen
from .weather_time_screen import WeatherAndTimeScreen


class MainMenuScreen(Screen):
    """Class to create a main menu screen."""

    def __init__(self):
        super().__init__()

        x_pos = self.screen_width / 2 - 200
        button_size = (400, 30)

        self._buttons = [
            Button("Maps", (x_pos, 10), button_size, MapAndCharacterScreen().open),
            Button("Initiative", (x_pos, 50), button_size, InitiativeTrackerScreen().open),
            Button("Dice Roller", (x_pos, 90), button_size, DiceRollerScreen().open),
            Button("Sound Player", (x_pos, 130), button_size, SoundPlayerScreen().open),
            Button("Notes", (x_pos, 170), button_size, NotesScreen().open),
            Button("Weather and Time", (x_pos, 210), button_size, WeatherAndTimeScreen().open)]

    def _draw(self, screen):
        for button in self._buttons:
            button.draw(screen)

    def _handle_events(self, events):
        super()._handle_events(events)
        for button in self._buttons:
            button.handle_events(events)
