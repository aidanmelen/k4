from curses_wrapper.color import CursesColor, CursesColorPair
import curses
import random

def main(stdscr):
    # Start colors and init color pairs
    curses_color = CursesColor()
    curses_color.start_color()
    random_color_names = random.sample(list(curses_color.color_name_to_rgb.keys()), 200)
    curses_color.init_colors(color_names=random_color_names)

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs()
    # curses_color_pair.init_pairs(bg_color_name="BLACK")
    # curses_color_pair.init_pairs(bg_color_name="WHITE")

    # Turn off echoing and enable cbreak mode
    curses.noecho()
    curses.cbreak()

    # Enable keypad mode
    stdscr.keypad(True)

    # Clear the stdscr
    stdscr.clear()

    # Display all color pairs
    try:
        for color_pair_name, color_pair_number in curses_color_pair:
            stdscr.addstr(f"█ {color_pair_name} █", curses_color_pair.get(color_pair_name) | curses.A_BOLD)
        else:
            stdscr.addstr("\n\n")
    except curses.error as e:
        pass
    
    # Refresh the stdscr
    stdscr.refresh()

    # Wait for user input
    stdscr.getch()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass