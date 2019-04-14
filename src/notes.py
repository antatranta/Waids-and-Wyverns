"""All Utilities for saving Notes file"""


class Notes:
    """Class to open notes.txt file"""

    def __init__(self):
        file = open("notes.txt", "w+")
        file.read()
        file.close()
