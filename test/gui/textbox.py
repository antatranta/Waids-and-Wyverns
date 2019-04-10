import unittest
from unittest.mock import MagicMock, patch

import pygame
from src.gui.textbox import TextBox, TextArea, ALPHA_KEYS, NUMERIC_KEYS

class TestTextBox(unittest.TestCase):

    def test___init__(self):
        tb = TextBox((0, 0), (200, 200), initial_value="foobar", allowed=ALPHA_KEYS, center=True)
        self.assertEqual(tb.value, "foobar")
        self.assertEqual(tb.rect, pygame.Rect(0, 0, 200, 200))
        self.assertEqual(tb.selected, False)

    def test_select(self):
        tb = TextBox((0, 0), (200, 200))
        self.assertFalse(tb.selected, "initial state")

        with patch("pygame.mouse.get_pos", return_value=(100, 100)):
            tb.handle_events([MagicMock(type=pygame.MOUSEBUTTONUP)])
            self.assertTrue(tb.selected, "click on box")

        with patch("pygame.mouse.get_pos", return_value=(300, 300)):
            tb.handle_events([MagicMock(type=pygame.MOUSEBUTTONUP)])
            self.assertFalse(tb.selected, "click outside of box")

        tb.selected = True
        tb.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)])
        self.assertFalse(tb.selected, "press enter")

        tb.selected = True
        tb.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        self.assertFalse(tb.selected, "press escape")

    def test_typing(self):
        tb = TextBox((0, 0), (200, 200))
        self.assertEqual(tb.value, "")

        tb.selected = False
        tb.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_1, unicode='x')])
        self.assertEqual(tb.value, "")

        tb.selected = True
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode='a'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_1, unicode='1'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode=''),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode='b')]

        tb.handle_events(events)
        self.assertEqual(tb.value, "ab")

    def test_allowed(self):
        tb_num = TextBox((0, 0), (200, 200), allowed=NUMERIC_KEYS)
        self.assertEqual(tb_num.value, "")
        tb_num.selected = True

        tb_alpha = TextBox((0, 0), (200, 200), allowed=ALPHA_KEYS)
        self.assertEqual(tb_alpha.value, "")
        tb_alpha.selected = True

        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1, unicode='1'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode='a'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_0, unicode='0'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_2, unicode='@'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_z, unicode='Z'),
                  MagicMock(type=pygame.KEYDOWN, key=pygame.K_9, unicode='9')]

        tb_num.handle_events(events)
        self.assertTrue(tb_num.selected)
        tb_alpha.handle_events(events)

        self.assertEqual(tb_num.value, "109", "NUMERIC_KEYS")
        self.assertEqual(tb_alpha.value, "aZ", "ALPHA_KEYS")

class TestTextArea(unittest.TestCase):

    def test_cursor(self):
        ta = TextArea((0, 0), (100, 100), initial_value="hello world", always_selected=True)

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_w, unicode='W')])

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')])

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_h, unicode='H')])

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')])

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_COMMA, unicode=',')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')])

        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_DOWN, unicode='')])
        ta.handle_events([MagicMock(type=pygame.KEYDOWN, key=pygame.K_1, unicode='!')])

        self.assertEqual(ta.value, "Hello,\nWorld!")
