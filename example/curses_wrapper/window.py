from curses_wrapper.color import CursesColor, CursesColorPair
from curses_wrapper.window import CursesWindow, CursesWindowText

import curses


try:
    # Initialize screen
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.set_escdelay(1)
    stdscr.keypad(True)

    # Initialize colors
    curses_color = CursesColor()
    curses_color.start_color()
    curses_color.init_colors()

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs()
    curses_color_pair.init_pairs(bg_color_name="BLACK")
    curses_color_pair.init_pairs(bg_color_name="WHITE")
    curses_color_pair.init_pairs(bg_color_name="SKY")
    curses_color_pair.init_pairs(bg_color_name="GRAY")
    
    # Initialize windows
    window = CursesWindow(curses.LINES, curses.COLS, 0, 0, has_box=False)
    window_text = CursesWindowText(window)

    # Arbitrary window modifications
    window.window.bkgd(curses_color_pair.get("GOLD_ON_BLACK"))

    # Set ignore _curse.error when calling addstr or addnstr
    window.addstr_ignore_curses_error = True

    # Refresh screen after creating new windows
    stdscr.refresh()

    # Run screen
    while True:
        
        # Paint text
        window.addstr(0, 0, f"position: ({window.y}, {window.x})", curses_color_pair.get("CYAN_ON_BLACK"))
        window.addstr(1, 0, f"win size: ({window.lines}, {window.cols})", curses_color_pair.get("CYAN_ON_BLACK"))
        window.addstr(2, 0, f"max size: ({curses.LINES}, {curses.COLS})", curses_color_pair.get("CYAN_ON_BLACK"))
        
        # Normally we would only refresh after all content changes. However, this will display the real-time refresh times.
        window.refresh()
        window.addstr(3, 0, f"refresh time: {window.refresh_time}", curses_color_pair.get("CYAN_ON_BLACK"))
        window.addstr(4, 0, f"refresh elapsed time: {window.refresh_elapsed_time}", curses_color_pair.get("CYAN_ON_BLACK"))

        # Window text
        long_text = ", ".join(["very long text"] * 10)

        # Add shortened window text
        shortened_text = window_text.shorten(", ".join(["shorten"] * 10))
        window.addstr(7, 0, shortened_text, curses_color_pair.get("BLACK_ON_WHITE"))

        # Add window text with addnstr
        window.addnstr(11, 0, long_text, window.cols, curses_color_pair.get("BLACK_ON_WHITE"))

        # Add shortened/aligned window text
        align_left_shortened_text = window_text.align_left(
            window_text.shorten(
                ", ".join(["align left and shorten"] * 10)
            )
        )
        window.addstr(9, 0, align_left_shortened_text, curses_color_pair.get("BLACK_ON_WHITE"))

        # Add text with default cursor wrapping
        window.addstr(13, 0, long_text, curses_color_pair.get("BLACK_ON_SKY"))

        # Add window wrapped/aligned text
        wrapped_lines = window_text.wrap(", ".join(["align left and wrap"] * 10))
        align_left_wrapped_text = ''.join([window_text.align_left(line) for line in wrapped_lines])
        window.addstr(16, 0, align_left_wrapped_text, curses_color_pair.get("BLACK_ON_SKY"))

        # Add text with default cursor wrapping, but with wrap + max_lines to ensure lines are written on screen
        y = 20
        wrapped_longer_text = ''.join(window_text.wrap(", ".join(["wrap with max lines"] * 100), max_lines=window.lines-1-y, placeholder=''))
        window.addstr(y, 0, window_text.align_right(wrapped_longer_text), curses_color_pair.get("WHITE_ON_GRAY"))

        # Add text in the center of the screen.
        center_lines, center_cols = window.center_position
        center_msg = f"center: ({center_lines}, {center_cols})"
        window.addstr(center_lines, center_cols - len(center_msg) // 2, center_msg, curses_color_pair.get("MAGENTA_ON_BLACK"))
        
        # Add text to last window line. Ignore curses.error when writing text outside.
        window.addstr(window.lines - 1, 0, "This is the last line.", curses_color_pair.get("MAGENTA_ON_BLACK"))

        # Refresh window
        window.refresh() # refresh before gathering user input

        # Get input ascii character
        ch = stdscr.getch()

        # Handle resize event
        if ch == curses.KEY_RESIZE:
            stdscr.refresh()
            window.resize_max(should_refresh=True)
        
        elif ch == ord('q'):
            break
        
        elif ch == 27:
            break

except KeyboardInterrupt:
    pass
finally:
    curses.endwin()