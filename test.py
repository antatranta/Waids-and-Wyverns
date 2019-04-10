import sys
from unittest import TestLoader, TextTestRunner

import pygame

if __name__ == "__main__":
    pygame.font.init()

    suite = TestLoader().discover('test', '*.py')
    runner = TextTestRunner().run(suite)
    exit_code = 0 if runner.wasSuccessful() else 1
    sys.exit(exit_code)
