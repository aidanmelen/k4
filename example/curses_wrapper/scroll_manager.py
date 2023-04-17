from curses_wrapper import ScrollManager
from curses_wrapper.color import CursesColor, CursesColorPair
import curses

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # start colors
    curses_color = CursesColor()
    curses_color.start_color()
    curses_color.init_colors()

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs()
    curses_color_pair.init_pairs(bg_color_name="BLACK")
    stdscr.bkgd(curses_color_pair["WHITE_ON_BLACK"])

    max_y, max_x = stdscr.getmaxyx()

    # Create top sub-window
    h = max_y // 2 - 1
    w = max_x
    y = 0
    x = 0
    top_win = stdscr.subwin(h, w, y, x)
    top_win.bkgd(curses_color_pair["WHITE_ON_BLACK"])
    
    # Create bottom sub-window
    h = max_y // 2 - 1
    w = max_x
    y = max_y // 2
    x = 0
    bottom_win = stdscr.subwin(h, w, y, x)
    bottom_win.box()
    bottom_win.bkgd(curses_color_pair["SKY_ON_BLACK"])

    # Create bottom derived-window
    scroll_manager = ScrollManager()
    scroll_win = bottom_win.derwin(h - 2 , w - 3, 1, 2)
    scroll_win.bkgd(curses_color_pair["SKY_ON_BLACK"])
    scroll_manager.init(scroll_win)

    stdscr.refresh()

    # Generate colorized scroll items
    items = []
    for num in range(100):
        if num == 0:
            items.append({'text': f'{num + 1}. Header', 'color_pair_id': curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD})
        elif num == 10:
            items.append({'text': f'{num + 1}. Error', 'color_pair_id': curses_color_pair["RED_ON_BLACK"] | curses.A_BOLD})
        else:
            items.append({'text': f'{num + 1}. Item'})

    # Set scroll items
    scroll_manager.items = items

    while True:
        # Display colorized scroll items
        scroll_manager.display()

        # Select the current item
        top_win.erase()
        current_text = scroll_manager.select_text()
        top_win.addstr(4, max_x // 2 - len(current_text) // 2 , current_text, curses.A_BOLD)
        top_win.refresh()

        ch = stdscr.getch()

        # Handle scrolling
        scroll_manager.handle_input(ch)

        if ch == ord("q"):
            break


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass