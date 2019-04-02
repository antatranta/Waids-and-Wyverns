import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.gui.utils import DraggableMixin

class RectDraggable(DraggableMixin):
    def __init__(self, rect):
        self._pos = rect.topleft
        self.rect = rect
        DraggableMixin.__init__(self, rect.topleft)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self.rect.topleft = pos
        self._pos = pos

class TestDraggableMixin(unittest.TestCase):

    def test_drag(self):
        rect = RectDraggable(pygame.Rect(0, 0, 100, 100))

        rect.handle_events([MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(200, 200), button=1),
                            MagicMock(type=pygame.MOUSEMOTION, pos=(400, 400), buttons=(1, 0, 0)),
                            MagicMock(type=pygame.MOUSEBUTTONUP, pos=(400, 400), button=1)])

        self.assertEqual(rect.pos, (0, 0))

        rect.handle_events([MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(50, 50), button=1),
                            MagicMock(type=pygame.MOUSEMOTION, pos=(200, 200), buttons=(1, 0, 0)),
                            MagicMock(type=pygame.MOUSEBUTTONUP, pos=(200, 200), button=1)])

        self.assertEqual(rect.pos, (150, 150))

        rect.handle_events([MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(150, 150), button=1),
                            MagicMock(type=pygame.MOUSEMOTION, pos=(160, 160), buttons=(1, 0, 0)),
                            MagicMock(type=pygame.MOUSEBUTTONUP, pos=(160, 160), button=1),
                            MagicMock(type=pygame.MOUSEMOTION, pos=(0, 0), buttons=(1, 0, 0))])

        self.assertEqual(rect.pos, (160, 160))
