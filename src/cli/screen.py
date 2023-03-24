from .window import MenuWindow, CommandWindow, ContentWindow
import curses

class Screen:
    def __init__(self):
        self.stdscr = curses.initscr()

        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        
        self.menu_window = MenuWindow(6, curses.COLS, 0, 0)
        self.command_window = CommandWindow(3, curses.COLS, 6, 0)
        self.content_window = ContentWindow(curses.LINES-(6+3), curses.COLS, 6+3, 0)

        self.stdscr.refresh()
        self.content_window.window.refresh()

        self._focus = None
        self._contents = []

    @property
    def focus(self):
        return self._focus
    
    @property
    def contents(self):
        return self._contents

    @focus.setter
    def focus(self, value):
        self._focus = value
    
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

        if self._focus and self._contents:
            self.content_window.render(self._focus, self._contents)