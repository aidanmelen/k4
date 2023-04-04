from curses_wrapper import CursesWindowText
import pytest

@pytest.fixture
def curses_window_text(curses_window):
    return CursesWindowText(curses_window)

def test_align_left(curses_window_text):
    assert curses_window_text.align_left("test", 6) == "test  "
    assert curses_window_text.align_left("test", 2) == "test"
    assert curses_window_text.align_left("test") == "test      "

def test_align_right(curses_window_text):
    assert curses_window_text.align_right("test", 6) == "  test"
    assert curses_window_text.align_right("test", 2) == "test"
    assert curses_window_text.align_right("test") == "      test"

def test_align_center(curses_window_text):
    assert curses_window_text.align_center("testy", 7) == " testy "
    assert curses_window_text.align_center("testy", 3) == "testy"
    assert curses_window_text.align_center("testy") == "  testy   "

def test_shorten(curses_window_text):
    text = "This is a long sentence that needs to be shortened."
    assert curses_window_text.shorten(text, 20) == "This is a long [...]"
    assert curses_window_text.shorten(text, 20, placeholder='') == "This is a long"
    assert curses_window_text.shorten(text) == "This [...]"

def test_wrap(curses_window_text):
    text = "This is a long sentence that needs to be wrapped."
    wrapped = curses_window_text.wrap(text, 15)
    assert wrapped == ['This is a long', 'sentence that', 'needs to be', 'wrapped.']
    assert len(wrapped[0]) <= 15

def test_fill(curses_window_text):
    text = "This is a long sentence that needs to be filled."
    filled = curses_window_text.fill(text, 15)
    assert filled == "This is a long\nsentence that\nneeds to be\nfilled."