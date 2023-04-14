from unittest.mock import MagicMock, patch, call
from curses_wrapper import textbox
import pytest
import curses.textpad


def test_textbox_validate():
    assert textbox.validate(ord("a")) == ord("a")
    assert textbox.validate(curses.KEY_BACKSPACE) == curses.KEY_BACKSPACE
    assert textbox.validate(curses.KEY_RESIZE) == curses.ascii.BEL
    assert textbox.validate(textbox.KEY_ESCAPE) == curses.ascii.BEL
    assert textbox.validate(ord(" ")) == ord(" ")


def test_textbox_edit(mock_curses):
    with patch("curses.curs_set") as mock_curses_curs_set:
        with patch("curses.set_escdelay") as mock_curses_set_escdelay:
            with patch("curses.textpad.Textbox") as mock_curses_textbox:
                with patch("curses_wrapper.textbox.validate") as mock_textbox_validate:
                    mock_win = MagicMock()
                    mock_curses_textbox.return_value.gather.return_value = "mock text result"

                    result = textbox.edit(mock_win)

                    mock_curses_curs_set.assert_has_calls([call(1), call(0)])
                    mock_curses_set_escdelay.assert_has_calls([call(1), call(1000)])
                    mock_curses_textbox.assert_called_once_with(mock_win, insert_mode=True)
                    mock_curses_textbox.assert_has_calls(
                        [
                            call(mock_win, insert_mode=True),
                            call().edit(mock_textbox_validate),
                            call().gather(),
                        ]
                    )

                    assert result == "mock text result"
