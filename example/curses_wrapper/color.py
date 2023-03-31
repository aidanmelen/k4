from curses_wrapper.color import CursesColor
from curses_wrapper.color_pair import CursesColorPair
import curses

def main(screen):
    # Start colors and init color pairs
    curses_color = CursesColor()
    curses_color.start_color()
    curses_color.init_colors()

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_pairs()
    curses_color_pair.init_pairs(bg_color_name="BLACK")
    curses_color_pair.init_pairs(bg_color_name="WHITE")

    # Turn off echoing and enable cbreak mode
    curses.noecho()
    curses.cbreak()

    # Enable keypad mode
    screen.keypad(True)

    # Clear the screen
    screen.clear()

    # Display all color pairs
    for color_pair_name, color_pair_number in curses_color_pair:
        screen.addstr(f"█ {color_pair_name} █", curses_color_pair.get(color_pair_name))
    else:
        screen.addstr("\n\n")
    
    # Refresh the screen
    screen.refresh()

    # Wait for user input
    screen.getch()

    # Restore terminal settings
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass