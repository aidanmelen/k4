from curses_wrapper.color import CursesColor, CursesColorPair
from .window import MenuWindow, CommandWindow, ContentWindow
from .color import curses_color, curses_color_pair

import curses

class Screen:
    def __init__(self, stdscr):
        if stdscr:
            self.stdscr = stdscr
        else:
            self.stdscr = curses.initscr()

        # Start colors and init color pairs
        # NOTE: requires curses.initscr()
        curses_color.start_color()
        curses_color.init_colors()
        curses_color_pair.init_pairs(bg_color_name = "BLACK")

        self.stdscr.bkgd(curses_color_pair["WHITE_ON_BLACK"])
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.menu_window = MenuWindow(6, curses.COLS, 0, 0)
        self.command_window = CommandWindow(3, curses.COLS, 6, 0)
        self.content_window = ContentWindow(curses.LINES - (6 + 3), curses.COLS, 6 + 3, 0)

        self.stdscr.refresh()
        self.content_window._window.refresh()

        self.focus = "topics"

        # TODO get dynamically
        self.contents = [
            "TOPIC                              PARTITION",
            "_schemas_schemaregistry_confluent  1        ",
            "confluent.connect-configs          1        ",
            "confluent.connect-offsets          25       ",
            "confluent.connect-status           5        "
        ]

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


def main(stdscr) -> None:
    try:
        screen = Screen(stdscr)

        while True:
            screen.render()
            ch = screen.stdscr.getch()
            command = screen.command_window.handle_input(ch)

            if command in ["topics", "tops", "t"]:
                screen.focus = "topics"

                # TODO get dynamically
                screen.contents = [
                    "TOPIC                              PARTITION",
                    "_schemas_schemaregistry_confluent  1        ",
                    "confluent.connect-configs          1        ",
                    "confluent.connect-offsets          25       ",
                    "confluent.connect-status           5        "
                ]

            screen.menu_window.handle_input(ch)
            screen.content_window.handle_input(ch)

            if ch == curses.KEY_RESIZE:
                screen.resize()

            elif ch == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()