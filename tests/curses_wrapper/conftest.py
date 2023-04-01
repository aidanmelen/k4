from typing import Dict, Tuple
from unittest.mock import MagicMock, patch
from curses_wrapper import CursesColor, CursesColorPair
import curses
import pytest

@pytest.fixture
def mock_curses():
    with patch("curses.initscr"), \
         patch("curses.start_color"), \
         patch("curses.can_change_color"), \
         patch("curses.use_default_colors"), \
         patch("curses.init_color"), \
         patch("curses.init_pair"), \
         patch("curses.color_pair"), \
         patch("curses.color_content"):
        yield

@pytest.fixture
def curses_color(mock_curses):
    curses.COLORS = 256
    curses.COLOR_PAIRS = 32765
    cc = CursesColor()
    cc.start_color()
    cc.init_colors()
    return cc

@pytest.fixture
def curses_color_pair(curses_color):
    cc = CursesColorPair(curses_color)
    cc.init_pairs()
    return cc