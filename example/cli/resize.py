import curses

def main(stdscr):
    curses.curs_set(0) # hide cursor
    stdscr.clear() # clear the screen

    # create the two windows
    top_win = curses.newwin(curses.LINES // 2, curses.COLS, 0, 0)
    bottom_win = curses.newwin(curses.LINES // 2, curses.COLS, curses.LINES // 2, 0)

    # draw some content in each window
    top_win.addstr(0, 0, "This is the top window")
    bottom_win.addstr(0, 0, "This is the bottom window")

    stdscr.refresh() # draw the windows

    while True:
        # get the current screen size
        height, width = stdscr.getmaxyx()

        if height < 4 or width < 1:
            # if the screen is too small to display both windows, clear the screen
            stdscr.clear()
            stdscr.addstr(0, 0, f"Screen too small! ({height}, {width})")
            stdscr.refresh()
        else:
            # if the screen is large enough, redraw the windows
            if not (top_win.getmaxyx() == (height // 2, width)):
                top_win = curses.newwin(height // 2, width, 0, 0)
                top_win.addstr(0, 0, f"This is the top window ({height}, {width})")
            if not (bottom_win.getmaxyx() == (height // 2, width)):
                bottom_win = curses.newwin(height // 2, width, height // 2, 0)
                bottom_win.addstr(0, 0, f"This is the bottom window ({height}, {width})")
            top_win.refresh()
            bottom_win.refresh()

        # wait for a key press
        ch = stdscr.getch()

        if ch == ord('q'):
            break

curses.wrapper(main)