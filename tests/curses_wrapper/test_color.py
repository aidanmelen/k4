from unittest.mock import patch
from curses_wrapper import CursesColor
import pytest
import curses
import os


# def test_start_color():
#     cc = CursesColor()

#     with pytest.raises(ValueError, match="Cannot change colors displayed by the terminal"):
#         cc.start_color()

#     os.environ["TERM"] = "xterm-256color"

#     with pytest.raises(ValueError, match="No extended color support found"):
#         cc.start_color()
    
def test_init_colors(curses_color):
    for color_name, color_rgb in curses_color._color_name_to_rgb.items():
        assert curses_color[color_name] == color_rgb

# def test_color_conversion(curses_color):
#     curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
#     assert curses_color.color_pair("WHITE", "BLACK") == 1

#     with pytest.raises(KeyError, match="Color name 'INVALID' not found"):
#         curses_color.color_pair("WHITE", "INVALID")

#     with pytest.raises(KeyError, match="Color name 'INVALID' not found"):
#         curses_color.color_pair("INVALID", "BLACK")


# def test_color_number_allocation(curses_color):
#     for color_name in curses_color._color_name_to_rgb.keys():
#         assert isinstance(curses_color[color_name], int)
#         assert curses_color[color_name] not in curses_color._used_color_numbers

#     with pytest.raises(ValueError, match="No more color pairs available"):
#         for _ in range(16):
#             curses_color.allocate_color_pair()

#     assert curses_color.allocate_color_pair() in curses_color._used_color_numbers


# def test_color_pair_setting_and_deallocation(curses_color):
#     curses_color.allocate_color_pair()
#     curses_color.set_color_pair("MY_COLOR", "WHITE", "BLACK")
#     assert curses_color["MY_COLOR"] == curses_color.color_pair("WHITE", "BLACK")
#     assert curses_color.color_pair("MY_COLOR", fallback=None) is None

#     with pytest.raises(KeyError, match="Color name 'INVALID' not found"):
#         curses_color.set_color_pair("MY_COLOR", "WHITE", "INVALID")

#     with pytest.raises(KeyError, match="Color name 'INVALID' not found"):
#         curses_color.set_color_pair("MY_COLOR", "INVALID", "BLACK")

#     with pytest.raises(KeyError, match="Color name 'MY_COLOR' not found"):
#         curses_color.deallocate_color_pair("MY_COLOR")

#     assert curses_color.deallocate_color_pair("WHITE", "BLACK") in curses_color._used_color_numbers


# def test_color_pair_caching(curses_color):
#     assert curses_color.color_pair("WHITE", "BLACK") == curses_color.color_pair("WHITE", "BLACK")
#     curses_color.allocate_color_pair()
#     assert curses_color.color_pair("WHITE", "BLACK") != curses_color.color_pair("WHITE", "BLACK")