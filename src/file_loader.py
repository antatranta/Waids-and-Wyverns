""" All utilities and class for map preloading into a list """
#pylint: disable=too-few-public-methods
import os


class MapFileLoader:
    """ Class to load the map files (png, jpg, etc) """

    def __init__(self):
        self.map_path = os.path.join(".", "assets", "images", "maps")

    def load_map_files(self):
        """ Loads the map files into map_files list """
        maps = []
        for map_file in os.listdir(self.map_path):
            if map_file.endswith(".png") or map_file.endswith(".jpg"):
                maps.append(os.path.join(self.map_path, map_file))

        return maps


class CharacterFileLoader:
    """ Class to load the character files (png, jpg, etc) """

    def __init__(self):
        self.character_path = os.path.join(".", "assets", "images", "characters")

    def load_character_files(self):
        """ Loads the character files into characters list """
        characters = []
        for character_file in os.listdir(self.character_path):
            if character_file.endswith(".png") or character_file.endswith(".jpg"):
                characters.append(os.path.join(self.character_path, character_file))

        return characters
