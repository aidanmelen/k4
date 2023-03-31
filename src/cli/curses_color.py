from typing import Type
import curses
import os


class CursesColor:
    COLOR_DEFAULT = -1

    def __init__(self):
        self._color_name_to_number = {}
        self._used_color_numbers = set()
        self._color_name_to_rgb = {
            "WHITE": (1000, 1000, 1000),
            "BLACK": (0, 0, 0),
            "RED": (1000, 0, 0),
            "GREEN": (0, 1000, 0),
            "BLUE": (0, 0, 1000),
            "YELLOW": (1000, 1000, 0),
            "MAGENTA": (1000, 0, 1000),
            "CYAN": (0, 750, 750),
            "GRAY": (500, 500, 500),
            "ORANGE": (1000, 500, 0),
            "PURPLE": (500, 0, 1000),
            "PINK": (1000, 750, 750),
            "TURQUOISE": (0, 750, 750),
            "GOLD": (1000, 850, 0),
            "SILVER": (750, 750, 750),
            "NAVY": (0, 0, 500),
            "TEAL": (0, 500, 500),
            "LIME": (500, 1000, 0),
            "MAROON": (500, 0, 0),
            "OLIVE": (500, 500, 0),
            "BEIGE": (1000, 1000, 750),
            "BROWN": (750, 500, 250),
            "IVORY": (1000, 1000, 750),
            "SNOW": (1000, 950, 950),
            "TAN": (750, 500, 250),
            "PEACH": (1000, 854, 725),
            "LILAC": (860, 690, 1000),
            "PERIWINKLE": (780, 783, 900),
            "MINT": (750, 1000, 750),
            "AQUAMARINE": (500, 1000, 830),
            "GOLDENROD": (855, 645, 0),
            "ROSE": (1000, 500, 500),
            "TANGERINE": (1000, 643, 0),
            "SKY": (500, 850, 1000),
            "VIOLET": (1000, 0, 1000),
            "AZURE": (0, 500, 1000),
            "CERULEAN": (0, 820, 1000),
            "ECRU": (995, 975, 880),
            "JADE": (0, 560, 400),
            "SAPPHIRE": (59, 322, 729),
            "ELECTRIC_BLUE": (0, 1000, 1000),
            "SCARLET": (750, 0, 0),
            "BURGUNDY": (800, 0, 200),
            "MARIGOLD": (1000, 850, 200),
            "TEAL_GREEN": (0, 510, 490),
            "OLIVE_GREEN": (333, 420, 65),
            "GRASS_GREEN": (0, 604, 90),
            "MAUVE": (880, 690, 690),
            "PEACOCK": (0, 664, 717),
            "SIENNA": (640, 320, 160),
            "STRAW": (1000, 930, 700),
            "CINNAMON": (820, 410, 220),
            "MUSTARD": (1000, 860, 350),
            "PLATINUM": (229, 228, 226),
        }

    def start_color(self):
        curses.start_color()

        if not curses.can_change_color():
            err_msg = "Error: Cannot change colors displayed by the terminal."
            raise ValueError(err_msg)

        if os.environ.get("TERM") != "xterm-256color":
            err_msg = "Error: No extended color support found. This allows more than 256 color pairs for terminals that support more than 16 colors (e.g. xterm-256color)"
            raise ValueError(err_msg)

        curses.use_default_colors()

    def init_colors(self):
        for color_name, color_rgb in self._color_name_to_rgb.items():
            self[color_name] = color_rgb

    @property
    def color_name_to_number(self):
        return self._color_name_to_number

    def color_content_by_name(self, color_name):
        return curses.color_content(self._color_name_to_number[color_name])

    def color_content_by_number(self, color_number):
        return curses.color_content(color_number)

    def next_color_number(self):
        # use color numbers from highest to lowest to override the 8-bit color numbers last
        for color_number in range(curses.COLORS-1, -1, -1):
            if color_number not in self._used_color_numbers:
                return color_number
        else:
            raise ValueError("Color is greater than 255 (curses.COLORS - 1).")

    def is_color_initialized(self, color_number):
        return color_number in self._color_name_to_number.values()

    def __setitem__(self, color_name, rgb):
        color_name = str(color_name).upper()
        
        if color_name in self._color_name_to_number:
            # update existing color
            self._color_name_to_rgb[color_name] = rgb
        else:
            # create new color
            color_number = self.next_color_number()
            self._color_name_to_number[color_name] = color_number
            self._used_color_numbers.add(color_number)

        curses.init_color(color_number, *rgb)

    def __getitem__(self, color_name):
        return self._color_name_to_number[color_name]

    def get(self, color_name, default=COLOR_DEFAULT):
        return self._color_name_to_number.get(color_name, default)

    def __iter__(self):
        return iter(self._color_name_to_number.items())

    def items(self):
        return self._color_name_to_number.items()


class CursesColorPair:
    COLOR_PAIR_DEFAULT = 0

    def __init__(self, curses_color: Type[CursesColor]):
        self._curses_color = curses_color
        self._pair_name_to_number = {}
        self._used_pair_numbers = set()

    def init_pairs(self, bg_color_name=None):
        bg_color_name = str(bg_color_name).upper()
        bg_color_number = self._curses_color.get(bg_color_name)

        for fg_color_name, fg_color_number in self._curses_color:
            self.init_pair(fg_color_name, bg_color_name)

    def init_pair(self, fg_color_name=None, bg_color_name=None):
        pair_name = f"{fg_color_name}_ON_{bg_color_name}".upper()

        fg_color_number = self._curses_color.get(fg_color_name)
        bg_color_number = self._curses_color.get(bg_color_name)

        if not fg_color_number:
            raise ValueError(f"The foreground color name {fg_color_name} has not been initialized.")
        
        if not bg_color_number:
            raise ValueError(f"The background color name {bg_color_name} has not been initialized.")

        self[pair_name] = (fg_color_name, bg_color_name)        

    def next_pair_number(self):
        for pair_number in range(1, curses.COLOR_PAIRS - 1):
            if pair_number not in self._used_pair_numbers:
                return pair_number
        else:
            raise ValueError("Color pair is greater than 32765 (curses.COLOR_PAIRS - 1).")

    @property
    def pair_name_to_number(self):
        return self._pair_name_to_number

    def __setitem__(self, pair_name, color_pair_names):
        if len(color_pair_names) != 2:
            raise ValueError("color_pair_names must be a 2-tuple of color names.")

        fg_color_name, bg_color_name = map(str.upper, color_pair_names)
        pair_number = self.next_pair_number()
        curses.init_pair(
            pair_number, self._curses_color.get(fg_color_name), self._curses_color.get(bg_color_name)
        )
        self._pair_name_to_number[pair_name] = curses.color_pair(pair_number)
        self._used_pair_numbers.add(pair_number)

    def __getitem__(self, name):
        return self._pair_name_to_number[name]
    
    def get(self, pair_name, default=COLOR_PAIR_DEFAULT):
        return self._pair_name_to_number.get(pair_name, default)

    def __iter__(self):
        return iter(self._pair_name_to_number.items())
    
    def items(self):
        return self._pair_name_to_number.items()
