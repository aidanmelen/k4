from cli.curses_color import CursesColor, CursesColorPair
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
    curses_color_pair.init_pairs(bg_color_name="GOLD")
    # curses_color_pair.init_pair("RED", bg_color_name="BLACK")

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

    # Display specific color pairs
    # screen.addstr("RED_ON_BLACK", curses_color_pair["RED_ON_BLACK"])
    # screen.addstr("GREEN_ON_BLACK", curses_color_pair["GREEN_ON_BLACK"])
    # screen.addstr("BLUE_ON_BLACK", curses_color_pair["BLUE_ON_BLACK"])
    # screen.addstr("\n\n")

    # Display custom color pairs by number
    # curses_color_pair.init_pair("BLACK")
    # curses_color_pair.init_pair("WHITE")
    # curses_color_pair.init_pair("WHITE", "BLACK")

    # curses_color_pair.init_pair("GOLD", "WHITE")
    # curses_color_pair.init_pair("BROWN", "WHITE")
    # screen.addstr("TURQUOISE_ON_WHITE", curses_color_pair["TURQUOISE_ON_WHITE"])
    # screen.addstr("GOLD_ON_WHITE", curses_color_pair["GOLD_ON_WHITE"])
    # screen.addstr("BROWN_ON_WHITE", curses_color_pair["BROWN_ON_WHITE"] | curses.A_BOLD)
    # screen.addstr("\n\n")
    
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