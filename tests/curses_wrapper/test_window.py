from unittest.mock import MagicMock, patch
from curses_wrapper import CursesWindow
import curses
import time
import pytest


def test_curses_window_init(curses_window):
    assert curses_window._h == 5
    assert curses_window._w == 10
    assert curses_window._y == 2
    assert curses_window._x == 2
    assert not curses_window.should_box
    assert curses_window._refresh_time == 1.0
    assert curses_window._refresh_elapsed_time == 0
    assert curses.newwin.called


def test_curses_window_window(curses_window):
    assert curses_window.window == curses_window._window


def test_curses_window_size(curses_window):
    assert curses_window.size == (5, 10)


def test_curses_window_position(curses_window):
    assert curses_window.position == (2, 2)


def test_curses_window_refresh_time(curses_window):
    assert curses_window.refresh_time == 1.0


def test_curses_window_update_refresh_time(curses_window, mock_time_perf_counter):
    mock_time_perf_counter.return_value = 5.0
    curses_window._update_refresh_time()
    assert curses_window.refresh_time == 5.0


def test_curses_window_update_max_size(curses_window):
    with patch.object(curses_window._window, "getmaxyx") as mock_getmaxyx:
        mock_getmaxyx.return_value = (200, 200)
        curses_window.update_max_size()
        assert curses_window._max_h == 200
        assert curses_window._max_w == 200


def test_curses_window_addstr(curses_window):
    with patch.object(curses_window.window, "addstr") as mock_addstr:
        h, w, y, x = 1, 2, 3, 4
        curses_window.addstr(h, w)
        mock_addstr.assert_called_with(h, w)

        curses_window.addstr(h, w, y, x)
        mock_addstr.assert_called_with(h, w, y, x)


def test_curses_window_addstr_when_raise_on_curses_error_true(curses_window):
    with patch.object(curses_window.window, "addstr") as mock_addstr:
        mock_addstr.side_effect = curses.error("_curses.error: addwstr() returned ERR")

        h, w, y, x = 1, 2, 3, 4
        with pytest.raises(curses.error):
            curses_window.addstr(h, w)


def test_curses_window_addstr_when_raise_on_curses_error_false(curses_window):
    with patch.object(curses_window.window, "addstr") as mock_addstr:
        mock_addstr.side_effect = curses.error("_curses.error: addwstr() returned ERR")

        h, w, y, x = 1, 2, 3, 4
        curses_window.addstr(h, w, raise_on_curses_error=False)


def test_curses_window_refresh(curses_window):
    with patch.object(curses_window.window, "noutrefresh") as mock_noutrefresh:
        with patch("curses.doupdate") as mock_doupdate:
            curses_window.refresh()
            assert mock_noutrefresh.called
            assert mock_doupdate.called


def test_curses_window_refresh_when_defer_true(curses_window):
    with patch.object(curses_window.window, "noutrefresh") as mock_noutrefresh:
        with patch("curses.doupdate") as mock_doupdate:
            curses_window.refresh(defer=True)
            assert mock_noutrefresh.called
            assert not mock_doupdate.called


def test_curses_window_resize(curses_window):
    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            curses_window.resize(8, 12)
            assert curses_window._h == 8
            assert curses_window._w == 12
            assert mock_resize.called
            mock_refresh.assert_called_once_with(defer=False)


def test_curses_window_resize_when_defer_refresh_true(curses_window):
    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            curses_window.resize(15, 20, defer_refresh=True)
            assert curses_window._h == 15
            assert curses_window._w == 20
            assert mock_resize.called
            mock_refresh.assert_called_once_with(defer=True)
        

def test_curses_window_resize_max_height(curses_window):
    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            with patch.object(curses_window, "update_max_size") as mock_update_max_size:
                curses_window._max_h = 200
                curses_window.resize_max_height()
                assert curses_window._h == 200
                assert curses_window._w == 10
                assert mock_resize.called
                mock_refresh.assert_called_once_with(defer=False)


def test_curses_window_resize_max_width(curses_window):
    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            with patch.object(curses_window, "update_max_size") as mock_update_max_size:
                curses_window._max_w = 200
                curses_window.resize_max_width()
                assert curses_window._h == 5
                assert curses_window._w == 200
                assert mock_resize.called
                mock_refresh.assert_called_once_with(defer=False)


def test_curses_window_resize_max_size(curses_window):
    with patch.object(curses_window.window, "resize") as mock_resize:
        with patch.object(curses_window, "refresh") as mock_refresh:
            with patch.object(curses_window, "update_max_size") as mock_update_max_size:
                curses_window._max_h = 200
                curses_window._max_w = 200
                curses_window.resize_max_size()
                assert curses_window._h == 200
                assert curses_window._w == 200
                assert mock_resize.called
                mock_refresh.assert_called_once_with(defer=False)


def test_curses_window_move(curses_window):
    with patch.object(curses_window.window, "move") as mock_move:
        with patch.object(curses_window, "refresh") as mock_refresh:
            curses_window.move(4, 6)
            mock_move.assert_called_once_with(4, 6)
            assert curses_window.position == (4, 6)
            mock_refresh.assert_called_with(defer=False)


def test_curses_window_clear(curses_window):
    with patch.object(curses_window.window, "clear") as mock_clear:
        curses_window.clear()
        assert mock_clear.called


def test_curses_window_erase(curses_window):
    with patch.object(curses_window.window, "erase") as mock_erase:
        curses_window.erase()
        assert mock_erase.called