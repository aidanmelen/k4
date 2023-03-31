from typing import Type, Dict, Tuple, Iterator, ItemsView
from .color import CursesColor
import curses


class CursesColorPair:
    """A wrapper around the curses color pair functionality.

    This class provides a higher-level interface to the curses color
    pair functionality, allowing the user to work with color pair names
    and low-level color pair numbers.

    Attributes:
        COLOR_PAIR_DEFAULT (int): The default color pair number.
    """

    COLOR_PAIR_DEFAULT: int = 0

    def __init__(self, curses_color: Type[CursesColor]) -> None:
        """
        Initializes a new CursesColorPair object.

        Args:
            curses_color (Type[CursesColor]): A CursesColor object representing the color palette.
        """
        self._curses_color = curses_color
        self._pair_name_to_number = {}
        self._used_pair_numbers = set()

    def init_pairs(self, bg_color_name: str = None) -> None:
        """Initializes color pairs for all possible foreground/background color permutations."""
        if not self._curses_color.has_colors:
            raise RuntimeError("must call CursesColor().init_colors() before initializing the extended color pairs.")

        bg_color_name = str(bg_color_name).upper()
        bg_color_number = self._curses_color.get(bg_color_name)

        for fg_color_name, fg_color_number in self._curses_color:
            self.init_pair(fg_color_name, bg_color_name)

    def init_pair(self, fg_color_name: str = None, bg_color_name: str = None) -> None:
        """Initializes a color pair with the specified foreground and background colors."""
        pair_name = f"{fg_color_name}_ON_{bg_color_name}".upper()

        fg_color_number = self._curses_color.get(fg_color_name)
        bg_color_number = self._curses_color.get(bg_color_name)

        if not fg_color_number:
            raise ValueError(f"The foreground color name {fg_color_name} has not been initialized.")
        
        if not bg_color_number:
            raise ValueError(f"The background color name {bg_color_name} has not been initialized.")

        self[pair_name] = (fg_color_name, bg_color_name)        

    def next_pair_number(self) -> int:
        """Returns the next available color pair number from lowest to highest."""
        for pair_number in range(1, curses.COLOR_PAIRS - 1):
            if pair_number not in self._used_pair_numbers:
                return pair_number
        else:
            raise ValueError("Error: Color pair is greater than 32765 (curses.COLOR_PAIRS - 1).")

    @property
    def pair_name_to_number(self) -> Dict[str, int]:
        """Returns a dictionary mapping pair names to pair numbers."""
        return self._pair_name_to_number

    def __setitem__(self, pair_name: str, color_pair_names) -> None:
        """Sets a color pair with the specified name and color pair."""
        if len(color_pair_names) != 2:
            raise ValueError("color_pair_names must be a 2-tuple of color names.")

        fg_color_name, bg_color_name = map(str.upper, color_pair_names)
        pair_number = self.next_pair_number()
        curses.init_pair(
            pair_number, self._curses_color.get(fg_color_name), self._curses_color.get(bg_color_name)
        )
        self._pair_name_to_number[pair_name] = curses.color_pair(pair_number)
        self._used_pair_numbers.add(pair_number)

    def __getitem__(self, name: str) -> int:
        """Get the color pair number associated with the specified color pair name."""
        return self._pair_name_to_number[name]
    
    def get(self, pair_name: str, default: int = COLOR_PAIR_DEFAULT) -> int:
        """Get the color pair number associated with the specified color pair name, or the default value if not found."""
        return self._pair_name_to_number.get(pair_name, default)

    def __iter__(self) -> Iterator[Tuple[str, int]]:
        """Get an iterator over the color pairs."""
        return iter(self._pair_name_to_number.items())
    
    def items(self)-> ItemsView[str, int]:
        """Get an iterator over the color pairs."""
        return self._pair_name_to_number.items()