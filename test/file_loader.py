import unittest
import os
from src.file_loader import MapFileLoader, CharacterFileLoader, MusicFileLoader, SoundFileLoader


ASSETS = os.path.join(".", "test", "fixtures", "assets")


class TestMapFileLoader(unittest.TestCase):
    def test_file_loader(self):
        map_path = os.path.join(ASSETS, "images", "maps")

        map_loader = MapFileLoader(map_path=map_path)

        self.assertCountEqual(map_loader.load_map_files(), [
            os.path.join(map_path, "my_map.jpg"),
            os.path.join(map_path, "another_map.png"),
        ])


class TestCharacterLoader(unittest.TestCase):
    def test_character_loader(self):
        character_path = os.path.join(ASSETS, "images", "characters")

        char_loader = CharacterFileLoader(character_path=character_path)

        self.assertCountEqual(char_loader.load_character_files(), [
            os.path.join(character_path, "another_character.png"),
            os.path.join(character_path, "character1.jpg"),
        ])


class TestMusicFileLoader(unittest.TestCase):
    def test_music_loader(self):
        music_path = os.path.join(ASSETS, "media", "music")

        music_loader = MusicFileLoader(music_path=music_path)

        self.assertCountEqual(music_loader.load_music_files(), [
            os.path.join(music_path, "music.mp3"),
            os.path.join(music_path, "another_music.ogg")
        ])


class TestSoundFileLoader(unittest.TestCase):
    def test_sound_loader(self):
        sound_path = os.path.join(ASSETS, "media", "sound")

        sound_loader = SoundFileLoader(sound_path=sound_path)

        self.assertCountEqual(sound_loader.load_sound_files(), [
            os.path.join(sound_path, "sound.wav"),
            os.path.join(sound_path, "another_sound.ogg")
        ])