from .window import MenuWindow, CommandWindow, ContentWindow
import curses


class CursesScreen:
    def __init__(self, stdscr=None):
        """
        The k4 screen class with 3 standard windows: menu, command, content

        Context: None                     __      _____
        <?> Help                         |  | __ /  |  |
        <:> navigate                     |  |/ //   |  |_ <- menu window
        <s> search                       |    </    ^   /
        <i> Internal                     |__|_ \____   |
                                              \/    |__|
        ┌────────────────────────────────────────────────┐
        │ > textpad                                      │<- command window
        └────────────────────────────────────────────────┘
        ┌─────────────────── Topics[4] ──────────────────┐
        │ TOPIC                              PARTITION   │
        │ _schemas                           1           │
        │ connect-configs                    1         <---- scroll window
        │ connect-offsets                    25          │
        │ connect-status                     5           │<- content window
        │                                                │
        └────────────────────────────────────────────────┘
        """
        if stdscr:
            self.stdscr = stdscr
        else:
            self.stdscr = curses.initscr()

        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.menu_window = MenuWindow(6, curses.COLS, 0, 0)
        self.command_window = CommandWindow(3, curses.COLS, 6, 0)
        self.content_window = ContentWindow(curses.LINES - (6 + 3), curses.COLS, 6 + 3, 0)

        self.stdscr.refresh()
        self.content_window.window.border()
        self.content_window.window.refresh()

        self._banner = None
        self._contents = []

    @property
    def banner(self):
        return self._banner

    @property
    def contents(self):
        return self._contents

    @banner.setter
    def banner(self, value):
        self._banner = value

    @contents.setter
    def contents(self, value):
        self._contents = value

    def resize(self):
        self.stdscr.erase()
        self.stdscr.refresh()
        self.menu_window.resize()
        self.command_window.resize()
        self.content_window.resize()

    def render(self):
        self.menu_window.render()
        self.command_window.render()

        if self._banner and self._contents:
            self.content_window.render(self._banner, self._contents)

    def erase(self):
        self.stdscr.erase()
        self.menu_window.erase()
        self.command_window.erase()
        self.content_window.erase()


class TopicScreen(CursesScreen):
    def __init__(self):
        """
        The k4 topic screen class.
        """
        super().__init__()
