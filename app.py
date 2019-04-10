import pygame
from src.menu_screen import MainMenuScreen

if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(500, 50)

    MainMenuScreen().open()
