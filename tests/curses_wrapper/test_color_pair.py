from typing import Type, Dict, Tuple
from curses_wrapper import CursesColor
from curses_wrapper import CursesColorPair
import pytest
import curses


def test_curses_color_pair_init_pairs(curses_color):
    cc = CursesColorPair(curses_color)
    cc.init_pairs()
    cc.init_pairs("BLACK")
    cc.init_pairs("WHITE")
    assert "WHITE_ON_NONE" in cc.pair_name_to_number
    assert "WHITE_ON_BLACK" in cc.pair_name_to_number
    assert "RED_ON_WHITE" in cc.pair_name_to_number


def test_curses_color_pair_init_pair(curses_color):
    cc = CursesColorPair(curses_color)
    cc.init_pair("WHITE")
    cc.init_pair("WHITE", "BLUE")
    cc.init_pair("CYAN", "BLACK")
    assert "WHITE_ON_NONE" in cc.pair_name_to_number
    assert "WHITE_ON_BLUE" in cc.pair_name_to_number
    assert "CYAN_ON_BLACK" in cc.pair_name_to_number
    assert "GRAY_ON_BLACK" not in cc.pair_name_to_number


def test_curses_color_pair_next_pair_number(curses_color_pair):
    expected_next_pair_number = len(curses_color_pair._used_pair_numbers) + 1
    actual_next_pair_number = curses_color_pair.next_pair_number()
    assert actual_next_pair_number == expected_next_pair_number


def test_curses_color_pair_pair_name_to_number(curses_color_pair):
    assert len(curses_color_pair.pair_name_to_number) == len(curses_color_pair._pair_name_to_number)


def test_curses_color_pair__setitem__(curses_color_pair):
    curses_color_pair["CUSTOM"] = ("YELLOW", "BLUE")
    assert "CUSTOM" in curses_color_pair.pair_name_to_number


def test_curses_color_pair__getitem__(curses_color_pair):
    curses_color_pair["CYAN_ON_BLACK"] = ("CYAN", "BLACK")
    assert curses_color_pair["CYAN_ON_BLACK"] == curses_color_pair._pair_name_to_number["CYAN_ON_BLACK"]


def test_curses_color_pair_get(curses_color_pair):
    curses_color_pair["CYAN_ON_BLACK"] = ("CYAN", "BLACK")
    assert curses_color_pair.get("CYAN_ON_BLACK") == curses_color_pair._pair_name_to_number["CYAN_ON_BLACK"]


def test_curses_color_pair__iter__(curses_color_pair):
    pair_name_to_number_items = iter(curses_color_pair)
    assert "WHITE_ON_NONE" == next(pair_name_to_number_items)[0]


def test_curses_color_pair_items(curses_color_pair):
    assert "GRAY_ON_NONE" in dict(curses_color_pair.items())