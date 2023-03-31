from typing import Dict, Tuple
from unittest.mock import MagicMock, patch
from curses_wrapper import CursesColor
import curses
import pytest

@pytest.fixture
def mock_curses():
    with patch("curses.initscr"), \
         patch("curses.start_color"), \
         patch("curses.can_change_color"), \
         patch("curses.use_default_colors"):
        yield

@pytest.fixture
def curses_color(mock_curses):
    curses.COLORS = 256

    cc = CursesColor()
    cc.start_color()
    cc.init_colors()
    return cc