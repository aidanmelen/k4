import curses
import os

class CursesColor:
    COLORS = {
        'COLOR_BLACK': (0, 0, 0, 0),
        'COLOR_RED': (1, 1000, 0, 0),
        'COLOR_GREEN': (2, 0, 1000, 0),
        'COLOR_YELLOW': (3, 1000, 1000, 0),
        'COLOR_BLUE': (4, 0, 0, 1000),
        'COLOR_MAGENTA': (5, 1000, 0, 1000),
        'COLOR_CYAN': (6, 0, 1000, 1000),
        'COLOR_WHITE': (7, 1000, 1000, 1000),
        'COLOR_GREY': (8, 500, 500, 500)
    }

    COLOR_PAIRS = {}

    COLOR_PAIR_BLACK_ON_BLACK = 0
    COLOR_PAIR_RED_ON_BLACK = 1
    COLOR_PAIR_GREEN_ON_BLACK = 2
    COLOR_PAIR_YELLOW_ON_BLACK = 3
    COLOR_PAIR_BLUE_ON_BLACK = 4
    COLOR_PAIR_MAGENTA_ON_BLACK = 5
    COLOR_PAIR_CYAN_ON_BLACK = 6
    COLOR_PAIR_WHITE_ON_BLACK = 7
    COLOR_PAIR_GREY_ON_BLACK = 8

    def start_color(self):
        curses.start_color()
        if os.environ.get('TERM') == 'xterm-256color':
            curses.use_default_colors()
        self._init_colors()
        self._init_color_pairs()

    def _init_colors(self):
        for name, (color_id, r, g, b) in CursesColor.COLORS.items():
            if color_id <= curses.COLORS-1:
                curses.init_color(color_id, r, g, b)
            else:
                raise ValueError(f"Custom color {name} not initialized, color number is greater than COLORS-1")

    def _init_color_pairs(self):
        for color_name, (color_id, r, g, b) in CursesColor.COLORS.items():
            if color_id <= curses.COLORS-1:
                color_pair_name = f"COLOR_PAIR_{color_name.replace('COLOR_', '')}_ON_BLACK"
                color_pair_id = sum((color_id, r, g, b))
                curses.init_pair(color_pair_id, color_id, curses.COLOR_BLACK)
                self.COLOR_PAIRS[color_pair_name] = color_pair_id
                setattr(CursesColor, color_pair_name, color_pair_id)

            else:
                raise ValueError(f"Custom color pair {color_name} not initialized, color number is greater than COLORS-1")

    @staticmethod
    def color_pair(id, fg, bg=-1):
        if bg == -1:
            return curses.color_pair(id) | curses.color_pair(fg)
        else:
            return curses.color_pair(id) | curses.color_pair(fg) | curses.color_pair(bg)



#######

def main(screen):
    # Instantiate the CursesColor class
    curses_color = CursesColor()
    curses_color.start_color()

    # Turn off echoing and enable cbreak mode
    curses.noecho()
    curses.cbreak()

    # Enable keypad mode
    screen.keypad(True)

    # Clear the screen
    screen.clear()
    screen.addstr(f"COLOR_PAIR_RED_ON_BLACK\n", curses.color_pair(curses_color.COLOR_PAIR_RED_ON_BLACK))
    screen.addstr(f"COLOR_PAIR_RED_ON_BLACK\n", curses.color_pair(curses_color.COLOR_PAIR_RED_ON_BLACK))
    screen.addstr(f"COLOR_PAIR_GREEN_ON_BLACK\n", curses.color_pair(curses_color.COLOR_PAIR_GREEN_ON_BLACK))
    screen.addstr(f"COLOR_PAIR_BLUE_ON_BLACK\n", curses.color_pair(curses_color.COLOR_PAIR_BLUE_ON_BLACK))

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