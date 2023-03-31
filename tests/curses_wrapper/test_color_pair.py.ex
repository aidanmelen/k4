from typing import Type, Dict, Tuple

from curses_wrapper import CursesColor
from curses_wrapper import CursesColorPair

import pytest
import curses



@pytest.fixture
def curses_color():
    return CursesColor()


@pytest.fixture
def curses_color_pair(curses_color):
    return CursesColorPair(curses_color)


def test_init_pairs(curses_color_pair):
    with pytest.raises(RuntimeError):
        curses_color_pair.init_pairs()

    curses_color_pair._curses_color.init_colors()
    curses_color_pair.init_pairs()

    for fg_color_name, fg_color_number in curses_color_pair._curses_color:
        pair_name = f"{fg_color_name}_ON_BLACK"
        assert pair_name in curses_color_pair.pair_name_to_number


def test_init_pair(curses_color_pair):
    curses_color_pair._curses_color.init_colors()

    with pytest.raises(ValueError):
        curses_color_pair.init_pair(fg_color_name="not a color")

    with pytest.raises(ValueError):
        curses_color_pair.init_pair(bg_color_name="not a color")

    curses_color_pair.init_pair(fg_color_name="white", bg_color_name="black")

    assert "WHITE_ON_BLACK" in curses_color_pair.pair_name_to_number


def test_next_pair_number(curses_color_pair):
    next_pair_number = curses_color_pair.next_pair_number()

    assert isinstance(next_pair_number, int)
    assert next_pair_number not in curses_color_pair._used_pair_numbers


def test_pair_name_to_number(curses_color_pair):
    assert isinstance(curses_color_pair.pair_name_to_number, dict)


def test_setitem(curses_color_pair):
    curses_color_pair._curses_color.init_colors()
    curses_color_pair["RED_ON_BLACK"] = ("red", "black")

    assert "RED_ON_BLACK" in curses_color_pair.pair_name_to_number


def test_getitem(curses_color_pair):
    curses_color_pair._curses_color.init_colors()
    curses_color_pair["GREEN_ON_BLACK"] = ("green", "black")

    assert curses_color_pair["GREEN_ON_BLACK"] in range(1, COLOR_PAIRS - 1)


def test_get(curses_color_pair):
    curses_color_pair._curses_color.init_colors()
    curses_color_pair["YELLOW_ON_BLACK"] = ("yellow", "black")

    assert curses_color_pair.get("YELLOW_ON_BLACK") in range(1, COLOR_PAIRS - 1)
    assert curses_color_pair.get("not a color", default=5) == 5


def test_iter(curses_color_pair):
    assert isinstance(iter(curses_color_pair), tuple)


def test_items(curses_color_pair):
    assert isinstance(curses_color_pair.items(), dict.items)
