from cli.curses_color import CursesColor, CursesColorPair
import curses

def main(screen):
    # Start colors and init color pairs
    curses_color = CursesColor()
    curses_color.start_color()
    curses_color.init_colors()

    curses_color_pair = CursesColorPair(curses_color)
    curses_color_pair.init_color_pairs(bg_color_name="WHITE")

    # Turn off echoing and enable cbreak mode
    curses.noecho()
    curses.cbreak()

    # Enable keypad mode
    screen.keypad(True)

    # Clear the screen
    screen.clear()

    # screen.addstr(str(curses_color.color_name_to_number))
    # screen.addstr(str(curses_color_pair.color_name_to_number))

    # Display all color pairs
    for color_pair_name, _ in curses_color_pair:
        screen.addstr(color_pair_name, curses_color_pair[color_pair_name] | curses.A_BOLD)
    else:
        screen.addstr("\n\n")

    # Display specific color pairs
    # screen.addstr("RED_ON_BLACK", curses_color_pair["RED_ON_BLACK"])
    # screen.addstr("GREEN_ON_BLACK", curses_color_pair["GREEN_ON_BLACK"])
    # screen.addstr("BLUE_ON_BLACK", curses_color_pair["BLUE_ON_BLACK"])
    # screen.addstr("\n\n")

    # Display custom color pairs by name
    # curses_color_pair.init_color_pair_by_name("WHITE", "TURQUOISE")
    # curses_color_pair.init_color_pair_by_name("BLACK", "GOLD")
    # curses_color_pair.init_color_pair_by_name("NAVY", "WHITE")
    # screen.addstr("WHITE_ON_TURQUOISE", curses_color_pair["WHITE_ON_TURQUOISE"])
    # screen.addstr("BLACK_ON_GOLD", curses_color_pair["BLACK_ON_GOLD"])
    # screen.addstr("NAVY_ON_WHITE", curses_color_pair["NAVY_ON_WHITE"] | curses.A_BOLD)
    # screen.addstr("\n\n")

    # Display custom color pairs by number
    # curses_color_pair.init_color_pair_by_number(curses_color["TURQUOISE"], curses_color["WHITE"])
    # curses_color_pair.init_color_pair_by_number(curses_color["GOLD"], curses_color["WHITE"])
    # curses_color_pair.init_color_pair_by_number(curses_color["BROWN"], curses_color["WHITE"])
    # screen.addstr("TURQUOISE_ON_WHITE", curses_color_pair["WHITE_ON_TURQUOISE"])
    # screen.addstr("GOLD_ON_WHITE", curses_color_pair["GOLD_ON_WHITE"])
    # screen.addstr("BROWN_ON_WHITE", curses_color_pair["BROWN_ON_WHITE"] | curses.A_BOLD)

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