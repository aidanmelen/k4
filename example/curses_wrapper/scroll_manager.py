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
    curses_color.init_colors(color_names=["WHITE", "RED", "LIGHT_SKY_BLUE", "ORANGE", "MEDIUM_PURPLE", "BLACK"])

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs()
    curses_color_pair.init_pairs(bg_color_name="BLACK")
    stdscr.bkgd(curses_color_pair["WHITE_ON_BLACK"])

    max_y, max_x = stdscr.getmaxyx()

    # Create top sub-window
    h = max_y // 3 - 1
    w = max_x
    y = 0
    x = 0
    top_win = stdscr.subwin(h, w, y, x)
    top_win.bkgd(curses_color_pair["WHITE_ON_BLACK"])
    
    # Create bottom sub-window
    h = (max_y // 3) * 2 - 1
    w = max_x
    y = max_y // 3
    x = 0
    bottom_win = stdscr.subwin(h, w, y, x)
    bottom_win.box()
    bottom_win.bkgd(curses_color_pair["LIGHT_SKY_BLUE_ON_BLACK"])

    # Create bottom derived-window
    scroll_manager = ScrollManager()
    scroll_win = bottom_win.derwin(h - 2 , w - 4, 1, 2)
    scroll_manager.init(scroll_win, curses_color_pair["LIGHT_SKY_BLUE_ON_BLACK"], cursor_start_position=1, has_fixed_header_line=True)

    stdscr.refresh()

    # Generate colorized scroll items
    items = []
    for num in range(100):
        if num == 0:
            items.append({'line': f'{num + 1}. Header', 'color_pair_id': curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD})
        elif num == 5:
            items.append({'line': f'{num + 1}. Creating', 'color_pair_id': curses_color_pair["ORANGE_ON_BLACK"] | curses.A_BOLD})
        elif num == 10:
            items.append({'line': f'{num + 1}. Error', 'color_pair_id': curses_color_pair["RED_ON_BLACK"] | curses.A_BOLD})
        elif num == 15:
            items.append({'line': f'{num + 1}. Deleting', 'color_pair_id': curses_color_pair["MEDIUM_PURPLE_ON_BLACK"] | curses.A_BOLD})
        else:
            items.append({'line': f'{num + 1}. Item'})

    # Set scroll items
    scroll_manager.items = items

    ch  = -1
    while True:
        # Display colorized scroll items
        scroll_manager.display()

        # Select the current item
        top_win.erase()
        current_line = scroll_manager.select_item_line()
        current_line_color_pair_id = scroll_manager.select_item_color_pair_id()
        top_win.addstr(4, max_x // 2 - len(current_line) // 2 , current_line, current_line_color_pair_id | curses.A_BOLD)
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