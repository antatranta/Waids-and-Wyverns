import sys
from unittest import TestLoader, TextTestRunner

if __name__ == "__main__":
    suite = TestLoader().discover('test', '*.py')
    runner = TextTestRunner().run(suite)
    exit_code = 0 if runner.wasSuccessful() else 1
    sys.exit(exit_code)
