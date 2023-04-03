from typing import Tuple
import curses
import time


class CursesWindow:
    """A wrapper around the curses window functionality.

    This class provides a higher-level interface to the curses window
    functionality.

    Attributes:
        PADDING (int): the size of padding.
    """
    PADDING = 1

    def __init__(self, height: int, width: int, y: int, x: int, should_box: bool = False) -> None:
        """
        Initialize a CursesWindow object.

        Args:
        - height (int): the height of the window
        - width (int): the width of the window
        - y (int): the y-coordinate of the top left corner of the window
        - x (int): the x-coordinate of the top left corner of the window
        - box (bool, optional): whether or not to draw a box around the window. Default is False.
        """
        self._h = height
        self._w = width
        self._y = y
        self._x = x
        self._max_h = curses.LINES
        self._max_w = curses.COLS
        self.should_box = should_box

        self._window = curses.newwin(height, width, y, x)
        self._window.box()

        self._refresh_time = time.perf_counter()
        self._refresh_elapsed_time = 0.0


    @property
    def window(self) -> curses.window:
        """Returns the curses.window object associated with this CursesWindow."""
        return self._window

    @property
    def size(self) -> Tuple[int, int]:
        """Returns the size (height, width) of the window."""
        return (self._h, self._w)

    @property
    def position(self) -> Tuple[int, int]:
        """Returns the position (y, x) of the top left corner of the window."""
        return (self._y, self._x)

    @property
    def center_position(self) -> Tuple[int, int]:
        return (self._h//2, self._w//2)

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

    def update_max_size(self) -> None:
        """Update the maximum size (height, width) of the screen."""
        self._max_h, self._max_w = self._window.getmaxyx()

    def addstr(self, *args, raise_on_curses_error=True):
        try:
            self.window.addstr(*args)
        except curses.error as e:
            # Writing outside the window, subwindow, or pad raises curses.error.
            if raise_on_curses_error:
                raise e
            else:
                # It may be desirable to ignore the error rather than crash.
                pass
    
    def refresh(self, defer=False) -> None:
        """Refresh the window and update the current refresh time.
        
        Args:
            defer (bool): If you have to update multiple windows, you can speed performance and perhaps reduce screen flicker by marking the window for refresh but deferring the window update.
        """
        self._window.noutrefresh()

        if not defer:
            curses.doupdate()
            self._update_refresh_time()

            if self.should_box:
                self._window.box()

    def resize(self, height: int, width: int, defer_refresh=False) -> None:
        """Resize the window to the specified height and width."""
        self._h = height
        self._w = width

        self.clear()
        self._window.resize(self._h, self._w)
        self.refresh(defer=defer_refresh)
    
    def resize_max_height(self, defer_refresh=False) -> None:
        """Resize the window to the maximum height of the screen."""
        self.update_max_size()
        self.resize(self._max_h, self._w, defer_refresh)
    
    def resize_max_width(self, defer_refresh=False) -> None:
        """Resize the window to the maximum width of the screen."""
        self.update_max_size()
        self.resize(self._h, self._max_w, defer_refresh)
    
    def resize_max_size(self, defer_refresh=False) -> None:
        """Resize the window to the maximum size of the screen."""
        self.update_max_size()
        self.resize(self._max_h, self._max_w, defer_refresh)

    def move(self, y: int, x: int, defer_refresh=False) -> None:
        """Move the window to the specified position."""
        self._y = y
        self._x = x
        self._window.move(y, x)
        self.refresh(defer=defer_refresh)
    
    def clear(self) -> None:
        """Clear the contents of the window."""
        self._window.clear()
    
    def erase(self) -> None:
        """Erase the contents of the window."""
        self._window.erase()