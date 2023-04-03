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
    curses_window = CursesWindow(curses.LINES, curses.COLS, 0, 0, should_box=True)
    curses_window.window.bkgd(curses_color_pair.get("GOLD_ON_BLACK"))

    # Refresh screen after creating new windows
    stdscr.refresh()

    # Run screen
    while True:
        
        # Add content
        curses_window.addstr(1, 1, f"position: ({curses_window._y}, {curses_window._x})", curses_color_pair.get("CYAN_ON_BLACK"))
        curses_window.addstr(2, 1, f"win size: ({curses_window._h}, {curses_window._w})", curses_color_pair.get("CYAN_ON_BLACK"))
        curses_window.addstr(3, 1, f"max size: ({curses_window._max_h}, {curses_window._max_w})", curses_color_pair.get("CYAN_ON_BLACK"))
        
        # normally we would refresh after all content changes.
        curses_window.refresh()
        curses_window.addstr(5, 1, f"refresh time: {curses_window.refresh_time}", curses_color_pair.get("CYAN_ON_BLACK"))
        curses_window.addstr(6, 1, f"refresh elapsed time: {curses_window.refresh_elapsed_time}", curses_color_pair.get("CYAN_ON_BLACK"))

        center_height, center_width = curses_window.center_position
        center_msg = f"center: ({center_height}, {center_width})"
        curses_window.addstr(center_height, center_width - len(center_msg) // 2, center_msg)
        
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