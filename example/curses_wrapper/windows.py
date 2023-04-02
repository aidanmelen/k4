from curses_wrapper.color import CursesColor
from curses_wrapper.color_pair import CursesColorPair
from curses_wrapper.window import CursesWindow

import curses

try:
    # Initialize screen
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)

    # Initialize colors
    curses_color = CursesColor()
    curses_color.start_color()
    curses_color.init_colors()

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs()
    curses_color_pair.init_pairs(bg_color_name="BLACK")
    
    # Initialize windows
    curses_window = CursesWindow(curses.LINES, curses.COLS, 0, 0, box=True)
    curses_window.window.bkgd(curses_color_pair.get("TURQUOISE_ON_BLACK"))

    # Refresh screen after creating new windows
    stdscr.refresh()

    # Run screen
    while True:
        
        # Add content
        curses_window.addstr(1, 1, f"         position: ({curses_window._y}, {curses_window._x})")
        curses_window.addstr(2, 1, f"             size: ({curses_window._h}, {curses_window._w})")
        curses_window.addstr(3, 1, f"         max size: ({curses_window._max_h}, {curses_window._max_w})")
        curses_window.addstr(4, 1, f"last refresh time: {curses_window.last_refresh_time}")
        
        # Refresh window
        curses_window.refresh()

        # Get input ascii character
        ch = stdscr.getch()

        # Handle resize event
        if ch == curses.KEY_RESIZE:
            curses_window.resize_max_size(defer_refresh=True)
        
        elif ch == ord('q'):
            break


except KeyboardInterrupt:
    pass
finally:
    curses.endwin()