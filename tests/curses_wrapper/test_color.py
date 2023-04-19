from unittest.mock import patch
from curses_wrapper import CursesColor
import pytest
import curses
import os


def test_curses_color_start_color(mock_curses):
    curses.COLORS = 256
    cc = CursesColor()
    cc.start_color()
    assert curses.can_change_color.called
    assert curses.use_default_colors.called


def test_curses_color_start_color_when_cannot_change_color(mock_curses):
    curses.COLORS = 256
    cc = CursesColor()

    os.environ["TERM"] = "xterm-256color"
    curses.can_change_color.return_value = False

    with pytest.raises(Exception, match="Cannot change colors displayed by the terminal."):
        cc.start_color()


def test_curses_color_start_color_without_extended_colors(mock_curses):
    curses.COLORS = 256
    cc = CursesColor()

    os.environ["TERM"] = "unknown"
    curses.can_change_color.return_value = True

    with pytest.raises(Exception, match="No extended color support found."):
        cc.start_color()

    os.environ["TERM"] = "xterm-256color"


def test_curses_color_init_colors(curses_color):
    assert list(curses_color.color_name_to_number.keys()) == ['WHITE', 'BLACK', 'RED', 'GREEN', 'BLUE']


def test_curses_color_has_colors(mock_curses):
    curses.COLORS = 256
    cc = CursesColor()
    assert not cc.has_colors

    cc.start_color()
    cc.init_colors(color_names = ['WHITE', 'BLACK', 'RED', 'GREEN', 'BLUE'])
    assert cc.has_colors


def test_curses_color_color_content_by_name(curses_color):
    curses_color.color_content_by_name("WHITE")
    assert curses.color_content.called


def test_curses_color_color_name_to_number(curses_color):
    curses_color.color_content_by_number("WHITE")
    assert curses.color_content.called


def test_curses_color_is_color_initialized(curses_color):
    # assign color number from COLOR-1 (256) to 0
    for color_name in ["WHITE", "BLACK", "RED", "GREEN", "BLUE"]:
        expected_color_number = curses_color.color_name_to_number[color_name]
        assert curses_color.is_color_initialized(expected_color_number)

    # color 50 should not be set because we only have like 50 pre-defined colors
    assert not curses_color.is_color_initialized(50)
    assert not curses_color.is_color_initialized(45)
    assert not curses_color.is_color_initialized(40)


def test_curses_color_next_color_number(curses_color):
    expected_next_color_number = min(curses_color.color_name_to_number.values()) - 1
    actual_next_color_number = curses_color.next_color_number()
    assert actual_next_color_number == expected_next_color_number


def test_curses_color__setitem__(curses_color):
    next_color_number = curses_color.next_color_number()
    assert next_color_number not in curses_color._used_color_numbers
    curses_color["CUSTOM"] = (1, 2, 3)
    assert curses_color.color_name_to_number["CUSTOM"] == next_color_number
    assert next_color_number in curses_color._used_color_numbers
    assert curses.init_color.called


def test_curses_color__setitem__with_existing_color(curses_color):
    previous_used_color_numbers_count = len(curses_color._used_color_numbers)
    previous_color_content = curses_color._color_name_to_rgb["WHITE"]
    curses_color["WHITE"] = (1, 2, 3)

    # no new color was added
    assert previous_used_color_numbers_count == len(curses_color._used_color_numbers)

    # but the WHITE RBG 3-tuple was updated
    assert curses_color._color_name_to_rgb["WHITE"] != previous_color_content
    assert curses.init_color.called


def test_curses_color__setitem__when_max_colors(curses_color):
    # artificially fill colors
    for color_number in range(curses.COLORS - 1, -1, -1):
        curses_color._used_color_numbers.add(color_number)

    with pytest.raises(Exception, match=f"All {curses.COLORS} colors are set."):
        curses_color["MAX_COLOR"] = (1, 2, 3)


def test_curses_color__getitem__(curses_color):
    assert curses_color["RED"] == curses_color.color_name_to_number["RED"]
    assert curses_color["GREEN"] == curses_color.color_name_to_number["GREEN"]
    assert curses_color["BLUE"] == curses_color.color_name_to_number["BLUE"]


def test_curses_color_get(curses_color):
    assert curses_color["RED"] == curses_color.get("RED")
    assert curses_color.COLOR_DEFAULT == curses_color.get("FAKE")
    assert 10 == curses_color.get("FAKE", 10)


def test_curses_color__iter__(curses_color):
    color_name_to_number_iter = iter(curses_color)
    assert ("WHITE", 255) == next(color_name_to_number_iter)
    assert ("BLACK", 254) == next(color_name_to_number_iter)
    assert ("RED", 253) == next(color_name_to_number_iter)


def test_curses_color_items(curses_color):
    color_name_to_number_items = dict(curses_color.items())
    assert color_name_to_number_items["RED"] == 253
    assert color_name_to_number_items["GREEN"] == 252
    assert color_name_to_number_items["BLUE"] == 251
