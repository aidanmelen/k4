from typing import Tuple, List
import textwrap
import curses
import time


class CursesWindow:
    """A wrapper around the curses window functionality.

    This class provides a higher-level interface to the curses window
    functionality.
    """

    def __init__(
        self, lines: int, cols: int, y: int = 0, x: int = 0, has_box: bool = False
    ) -> None:
        """
        Initialize a CursesWindow object.

        Args:
        - lines (int): the lines of the window
        - cols (int): the cols of the window
        - y (int, optional): the y-coordinate of the top left corner of the window. Default is 0.
        - x (int, optional): the x-coordinate of the top left corner of the window. Default is 0.
        - has_box (bool, optional): whether or not to draw a box around the window. Default is False.
        """
        self._lines = lines
        self._cols = cols
        self._y = y
        self._x = x
        self.has_box = has_box
        self._window = curses.newwin(lines, cols, y, x)
        self._refresh_time = time.perf_counter()
        self._refresh_elapsed_time = 0.0
        self._addstr_ignore_curses_error = False

    @property
    def window(self) -> curses.window:
        """Returns the curses.window object associated with this CursesWindow."""
        return self._window

    @property
    def lines(self) -> int:
        """Returns the lines size of the window."""
        return self._lines

    @property
    def cols(self) -> int:
        """Returns the cols size of the window."""
        return self._cols

    @property
    def y(self) -> int:
        """Returns the y position of the window."""
        return self._y

    @property
    def x(self) -> int:
        """Returns the x position of the window."""
        return self._x

    @property
    def size(self) -> Tuple[int, int]:
        """Returns the size (lines, cols) of the window."""
        return (self._lines, self._cols)

    @property
    def position(self) -> Tuple[int, int]:
        """Returns the position (y, x) of the top left corner of the window."""
        return (self._y, self._x)

    @property
    def center_position(self) -> Tuple[int, int]:
        return (self._lines // 2, self._cols // 2)

    @property
    def refresh_time(self) -> float:
        """Returns the time (in seconds) since the window was last refreshed."""
        return self._refresh_time

    @property
    def refresh_elapsed_time(self) -> float:
        return self._refresh_elapsed_time

    def _update_refresh_time(self) -> None:
        """Update the refresh time and the elapsed time since the last refresh."""
        current_time = time.perf_counter()
        self._refresh_elapsed_time = round(current_time - self._refresh_time, 9)
        self._refresh_time = current_time

    def getmaxyx(self) -> None:
        """Return a tuple (y, x) of the height and width of the window."""
        return self._window.getmaxyx()

    @property
    def addstr_ignore_curses_error(self):
        return self._addstr_ignore_curses_error
    
    @addstr_ignore_curses_error.setter
    def addstr_ignore_curses_error(self, value):
        bool_value = value == True
        self._addstr_ignore_curses_error = bool_value

    def addstr(self, *args, ignore_curses_error=False):
        """Paint the character string str at (y, x) with attributes attr, overwriting anything previously on the display."""
        try:
            self.window.addstr(*args)
        except curses.error as e:
            # Writing outside the window, subwindow, or pad raises curses.error.
            if any([self.addstr_ignore_curses_error, ignore_curses_error]):
                pass
            else:
                raise e

    def addnstr(self, *args, ignore_curses_error=False):
        """Paint at most n characters of the character string str at (y, x) with attributes attr, overwriting anything previously on the display."""
        try:
            self.window.addnstr(*args)
        except curses.error as e:
            # Writing outside the window, subwindow, or pad raises curses.error.
            if any([self.addstr_ignore_curses_error, ignore_curses_error]):
                pass
            else:
                raise e

    def noutrefresh(self) -> None:
        """Mark for refresh but wait."""
        self._window.noutrefresh()

    def doupdate(self) -> None:
        """Update the physical screen."""
        self._window.doupdate()
        self._update_refresh_time()

    def refresh(self) -> None:
        """Refresh the window and update the current refresh time."""
        self._window.refresh()
        self._update_refresh_time()

        if self.has_box:
            self._window.box()

    def resize(self, lines: int, cols: int, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the specified lines and cols."""
        self._lines = lines
        self._cols = cols

        self.clear()
        self._window.resize(self._lines, self._cols)

        if should_refresh:
            self.refresh()

        if should_noutrefresh:
            self.noutrefresh()

    def resize_max_lines(self, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the maximum lines of the entire terminal screen."""
        curses.update_lines_cols()
        self.resize(curses.LINES, self._cols, should_refresh, should_noutrefresh)

    def resize_max_cols(self, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the maximum columes of the entire terminal screen."""
        curses.update_lines_cols()
        self.resize(self._lines, curses.COLS, should_refresh, should_noutrefresh)

    def resize_max(self, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the maximum size of the entire terminal screen."""
        curses.update_lines_cols()
        self.resize(curses.LINES, curses.COLS, should_refresh, should_noutrefresh)

    def clear(self) -> None:
        """Clear the contents of the window."""
        self._window.clear()


class CursesWindowText:
    """A wrapper around the curses window functionality.

    This class provides a higher-level interface to the curses window
    functionality.

    Attributes:
        PADDING (int): the size of padding.
    """

    PADDING = 1

    def __init__(self, window: CursesWindow) -> None:
        """
        Initialize a CursesWindowText object.

        Arguments:
            window (CursesWindow): The CursesWindow object.
        """
        self.__window = window
    
    def align_left(self, text: str, width: int = None) -> str:
        """Align left and pad the given text given width."""
        if not width:
            width = self.__window.cols
        return "{:<{}}".format(text, width)
    
    def align_right(self, text: str, width: int = None) -> str:
        """Align right and pad the given text given width."""
        if not width:
            width = self.__window.cols
        return "{:>{}}".format(text, width)
    
    def align_center(self, text: str, width: int = None) -> str:
        """Align center and pad the given text given width."""
        if not width:
            width = self.__window.cols
        return "{:^{}}".format(text, width)

    def shorten(self, text: str, width: int = None, **kwargs) -> str:
        """Collapse and truncate the given text to fit in the given width."""
        if not width:
            width = self.__window.cols
        return textwrap.shorten(text, width, **kwargs)

    def wrap(self, text: str, width: int = None, **kwargs) -> List[str]:
        """Wraps the single paragraph in text (a string) so every line is at most width characters long. Returns a list of output lines, without final newlines."""
        if not width:
            width = self.__window.cols
        return textwrap.wrap(text, width, **kwargs)
    
    def fill(self, text: str, width: int = None, **kwargs) -> str:
        if not width:
            width = self.__window.cols
        return textwrap.fill(text, width, **kwargs)