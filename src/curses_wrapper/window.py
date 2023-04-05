from typing import Tuple, List, Dict, Callable, Any, Optional
import textwrap
import curses


class CursesWindow:
    """A wrapper around the curses window functionality.

    This class provides additional functionality and customization options for `curses.window` functions,
    while still allowing access to all of the underlying `curses.window` functionality.

    For more information on the `curses.window` object and its functions, see the Python documentation:
    https://docs.python.org/3/library/curses.html#window-objects
    """

    def __init__(
        self, lines: int = None, cols: int = None, y: int = 0, x: int = 0, window: curses.window = None, has_box: bool = False
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
        if not any([lines, cols, window]):
            raise ValueError("One of lines and cols or window must be provided.")
        
        if all([lines, cols]):
            self._lines = lines
            self._cols = cols
            self._y = y
            self._x = x
            self._window = curses.newwin(lines, cols, y, x)
        elif window:
            lines, cols = window.getmaxyx()
            y, x = window.getbegyx()
            self._lines = lines
            self._cols = cols
            self._y = y
            self._x = x
            self._window = window
        else:
            raise ValueError("One of lines and cols or window must be provided.")

        self.has_box = has_box
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
    def addstr_ignore_curses_error(self):
        return self._addstr_ignore_curses_error
    
    @addstr_ignore_curses_error.setter
    def addstr_ignore_curses_error(self, value):
        bool_value = value == True
        self._addstr_ignore_curses_error = bool_value

    def addstr(self, *args, ignore_curses_error: bool = False) -> None:
        """Paint the character string str at (y, x) with attributes attr, overwriting anything previously on the display."""
        try:
            self.window.addstr(*args)
        except curses.error as e:
            # Writing outside the window, subwindow, or pad raises curses.error.
            if any([self.addstr_ignore_curses_error, ignore_curses_error]):
                pass
            else:
                raise e

    def addnstr(self, *args, ignore_curses_error: bool = False) -> None:
        """Paint at most n characters of the character string str at (y, x) with attributes attr, overwriting anything previously on the display."""
        try:
            self.window.addnstr(*args)
        except curses.error as e:
            # Writing outside the window, subwindow, or pad raises curses.error.
            if any([self.addstr_ignore_curses_error, ignore_curses_error]):
                pass
            else:
                raise e

    def refresh(self) -> None:
        """Update the display immediately (sync actual screen with previous drawing/deleting methods)."""
        self._window.refresh()

        if self.has_box:
            self._window.box()

    def resize(self, lines: int, cols: int, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the specified lines and cols."""
        self._lines = lines
        self._cols = cols

        self._window.resize(self._lines, self._cols)
        
        if should_refresh:
            self.clear()
            self.refresh()

        if should_noutrefresh:
            self.clearok()
            self.noutrefresh()

    def resize_max_lines(self, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the maximum lines of the entire terminal screen."""
        curses.update_lines_cols()
        self._lines = curses.LINES - 1 - self.y
        self.resize(self._lines, self._cols, should_refresh, should_noutrefresh)

    def resize_max_cols(self, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the maximum columns of the entire terminal screen."""
        curses.update_lines_cols()
        self._cols = curses.COLS - 1 - self.x
        self.resize(self._lines, self._cols , should_refresh, should_noutrefresh)

    def resize_max(self, should_refresh=False, should_noutrefresh=False) -> None:
        """Resize the window to the maximum size (lines, columns) of the entire terminal screen."""
        curses.update_lines_cols()
        self._lines = curses.LINES - 1 - self.y
        self._cols = curses.COLS - 1 - self.x
        self.resize(self._lines, self._cols, should_refresh, should_noutrefresh)

    def __getattr__(self, attr: str) -> Callable[..., Any]:
        """
        Dynamically generates a method that calls the specified `curses.window` function.

        This method is called when a method is accessed on an instance of `MyCursesWindow`
        that does not exist on the class itself. If the method exists on the underlying
        `curses.window` object, a new method is dynamically generated that calls the
        underlying function with the same arguments.

        Args:
            attr (str): The name of the method being accessed.

        Returns:
            A dynamically generated method that calls the specified `curses.window` function.

        Raises:
            AttributeError: If the specified method does not exist on the underlying `curses.window` object.
        """
        # check if the attribute exists in curses.window
        if hasattr(self.window, attr):
            # if it does, dynamically generate a method that calls the curses.window function
            def wrapper(*args):
                return getattr(self.window, attr)(*args)
            return wrapper
        else:
            # if it doesn't, raise an AttributeError
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


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
    
    def align_left(self, text: str, width: Optional[int] = None) -> str:
        """Align left and pad the given text given width."""
        if not width:
            width = self.__window.cols
        return "{:<{}}".format(text, width)
    
    def align_right(self, text: str, width: Optional[int] = None) -> str:
        """Align right and pad the given text given width."""
        if not width:
            width = self.__window.cols
        return "{:>{}}".format(text, width)
    
    def align_center(self, text: str, width: Optional[int] = None) -> str:
        """Align center and pad the given text given width."""
        if not width:
            width = self.__window.cols
        return "{:^{}}".format(text, width)

    def shorten(self, text: str, width: Optional[int] = None, **kwargs: Dict[str, Any]) -> str:
        """Collapse and truncate the given text to fit in the given width."""
        if not width:
            width = self.__window.cols
        return textwrap.shorten(text, width, **kwargs)

    def wrap(self, text: str, width: Optional[int] = None, **kwargs: Dict[str, Any]) -> List[str]:
        """Wraps the single paragraph in text (a string) so every line is at most width characters long. Returns a list of output lines, without final newlines."""
        if not width:
            width = self.__window.cols
        return textwrap.wrap(text, width, **kwargs)
    
    def fill(self, text: str, width: Optional[int] = None, **kwargs: Dict[str, Any]) -> str:
        if not width:
            width = self.__window.cols
        return textwrap.fill(text, width, **kwargs)