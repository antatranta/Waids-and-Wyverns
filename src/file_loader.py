""" All utilities and class for map preloading into a list """
import os


class MapFileLoader:
    """ Class to load the map files (png, jpg, etc) """

    def __init__(self, map_path=None):
        self.maps = []
        self.map_path = map_path or os.path.join(".", "assets", "images", "maps")
        self.load_map_files()

    def load_map_files(self):
        """ Loads the map files into map_files list """
        for map_file in os.listdir(self.map_path):
            if map_file.endswith(".png") or map_file.endswith(".jpg"):
                self.maps.append(os.path.join(self.map_path, map_file))

    def get_map_files(self):
        """ Gets the array of map files' location """
        return self.maps


class CharacterFileLoader:
    """ Class to load the character files (png, jpg, etc) """

    def __init__(self, character_path=None):
        self.characters = []
        self.character_path = character_path or os.path.join(".", "assets", "images", "characters")
        self.load_character_files()

    def load_character_files(self):
        """ Loads the character files into characters list """
        for character_file in os.listdir(self.character_path):
            if character_file.endswith(".png") or character_file.endswith(".jpg"):
                self.characters.append(os.path.join(self.character_path, character_file))

    def get_character_files(self):
        """ Gets the array of character files' location """
        return self.characters
