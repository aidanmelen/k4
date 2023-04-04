from curses_wrapper.color import CursesColor, CursesColorPair
from curses_wrapper.window import CursesWindow, CursesWindowText

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
    curses_color_pair.init_pairs(bg_color_name="WHITE")
    curses_color_pair.init_pairs(bg_color_name="SKY")
    curses_color_pair.init_pairs(bg_color_name="GRAY")
    
    # Initialize windows
    window = CursesWindow(curses.LINES, curses.COLS, 0, 0, has_box=False)
    window_text = CursesWindowText(window)

    # Arbitrary window modifications
    window.window.bkgd(curses_color_pair.get("GOLD_ON_BLACK"))

    # Refresh screen after creating new windows
    stdscr.refresh()

    # Run screen
    while True:
        
        # Paint text
        window.addstr(0, 0, f"position: ({window.y}, {window.x})", curses_color_pair.get("CYAN_ON_BLACK"), ignore_curses_error=True)
        window.addstr(1, 0, f"win size: ({window.lines}, {window.cols})", curses_color_pair.get("CYAN_ON_BLACK"), ignore_curses_error=True)
        window.addstr(2, 0, f"max size: ({curses.LINES}, {curses.COLS})", curses_color_pair.get("CYAN_ON_BLACK"), ignore_curses_error=True)
        
        # Normally we would only refresh after all content changes. However, this will display the real-time refresh times.
        window.refresh()
        window.addstr(3, 0, f"refresh time: {window.refresh_time}", curses_color_pair.get("CYAN_ON_BLACK"), ignore_curses_error=True)
        window.addstr(4, 0, f"refresh elapsed time: {window.refresh_elapsed_time}", curses_color_pair.get("CYAN_ON_BLACK"), ignore_curses_error=True)

        # Window text
        long_text = ", ".join(["very long text"] * 10)

        # Add window text with addnstr
        window.addnstr(11, 0, long_text, window.cols, curses_color_pair.get("BLACK_ON_WHITE"), ignore_curses_error=True)

        # Add shortened window text
        shortened_text = window_text.shorten(long_text)
        window.addstr(7, 0, shortened_text, curses_color_pair.get("BLACK_ON_WHITE"), ignore_curses_error=True)

        # Add shortened/aligned window text
        align_left_shortened_text = window_text.align_left(shortened_text)
        window.addstr(9, 0, align_left_shortened_text, curses_color_pair.get("BLACK_ON_WHITE"), ignore_curses_error=True)

        # Add text with default cursor wrapping
        window.addstr(13, 0, long_text, curses_color_pair.get("BLACK_ON_SKY"), ignore_curses_error=True)

        # Add window wrapped/aligned text
        wrapped_lines = window_text.wrap(long_text)
        align_left_wrapped_text = ''.join([window_text.align_left(line) for line in wrapped_lines])
        window.addstr(16, 0, align_left_wrapped_text, curses_color_pair.get("BLACK_ON_SKY"), ignore_curses_error=True)

        # Add text with default cursor wrapping, but with max_lines
        y = 20
        longer_text = ", ".join(["longer text"] * 100)
        wrapped_longer_text = window_text.fill(longer_text, max_lines=window.lines-y, placeholder='')
        window.addstr(y, 0, wrapped_longer_text, curses_color_pair.get("BLACK_ON_GRAY"), ignore_curses_error=True)

        # Add text in the center of the screen.
        center_lines, center_cols = window.center_position
        center_msg = f"center: ({center_lines}, {center_cols})"
        window.addstr(center_lines, center_cols - len(center_msg) // 2, center_msg, curses_color_pair.get("MAGENTA_ON_BLACK"), ignore_curses_error=True)
        
        # Add text to last window line. Ignore curses.error when writing text outside.
        window.addstr(window.lines - 1, 0, "This is the last line.", curses_color_pair.get("MAGENTA_ON_BLACK"), ignore_curses_error=True)

        # Refresh window
        window.refresh() # refresh before gathering user input

        # Get input ascii character
        ch = stdscr.getch()

        # Handle resize event
        if ch == curses.KEY_RESIZE:
            stdscr.refresh()
            window.resize_max()
        
        elif ch == ord('q'):
            break

except KeyboardInterrupt:
    pass
finally:
    curses.endwin()