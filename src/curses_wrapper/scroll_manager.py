from typing import List, Dict
import curses


class ScrollManager:
    UP = -1
    DOWN = 1

    def init(self, window: curses.window, color_pair_id: int = 1, start_line: int = 0) -> None:
        """
        Initialize the screen window
        ┌--------------------------------------┐
        |1. Item                               |
        |--------------------------------------| <- top = 1
        |2. Item                               |
        |3. Item                               |
        |4./Item///////////////////////////////| <- current = 3
        |5. Item                               |
        |6. Item                               |
        |7. Item                               |
        |8. Item                               | <- max_lines = 7
        |--------------------------------------|
        |9. Item                               |
        |10. Item                              | <- bottom = 10
        |                                      |
        |                                      | <- page = 1 (0 and 1)
        └--------------------------------------┘
        Attributes
            window: A full curses screen window
        Returns
            None
        """
        self.window = window
        self.color_pair_id = color_pair_id

        self.max_y, self.max_x = self.window.getmaxyx()
        self.y, self.x = self.window.getbegyx()

        # Initialize scroll items
        self.__items = []
        self.current_item = {}

        # Maximum visible line count for window
        self.max_lines = self.max_y

        # Available top line position for current page (used on scrolling)
        self.top = 0

        # Available bottom line position for whole pages (as length of items)
        self.bottom = len(self.__items)

        # Current highlighted line number (as window cursor)
        self.current = start_line

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items: List[Dict[str, str]]):
        # Update scroll book-keeping given the items
        self.__items = items
        self.bottom = len(self.__items)

    def scroll(self, direction: int) -> None:
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (
            (direction == self.DOWN)
            and (next_line == self.max_lines)
            and (self.top + self.max_lines < self.bottom)
        ):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (
            (direction == self.DOWN)
            and (next_line < self.max_lines)
            and (self.top + next_line < self.bottom)
        ):
            self.current = next_line
            return

    def paging(self, direction: int) -> None:
        """Paging the window when pressing left/right arrow keys"""
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        self.current = min(self.current, self.bottom - self.top - 1)

        # Page up
        # top position can not be negative, so if top position is going to be negative, we should set it as 0
        if direction == self.UP:
            self.top = max(0, self.top - self.max_lines)
        # Page down
        # top position should not be greater than the number of items, so we must restrict it
        elif direction == self.DOWN:
            self.top += min(self.max_lines, self.bottom - self.top - 1)

    def handle_input(self, ch: int) -> None:
        if ch == curses.KEY_UP:
            self.scroll(self.UP)
        elif ch == curses.KEY_DOWN:
            self.scroll(self.DOWN)
        elif ch == curses.KEY_LEFT:
            self.paging(self.UP)
        elif ch == curses.KEY_RIGHT:
            self.paging(self.DOWN)

    def select_line(self):
        """Return the line from the current item."""
        return str(self.current_item.get("line"))

    def select_line_color_pair_id(self):
        """Return the line color pair id from the current item."""
        return int(self.current_item.get("color_pair_id", self.color_pair_id))

    def display(self, should_pad_right_with_spaces: bool = True) -> None:
        """Display a scrollable list of items."""
        # Erase the window to prevent streaking on scroll
        self.window.erase()

        # Ensure lines are written within window columns
        # self.max_x = self.self.max_x - 1

        for y, item in enumerate(self.__items[self.top : self.top + self.max_lines]):

            line = item["line"]
            color_pair_id = item.get("color_pair_id", self.color_pair_id)

            if should_pad_right_with_spaces:
                spaces = " " * (self.max_x - len(item))
                line += spaces

            # Highlight the current cursor line
            try:
                if y == self.current:
                    self.window.addnstr(y, 0, line, self.max_x, color_pair_id | curses.A_REVERSE | curses.A_BOLD)
                    self.current_item = item
                elif self.max_y > 0:
                    self.window.addnstr(y, 0, line, self.max_x, color_pair_id)
            except curses.error:
                # Do not crash when user scrolls to the last line of the window.
                continue

        self.window.refresh()
