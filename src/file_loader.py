""" All utilities and class for map preloading into a list """
import os
from tkinter import Tk, filedialog


class FileLoader:
    """Base class to help with file loading."""

    def __init__(self, root, filetypes=None):
        """
        Initialize a FileLoader object.

        :param root:      Directory to load files from.
        :param filetypes: List of filetype suffixes (eg. '.txt') that this
                          FileLoader allows. If None all files are allowed.
        """
        self.root = root
        self.filetypes = filetypes if filetypes is not None else ['']

    def file_dialog(self):
        """Open a file dialog to select file."""
        Tk().withdraw()
        filetypes = [("Files", [f"*{suffix}" for suffix in self.filetypes]), ("All Files", "*")]
        return filedialog.askopenfilename(initialdir=self.root, filetypes=filetypes)

    def get_files(self):
        """Returns a list of all files of this loader."""
        files = []
        for file in os.listdir(self.root):
            if any([file.endswith(suffix) for suffix in self.filetypes]):
                files.append(os.path.join(self.root, file))
        return files


class MapFileLoader(FileLoader):
    """ Class to load the map files (png, jpg, etc) """

    def __init__(self, map_path=None):
        map_path = map_path or os.path.join(".", "assets", "images", "maps")
        super().__init__(map_path, [".jpg", ".png"])

    def load_map_files(self):
        """ Loads the map files into a list """
        return self.get_files()


class CharacterFileLoader(FileLoader):
    """ Class to load the character files (png, jpg, etc) """

    def __init__(self, character_path=None):
        character_path = character_path or os.path.join(".", "assets", "images", "characters")
        super().__init__(character_path, [".jpg", ".png"])

    def load_character_files(self):
        """ Loads the character files into characters list """
        return self.get_files()


class MusicFileLoader(FileLoader):
    """ Class to load music files (mp3 and ogg) """

    def __init__(self, music_path=None):
        music_path = music_path or os.path.join(".", "assets", "media", "music")
        super().__init__(music_path, [".mp3", ".ogg"])

    def load_music_files(self):
        """ Loads the music files into a list """
        return self.get_files()


class SoundFileLoader(FileLoader):
    """ Class to load sound files (wav and ogg) """

    def __init__(self, sound_path=None):
        sound_path = sound_path or os.path.join(".", "assets", "media", "sound")
        super().__init__(sound_path, [".wav", ".ogg"])

    def load_sound_files(self):
        """ Loads the sound files into a list """
        return self.get_files()
