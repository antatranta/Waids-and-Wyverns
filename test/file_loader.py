import unittest
import os
from src.file_loader import MapFileLoader, CharacterFileLoader

class TestMapFileLoader(unittest.TestCase):
    def test_file_loader(self):
        Loader = MapFileLoader()
        Loader.load_map_files()

        self.assertListEqual(Loader.get_map_files(), [os.path.join(".", "assets", "images", "maps", "placeholder.jpg")])

    
class TestCharacterLoader(unittest.TestCase):
    def test_character_loader(self):
        CharLoader = CharacterFileLoader()
        CharLoader.load_character_files()

        self.assertListEqual(CharLoader.get_character_files(), [os.path.join(".", "assets", "images", "characters")])