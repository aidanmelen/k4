from cli.curses_color import CursesColor
import curses

# import curses.textpad
import time


class CursesWindow:
    PAD = 1

    def __init__(self, h, w, y, x):
        self._window = curses.newwin(h, w, y, x)
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self._max_h = curses.LINES
        self._max_w = curses.COLS
        self._last_refresh_time = 0
        self._refresh_elapsed_time = 0

    @property
    def window(self):
        return self._window

    @property
    def size(self):
        return (self._y, self._x)

    @property
    def position(self):
        return (self._y, self._x)

    @property
    def last_refresh_time(self):
        return self._last_refresh_time

    def start_color(self):
        self.color = CursesColor()
        self.color.start_color()

    def update_refresh_time(self):
        current_time = time.perf_counter()
        self._refresh_elapsed_time = current_time - self._last_refresh_time
        self._last_refresh_time = current_time

    def refresh(self):
        self._window.refresh()
        self.update_refresh_time()

    def erase(self):
        self._window.erase()

    def resize(self, max_h=None, max_w=None):
        curses.update_lines_cols()

        self._max_h = max_h if max_h else curses.LINES
        self._max_w = max_w if max_w else curses.COLS

        self.erase()
        self._window.resize(self._h, self._max_w)
        self.refresh()


class MenuWindow(CursesWindow):
    LOGO = [
        " __      _____  ",
        "|  | __ /  |  | ",
        "|  |/ //   |  |_",
        "|    </    ^   /",
        "|__|_ \\____   |",
        "     \\/    |__|",
    ]

    def __init__(self, h, w, y, x):
        """
        A curses menu window wrapper class. For example:
        """
        super().__init__(h, w, y, x)

    def render(self):
        super().render()
        self._window.addstr(0, 0, "Context: None", curses.color_pair(10))
        self._window.addstr(1, 0, "<?> Help", curses.color_pair(10))
        self._window.addstr(2, 0, "<:> navigate", curses.color_pair(10))
        self._window.addstr(3, 0, "<s> search", curses.color_pair(10))
        self._window.addstr(4, 0, "<i> Internal", curses.color_pair(10))

        # Display k4 logo and align in top/right
        x = self.max_w - len(self.LOGO[0]) - self.PAD
        for y, line in enumerate(self.LOGO):
            if x >= 0:
                self._window.addstr(y, x, line)

        self._window.refresh()

    def handle_input(self, ch):
        pass

    def erase(self):
        super().erase()
