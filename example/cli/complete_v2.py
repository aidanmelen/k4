import curses
import curses.textpad
import time

class BaseWindow():
    PAD = 1

    def __init__(self, stdscr, h, w, y, x):
        self._window = stdscr.subwin(h, w, y, x)

        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.max_h = curses.LINES
        self.max_w = curses.COLS

        self.last_render_time = 0
        self.has_toggle_changed = False

    def resize(self):
        curses.update_lines_cols()
        self.max_h = curses.LINES
        self.max_w = curses.COLS

        self._window.erase()
        self._window.resize(self.h, self.max_w)
        self._window.refresh()

    def render(self):
        current_time = time.perf_counter()
        elapsed_time = current_time - self.last_render_time

class MenuWindow(BaseWindow):
    LOGO = [
        ' ____  __.  _____         ',
        '|    |/ _| /  |  | ______ ',
        '|      <  /   |  |/  ___/ ',
        '|    |  \\/    ^   \___ \\  ',
        '|____|__ \\____   /____  > ',
        '        \\/    |__|    \\/  '
    ]

    def __init__(self, stdscr, h, w, y, x):
        super().__init__(stdscr, h, w, y, x)

    def resize(self):
        super().resize()

    def render(self):
        super().render()

        info = {
            "context": None,
            "cluster": None,
            "user": None
        }

        options = {
            "1": "internal",
        }

        controls = {
            "ctrl-d": "Delete",
            "d": "Describe",
            "e": "Edit",
            "?": "Help"
        }

        # info
        for idx, k in enumerate(info.keys()):
            key_str = f"{k.capitalize()}: "
            value_str = str(info[k])
            max_value_str = self.max_w - 1 - len(key_str) - len(self.LOGO[0])

            self._window.addnstr(idx, 1, key_str, self.max_w)

            if max_value_str > 0:
                self._window.addnstr(idx, 1 + len(key_str), value_str, max_value_str, curses.A_BOLD)

        # options
        for idx, k in enumerate(options.keys()):
            key_str = f"<{k}> "
            value_str = str(options[k])
            max_value_str = self.max_w - 40 - len(key_str)

            if self.max_w - 40 > 0:
                self._window.addnstr(idx, 40, key_str, self.max_w - 40, curses.A_BOLD)

            if max_value_str > 0:
                self._window.addnstr(idx, 40 + len(key_str), value_str, max_value_str)

        # controls
        for idx, k in enumerate(controls.keys()):
            key_str = f"<{k}> "
            value_str = str(controls[k])
            max_value_str = self.max_w - 60 - len(key_str)

            if self.max_w - 60 > 0:
                self._window.addnstr(idx, 60, key_str, self.max_w - 60, curses.A_BOLD)

            if max_value_str > 0:
                self._window.addnstr(idx, 60 + len(key_str), value_str, max_value_str)

        # logo
        for idx, line in enumerate(self.LOGO):
            x = max(self.max_w - len(self.LOGO[0]), 0)
            self._window.addnstr(max(idx, 0), x, line, self.max_w - 1, curses.A_BOLD)

        self._window.refresh()

    def handle_input(self, ch):
        pass

