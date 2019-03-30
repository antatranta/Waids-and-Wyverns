""" All utilities and class for map preloading into a list """
#pylint: disable=too-few-public-methods
import os


class MapFileLoader:
    """ Class to load the map files (png, jpg, etc) """

    def __init__(self):
        self.map_files = []
        self.map_path = os.path.join(".", "assets", "images", "maps")

    def load_map_files(self):
        """ Loads the map files into map_files list """

        for map_file in os.listdir(self.map_path):
            if map_file.endswith(".png") or map_file.endswith(".jpg"):
                self.map_files.append(os.path.join(self.map_path, map_file))


class CharacterFileLoader:
    """ Class to load the character files (png, jpg, etc) """

    def __init__(self):
        self.characters = []
        self.character_path = os.path.join(".", "assets", "images", "characters")

    def load_character_files(self):
        """ Loads the character files into characters list """

        for character_file in os.listdir(self.character_path):
            if character_file.endswith(".png") or character_file.endswith(".jpg"):
                self.characters.append(os.path.join(self.character_path, character_file))
