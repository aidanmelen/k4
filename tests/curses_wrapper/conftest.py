from typing import Dict, Tuple
from unittest.mock import patch
from curses_wrapper import CursesColor, CursesColorPair
import curses
import pytest


@pytest.fixture
def mock_curses():
    curses.COLORS = 256
    curses.COLOR_PAIRS = 32765
    curses.LINES = 100
    curses.COLS = 100

    # fmt: off
    with patch("curses.initscr"), \
         patch("curses.start_color"), \
         patch("curses.can_change_color"), \
         patch("curses.use_default_colors"), \
         patch("curses.init_color"), \
         patch("curses.init_pair"), \
         patch("curses.color_pair"), \
         patch("curses.color_content"), \
         patch("curses.newwin"):
        yield


@pytest.fixture
def curses_color(mock_curses):
    cc = CursesColor()
    cc.start_color()
    cc.init_colors(color_names=["WHITE", "BLACK", "RED", "GREEN", "BLUE"])
    return cc


@pytest.fixture
def curses_color_pair(curses_color):
    cc = CursesColorPair(curses_color)
    cc.init_pairs()
    return cc
