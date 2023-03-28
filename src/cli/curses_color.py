from typing import Type
import curses
import os


class CursesColor:
    COLOR_DEFAULT = -1

    def __init__(self):
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
            "PEACOCK": (51, 161, 201),
            "SIENNA": (640, 320, 160),
            "STRAW": (1000, 930, 700),
            "CINNAMON": (820, 410, 220),
            "MUSTARD": (1000, 860, 350),
            "PLATINUM": (229, 228, 226),
        }

        self._color_name_to_number = {}
        self._used_color_numbers = set()

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
        return curses.color_content(self._color_name_to_number.get(color_name))
    
    def color_content_by_number(self, color_number):
        return curses.color_content(color_number)

    def __setitem__(self, color_name, rgb):
        if color_name == "DEFAULT":
            self._color_name_to_number[color_name] = self.COLOR_DEFAULT

        num_of_predefined_colors = 8
        for color_number in range(num_of_predefined_colors, curses.COLORS):
            if color_number not in self._used_color_numbers:
                curses.init_color(color_number, *rgb)
                self._color_name_to_rgb[color_name] = rgb
                self._color_name_to_number[color_name] = color_number
                self._used_color_numbers.add(color_number)
                break
        else:
            raise RuntimeError("All 256 colors are already set")

    def __getitem__(self, color_name):
        if color_name == "DEFAULT":
            return self.COLOR_DEFAULT
        return self._color_name_to_number[color_name]
    
    def get(self, color_name, default=None):
        if color_name == "DEFAULT":
            return self.COLOR_DEFAULT
        return self._color_name_to_number.get(color_name, default)

    def __iter__(self):
        return iter(self._color_name_to_number.items())


class CursesColorPair:
    def __init__(self, named_curses_color: Type[CursesColor]):
        self._curses_color = named_curses_color
        self._color_pair_name_to_number = {}
        self._used_color_pair_numbers = set()

    def init_color_pair_by_name(self, fg_color_name, bg_color_name="BLACK"):
        pair_name = f"{fg_color_name}_ON_{bg_color_name}"
        fg_color_number = self._curses_color.get(fg_color_name)
        bg_color_number = self._curses_color.get(bg_color_name)

        if not fg_color_number:
            raise ValueError(f"The foreground color name {fg_color_name} has not been initialized.")
        
        if not bg_color_number:
            raise ValueError(f"The background color name {bg_color_name} has not been initialized.")
        
        pair_number = sum((fg_color_number, bg_color_number))

        curses.init_pair(pair_number, self._curses_color[fg_color_name], self._curses_color[bg_color_name])
        self._color_pair_name_to_number[pair_name] = curses.color_pair(pair_number)
    
    def init_color_pair_by_number(self, fg_color_number, bg_color_number):
        color_number_to_name = {number: name for name, number in self._curses_color.color_name_to_number.items()}
        fg_color_name = color_number_to_name.get(fg_color_number)
        bg_color_name = color_number_to_name.get(bg_color_number)

        if not fg_color_name:
            raise ValueError(f"The foreground color number {fg_color_number} has not been initialized.")
        
        if not bg_color_name:
            raise ValueError(f"The background color number {bg_color_number} has not been initialized.")
        
        pair_name = f"{fg_color_name}_ON_{bg_color_name}"
        pair_number = sum((fg_color_number, bg_color_number))

        curses.init_pair(pair_number, self._curses_color[fg_color_name], self._curses_color[bg_color_name])
        self._color_pair_name_to_number[pair_name] = curses.color_pair(pair_number)

    def init_color_pairs(self, bg_color_name="DEFAULT"):
        for fg_color_name, fg_color_number in self._curses_color:
            pair_name = f"{fg_color_name}_ON_{bg_color_name}"
            pair_number = sum((fg_color_number, self._curses_color[bg_color_name]))

            curses.init_pair(pair_number, fg_color_number, self._curses_color[bg_color_name])
            self._color_pair_name_to_number[pair_name] = curses.color_pair(pair_number)

    @property
    def color_pairs_name_to_number(self):
        return self._color_pair_name_to_number

    # def __setitem__(self, name, color_number):
    #     # TODO
    #     curses.init_pair(pair_number, self._curses_color[fg_color_name], self._curses_color[bg_color_name])
    #     self._color_pair_name_to_number[pair_name] = curses.color_pair(pair_number)
    #     return self._color_pair_name_to_number[name] = color_number

    def __getitem__(self, name):
        return self._color_pair_name_to_number[name]
    
    def __iter__(self):
        return iter(self._color_pair_name_to_number.items())
