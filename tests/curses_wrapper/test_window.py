from unittest.mock import MagicMock, patch
from curses_wrapper import CursesWindow
import curses
import pytest


def test_curses_window_init(curses_window):
    assert curses_window._lines == 5
    assert curses_window._cols == 10
    assert curses_window._y == 2
    assert curses_window._x == 2
    assert not curses_window.has_box
    assert curses.newwin.called


def test_curses_window_window(curses_window):
    assert curses_window.window == curses_window._window


def test_curses_window_lines(curses_window):
    assert curses_window.lines == 5


def test_curses_window_cols(curses_window):
    assert curses_window.cols == 10


def test_curses_window_y(curses_window):
    assert curses_window.y == 2


def test_curses_window_x(curses_window):
    assert curses_window.x == 2


def test_curses_window_size(curses_window):
    assert curses_window.size == (5, 10)


def test_curses_window_position(curses_window):
    assert curses_window.position == (2, 2)


# @property
# def addstr_ignore_curses_error(self):
#     return self._addstr_ignore_curses_error

# @addstr_ignore_curses_error.setter
# def addstr_ignore_curses_error(self, value):
#     bool_value = value == True
#     self._addstr_ignore_curses_error = bool_value


def test_curses_window_addstr(curses_window):
    with patch.object(curses_window.window, "addstr") as mock_addstr:
        y, x = 0, 0
        text = "testing, testing, 123"
        curses_window.addstr(y, x)
        mock_addstr.assert_called_with(y, x)

        # assert that all curses window.addstr args are handled
        curses_window.addstr(y, x, text, curses.A_BOLD)
        mock_addstr.assert_called_with(y, x, text, curses.A_BOLD)

        with patch.object(curses_window.window, "addstr") as mock_addstr:
            mock_addstr.side_effect = curses.error("_curses.error: addwstr() returned ERR")
            with pytest.raises(curses.error):
                curses_window.addstr(100000, 100000, text)

        with patch.object(curses_window.window, "addstr") as mock_addstr:
            mock_addstr.side_effect = curses.error("_curses.error: addwstr() returned ERR")
            curses_window.addstr(100000, 100000, text, ignore_curses_error=True)


def test_curses_window_addnstr(curses_window):
    with patch.object(curses_window.window, "addnstr") as mock_addnstr:
        y, x = 0, 0
        text = "testing, testing, 123"
        curses_window.addnstr(y, x)
        mock_addnstr.assert_called_with(y, x)

        # assert that all curses window.addnstr args are handled
        curses_window.addnstr(y, x, text, curses.A_BOLD)
        mock_addnstr.assert_called_with(y, x, text, curses.A_BOLD)

        with patch.object(curses_window.window, "addnstr") as mock_addnstr:
            mock_addnstr.side_effect = curses.error("_curses.error: addwstr() returned ERR")
            with pytest.raises(curses.error):
                curses_window.addnstr(100000, 100000, text)

        with patch.object(curses_window.window, "addnstr") as mock_addnstr:
            mock_addnstr.side_effect = curses.error("_curses.error: addwstr() returned ERR")
            curses_window.addnstr(100000, 100000, text, ignore_curses_error=True)


def test_curses_window_noutrefresh(curses_window):
    with patch.object(curses_window.window, "noutrefresh") as mock_noutrefresh:
        curses_window.noutrefresh()
        assert mock_noutrefresh.called


def test_curses_window_doupdate(curses_window):
    with patch.object(curses_window.window, "doupdate") as mock_doupdate:
        curses_window.doupdate()
        assert mock_doupdate.called


def test_curses_window_refresh(curses_window):
    with patch.object(curses_window.window, "refresh") as mock_refresh:
        curses_window.refresh()
        assert mock_refresh.called


def test_curses_window_resize(curses_window):
    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            with patch.object(curses_window, "noutrefresh") as mock_noutrefresh:
                curses_window.resize(10, 20)
                assert curses_window.lines == 10
                assert curses_window.cols == 20
                assert mock_resize.called
                assert not mock_refresh.called
                assert not mock_noutrefresh.called

    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            with patch.object(curses_window, "noutrefresh") as mock_noutrefresh:
                curses_window.resize(10, 20, should_noutrefresh=True)
                assert curses_window.lines == 10
                assert curses_window.cols == 20
                assert mock_resize.called
                assert not mock_refresh.called
                assert mock_noutrefresh.called

    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            with patch.object(curses_window, "noutrefresh") as mock_noutrefresh:
                curses_window.resize(10, 20, should_refresh=True)
                assert curses_window.lines == 10
                assert curses_window.cols == 20
                assert mock_resize.called
                assert mock_refresh.called
                assert not mock_noutrefresh.called

def test_curses_window_getattr(curses_window):
    with patch.object(curses_window.window, "hline") as mock_hline:
        curses_window.hline()
        mock_hline.assert_called_once()

    with patch.object(curses_window.window, "derwin") as mock_derwin:
        curses_window.derwin()
        mock_derwin.assert_called_once()

    with patch.object(curses_window.window, "getmaxyx") as mock_getmaxyx:
        curses_window.getmaxyx()
        mock_getmaxyx.assert_called_once()
