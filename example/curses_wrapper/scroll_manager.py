from curses_wrapper import ScrollManager
import curses

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    max_y, max_x = stdscr.getmaxyx()
    
    # Create outer box sub-window
    h = max_y - 1
    w = max_x
    y = 0
    x = 0
    box_win = stdscr.subwin(h, w, y, x)
    box_win.box()
    stdscr.refresh()

    # Create inner scroll derived-window
    scroll_manager = ScrollManager()
    scroll_win = box_win.derwin(h - 2 , w - 4, 1, 2)
    scroll_manager.init(scroll_win)

    items = [f'{num + 1}. Item' for num in range(1000)]

    while True:
        scroll_manager.display(items)

        ch = stdscr.getch()

        scroll_manager.handle_input(ch)

        if ch == ord("q"):
            break


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass