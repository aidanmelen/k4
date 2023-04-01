from typing import Type, Dict, Tuple, Iterator, ItemsView
import curses
import os


class CursesColor:
    """A wrapper around the curses color functionality.

    This class provides a higher-level interface to the curses color
    functionality, allowing the user to work with color names and
    RGB values instead of low-level color numbers.

    Attributes:
        COLOR_DEFAULT (int): The default color number.
    """

    COLOR_DEFAULT: int = -1

    def __init__(self) -> None:
        """Initializes a new CursesColorPair object."""
        self._color_name_to_number: Dict[str, int] = {}
        self._used_color_numbers: set = set()
        self._color_name_to_rgb: Dict[str, Tuple[int, int, int]] = {
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
        self.__has_colors: bool = False

    def start_color(self) -> None:
        """Initializes curses colors and ensures that the terminal support 256 colors."""
        curses.start_color()

        if not curses.can_change_color():
            raise Exception("Cannot change colors displayed by the terminal.")

        if os.environ.get("TERM") != "xterm-256color":
            raise Exception("No extended color support found.")

        curses.use_default_colors()
        self.__has_colors = True

    def init_colors(self) -> None:
        """Initializes the extended colors."""
        for color_name, color_rgb in self._color_name_to_rgb.items():
            self[color_name] = color_rgb
    
    @property
    def has_colors(self) -> bool:
        """Returns True if the terminal supports colors."""
        return self.__has_colors

    @property
    def color_name_to_number(self) -> Dict[str, int]:
        """Returns a dictionary mapping color names to their corresponding color numbers."""
        return self._color_name_to_number

    def color_content_by_name(self, color_name: str) -> Tuple[int, int, int]:
        """Returns the RGB values of the color with the given name."""
        return curses.color_content(self._color_name_to_number[color_name])

    def color_content_by_number(self, color_number: int) -> Tuple[int, int, int]:
        """Returns the RGB values of the color with the given number."""
        return curses.color_content(color_number)

    def is_color_initialized(self, color_number: int) -> bool:
        """Returns True if the color with the given number has been initialized."""
        return color_number in self._color_name_to_number.values()

    def next_color_number(self) -> int:
        """Returns the next available color number from highest to lowest."""
        for color_number in range(curses.COLORS-1, -1, -1):
            if color_number not in self._used_color_numbers:
                return color_number
        else:
            raise Exception(f"All {curses.COLORS} colors are set.")

    def __setitem__(self, color_name: str, rgb: Tuple[int, int, int]) -> None:
        """Sets a color by name and its corresponding RGB values."""
        color_name = str(color_name).upper()
        
        if color_name in self._color_name_to_number:
            # update existing color
            color_number = self[color_name]
            self._color_name_to_rgb[color_name] = rgb
            curses.init_color(color_number, *rgb)

        else:
            # create new color
            color_number = self.next_color_number()
            self._color_name_to_number[color_name] = color_number
            self._used_color_numbers.add(color_number)
            curses.init_color(color_number, *rgb)

    def __getitem__(self, color_name: str) -> int:
        """Returns the color number of a given color name."""
        return self._color_name_to_number[color_name]

    def get(self, color_name: str, default_color_number: int = COLOR_DEFAULT) -> int:
        """Returns the color number of a given color name, or a default value if the color name does not exist."""
        return self._color_name_to_number.get(color_name, default_color_number)

    def __iter__(self) -> Iterator[Tuple[str, int]]:
        """Returns an iterator over the color name to color number mapping."""
        return iter(self._color_name_to_number.items())

    def items(self) -> ItemsView[str, int]:
        """Returns a view object containing the color name to color number mapping."""
        return self._color_name_to_number.items()