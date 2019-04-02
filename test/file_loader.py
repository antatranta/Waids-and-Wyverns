import unittest
import os
from src.file_loader import MapFileLoader, CharacterFileLoader

ASSETS = os.path.join(".", "test", "fixtures", "assets")

class TestMapFileLoader(unittest.TestCase):
    def test_file_loader(self):
        map_path = os.path.join(ASSETS, "images", "maps")

        Loader = MapFileLoader(map_path=map_path)

        self.assertCountEqual(Loader.load_map_files(), [
            os.path.join(map_path, "my_map.jpg"),
            os.path.join(map_path, "another_map.png"),
        ])


class TestCharacterLoader(unittest.TestCase):
    def test_character_loader(self):
        character_path = os.path.join(ASSETS, "images", "characters")

        CharLoader = CharacterFileLoader(character_path=character_path)

        self.assertCountEqual(CharLoader.load_character_files(), [
            os.path.join(character_path, "another_character.png"),
            os.path.join(character_path, "character1.jpg"),
        ])
