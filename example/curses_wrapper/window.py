from curses_wrapper import wrapper
from curses_wrapper.color import CursesColor, CursesColorPair
from curses_wrapper.window import CursesWindow, CursesWindowText

import curses

def draw(window):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.set_escdelay(1)

    # Allow window to be resized to minimum size.
    # Normally writing outside the window, subwindow, or pad raises curses.error.
    window.addstr_ignore_curses_error = True

    # Create window text helper
    window_text = CursesWindowText(window)

    # Start 10-bit colors in curses
    curses_color = CursesColor()
    curses_color.start_color()
    curses_color.init_colors()

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs(bg_color_name="BLACK")
    curses_color_pair.init_pair("AZURE", "WHITE")
    curses_color_pair.init_pair("GOLD", "BLACK")
    curses_color_pair.init_pair("BLACK", "SKY")
    curses_color_pair.init_pair("BLACK", "WHITE")

    # Set window background color
    window.bkgd(curses_color_pair["WHITE_ON_BLACK"])

    subwindow = CursesWindow(window=window.derwin(5, 10, 3, 5), has_box=True)

    ch = 0

    while (ch != ord('q')):

        # Declaration of strings
        title = window_text.align_center("Curses example")
        subtitle = window_text.align_center("Written by Aidan Melen")
        space_line = " " * window.cols
        align_left = "align left"
        align_center = "align center"
        align_right = "align right"
        shortened_text = window_text.shorten(", ".join(["shortened with window_text"] * 10))
        wrapped_text = "".join(window_text.wrap(", ".join(["wrapped with window_text"] * 10)))
        status_bar = window_text.align_center(f"Press 'q' to exit | STATUS BAR | Size: {window.lines}, {window.cols}")
        
        center_y, center_x = window.center_position

        # Rendering some text
        window.attron(curses_color_pair["AZURE_ON_WHITE"] | curses.A_BOLD)
        window.addstr(0, 0, space_line)
        window.addstr(0, 0, align_left)
        window.addstr(0, window.cols // 2 - len(align_center) // 2, align_center)
        window.addstr(0, window.cols - len(align_right), align_right)
        window.attroff(curses_color_pair["AZURE_ON_WHITE"] | curses.A_BOLD)

        
        # Render shortened text
        window.attron(curses_color_pair["WHITE_ON_BLACK"])
        window.addnstr(center_y + 1, 0, ", ".join(["shortened with addnstr()"] * 10), window.cols)
        window.addstr(center_y + 2, 0, shortened_text)

        # Render wrapped text
        window.addstr(center_y + 4, 0, ", ".join(["wrapped with addstr()"] * 10))
        window.addstr(center_y + 8, 0, wrapped_text)
        window.attroff(curses_color_pair["WHITE_ON_BLACK"])

        # Rendering title
        top_quarter_y = center_y - center_y // 2
        window.addstr(top_quarter_y, 0, title, curses_color_pair["GOLD_ON_BLACK"] | curses.A_BOLD)
        window.addstr(top_quarter_y + 1, 0, subtitle, curses_color_pair["WHITE_ON_BLACK"])

        # Render status bar
        window.addstr(window.lines - 1, 0, status_bar, curses_color_pair["BLACK_ON_SKY"])

        # Refresh the screen
        subwindow.refresh()
        window.refresh()

        # Wait for next input
        ch = window.getch()

        # Handle resize
        if ch == curses.KEY_RESIZE:
            window.resize_max(should_refresh=True)

            parent_y, parent_x = subwindow.getparyx()
            subwindow.resize(max(5, parent_y), max(parent_x, 10), should_refresh=True)

def main():
    wrapper(draw)

if __name__ == "__main__":
    main()