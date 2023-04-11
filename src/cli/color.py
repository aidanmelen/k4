from curses_wrapper.color import CursesColor, CursesColorPair

# Start colors and init color pairs
curses_color = CursesColor()
curses_color_pair = CursesColorPair(curses_color)

# NOTE: colors are started and color pairs are initialized in controller.py after curses.initscr()
