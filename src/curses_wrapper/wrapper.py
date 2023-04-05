from .window import CursesWindow

import curses

def wrapper(func) -> None:
    try:
        stdscr = curses.initscr()
        window = CursesWindow(window = stdscr)
        func(window)
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()