class CommandWindow(BaseWindow):
    def __init__(self, stdscr, h, w, y, x):
        super().__init__(stdscr, h, w, y, x)

    def resize(self):
        super().resize()
        self._window.border()
        self._window.refresh()

    def render(self):
        super().render()
        self._window.erase()
        self._window.border()
        self._window.addstr(self.PAD, self.PAD, " > ")
        self._window.refresh()

    def read_input(self):
        self._window.refresh()

        # show cursor
        curses.curs_set(1)

        # minimize ESCAPE delay
        curses.set_escdelay(1)

        prompt = " > "
        input_win = curses.newwin(1, self.max_w - len(prompt) - self.PAD * 2, 7, 4)
        input_pad = curses.textpad.Textbox(input_win, insert_mode=True)

        def validate(ch):

            # exit input with the escape key
            escape = 27
            if ch == escape:
                ch = curses.ascii.BEL # Control-G
            
            # delete the character to the left of the cursor
            elif ch in (curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
                ch = curses.KEY_BACKSPACE

            # exit input to resize windows
            elif ch == curses.KEY_RESIZE:
                ch = curses.ascii.BEL # Control-G

            return ch

        input_pad.edit(validate)
        cmd = input_pad.gather()

        # close cursor
        curses.curs_set(0)
        
        # reset ESCAPE delay
        curses.set_escdelay(1000)

        self._window.erase()

        return cmd.strip()

    def handle_input(self, ch):
        if ch == ord(':'):
            return self.read_input()

class ContentWindow(BaseWindow):
    UP = -1
    DOWN = 1
    PAD = 1

    def __init__(self, stdscr, h, w, y, x):
        super().__init__(stdscr, h, w, y, x)
        self._window.border()

        self.scroll_h = h - self.PAD * 2
        self.scroll_w = w - self.PAD * 3
        self._scroll_window = curses.newwin(self.scroll_h, self.scroll_w, y + self.PAD, x + (self.PAD * 2))

        self.max_lines = self.scroll_h
        self.top = 0
        self.bottom = 0
        self.current = 1 # line 0 should be the tabulated headers

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor p.ition after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor p.ition is 0, but top p.ition is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor p.ition touch the max lines, but absolute p.ition of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor p.ition or top p.ition is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor p.ition is above max lines, and absolute p.ition of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor p.ition as maximum item count on last page
        self.current = min(self.current, self.bottom - self.top - 1)

        # Page up
        # top p.ition can not be negative, so if top p.ition is going to be negative, we should set it as 0
        if (direction == self.UP):
            self.top = max(0, self.top - self.max_lines)
        # Page down
        # top p.ition should not be greater than the number of items, so we must restrict it
        elif (direction == self.DOWN):
            self.top += min(self.max_lines, self.bottom - self.top - 1)

    def resize(self):
        self._window.erase()
        self._scroll_window.erase()

        curses.update_lines_cols()
        self.max_h = curses.LINES
        self.max_w = curses.COLS

        self.h = self.max_h - 6 - 3

        if self.h > 1:
            self._window.resize(self.h, self.max_w)
            self._window.box()
            self._window.refresh()

        # Scroll book-keeping
        self.scroll_h = self.h - self.PAD * 2 # top and bottom horizontal content borders
        self.scroll_w = self.max_w - self.PAD * 3 # 1 PAD and 2 vertical content borders
        self.max_lines = self.scroll_h
        self.current = min(self.current, self.max_lines)  # Make sure the current selected line is always on screen

        if self.scroll_h > 2:
            self._scroll_window.resize(self.scroll_h, self.scroll_w)
            self._scroll_window.refresh()


    def render(self, banner=None, contents=[]):

        self._scroll_window.erase()

        # display banner
        if banner:
            banner_1 = f" {banner.capitalize()}"
            banner_2 = "("
            banner_3 = "all"
            banner_4 = ")["
            banner_5 = f"{len(contents) - 1}" # do not count header
            banner_6 = f"] "
            banner_ = f"{banner_1}{banner_2}{banner_3}{banner_4}"
            w_center = self.scroll_w // 2 - len(banner_) // 2

            if len(banner_) < self.max_w - self.PAD * 4:
                self._window.addstr(0, w_center, banner_1, curses.A_BOLD)
                self._window.addstr(banner_2)
                self._window.addstr(banner_3, curses.A_BOLD)
                self._window.addstr(banner_4)
                self._window.addstr(banner_5, curses.A_BOLD)
                self._window.addstr(banner_6)
                self._window.refresh()


        self.bottom = len(contents)  # update bottom for scrolling calculations

        # Only display the scrollable lines in focus
        headers = contents[0]
        for idx, item in enumerate(contents[self.top:self.top + self.max_lines]):

            # Truncate the item to the width of the window
            text = item[:self.scroll_w - self.PAD * 2]

            # Add right PAD to the item for cursor highlighting
            right_space_highlight = ' ' * (self.scroll_w - len(item) - 1) 

            # Highlight the current cursor headers line
            if text == headers and self.current == 0:
                self._scroll_window.addstr(idx, 0, text + right_space_highlight, curses.A_REVERSE)
            elif idx == 0 and item == headers:
                self._scroll_window.addstr(idx, 0, text)
            
            # Highlight the current cursor line
            elif idx == self.current:
                self._scroll_window.addstr(idx, 0, text + right_space_highlight, curses.A_REVERSE)
            elif self.scroll_h > 0:
                self._scroll_window.addstr(idx, 0, text)

        self._scroll_window.refresh()

    def handle_input(self, ch):        
        # Handle arrow scrolling inputs
        if ch == curses.KEY_UP:
            self.scroll(self.UP)

        elif ch == curses.KEY_DOWN:
            self.scroll(self.DOWN)

        elif ch == curses.KEY_LEFT:
            self.paging(self.UP)

        elif ch == curses.KEY_RIGHT:
            self.paging(self.DOWN)

class Screen:
    def __init__(self):
        self.stdscr = curses.initscr()

        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        self.menu_window = MenuWindow(self.stdscr, 6, curses.COLS, 0, 0)
        self.command_window = CommandWindow(self.stdscr, 3, curses.COLS, 6, 0)
        self.content_window = ContentWindow(self.stdscr, curses.LINES-(6+3), curses.COLS, 6+3, 0)

        self.stdscr.refresh()
        self.content_window._window.refresh()

        self._focus = None
        self._contents = []

    @property
    def focus(self):
        return self._focus
    
    @property
    def contents(self):
        return self._contents

    @focus.setter
    def focus(self, value):
        self._focus = value
    
    @contents.setter
    def contents(self, value):
        self._contents = value
    
    def resize(self):
        self.stdscr.erase()
        self.stdscr.refresh()
        self.menu_window.resize()
        self.command_window.resize()
        self.content_window.resize()

    def render(self):
        self.menu_window.render()
        self.command_window.render()

        if self._focus and self._contents:
            self.content_window.render(self._focus, self._contents)

def main():
    try:
        screen = Screen()

        ch = 0
        while ch != ord('q'):
            screen.render()
            ch = screen.stdscr.getch()
            command = screen.command_window.handle_input(ch)
            
            if command in ["topics", "tops", "t"]:
                screen.focus = "topics"

                # TODO get dynamically
                screen.contents = [
                    "TOPIC                              PARTITION",
                    "_schemas_schemaregistry_confluent  1        ",
                    "confluent.connect-configs          1        ",
                    "confluent.connect-offsets          25       ",
                    "confluent.connect-status           5        "
                ]

            screen.menu_window.handle_input(ch)
            screen.content_window.handle_input(ch)

            if ch == curses.KEY_RESIZE:
                screen.resize()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == '__main__':
    main()
    # curses.wrapper(main)
