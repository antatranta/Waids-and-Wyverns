from unittest import TestLoader, TextTestRunner

if __name__ == "__main__":
    suite = TestLoader().discover('test', '*.py')
    TextTestRunner().run(suite)
