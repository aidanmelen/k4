from .custom_color import *

import curses
import curses.textpad
import time

class CursesWindow():
    PAD = 1

    def __init__(self, h, w, y, x):
        self._window = curses.newwin(h, w, y, x)

        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.max_h = curses.LINES
        self.max_w = curses.COLS

        self.last_render_time = 0
        self.has_toggle_changed = False

        curses.start_color()
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    @property
    def window(self):
        return self._window
        
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
    
    def erase(self):
        self._window.erase()

class MenuWindow(CursesWindow):
    LOGO = [
        ' __      _____  ',
        '|  | __ /  |  | ',
        '|  |/ //   |  |_',
        '|    </    ^   /',
        '|__|_ \\____   |',
        '     \\/    |__|'
    ]

    def __init__(self, h, w, y, x):
        """
        A curses menu window wrapper class. For example:

        Context: None                     __      _____
        <?> Help                         |  | __ /  |  |
        <:> navigate                     |  |/ //   |  |_ <- menu window
        <s> search                       |    </    ^   /
        <i> Internal                     |__|_ \____   |
                                              \/    |__|
        """
        super().__init__(h, w, y, x)
    
    def resize(self):
        super().resize()

    def render(self):
        super().render()
        self._window.addstr(0, 0, "Context: None", curses.color_pair(10))
        self._window.addstr(1, 0, "<?> Help", curses.color_pair(10))
        self._window.addstr(2, 0, "<:> navigate", curses.color_pair(10))
        self._window.addstr(3, 0, "<s> search", curses.color_pair(10))
        self._window.addstr(4, 0, "<i> Internal", curses.color_pair(10))

        # Display k4 logo and align in top/right
        x = self.max_w - len(self.LOGO[0]) - self.PAD
        for y, line in enumerate(self.LOGO):
            if x >= 0:
                self._window.addstr(y, x, line)

        self._window.refresh()

    def handle_input(self, ch):
        pass
    
    def erase(self):
        super().erase()
    

class CommandWindow(CursesWindow):
    def __init__(self, h, w, y, x):
        """
        A curses command window wrapper class. For example:

        ┌────────────────────────────────────────────────┐
        │ > textpad                                      │<- command window
        └────────────────────────────────────────────────┘
        """
        super().__init__(h, w, y, x)
    
    def resize(self):
        super().resize()
        self._window.border()
        self._window.refresh()
    
    def erase(self):
        super().erase()

    def render(self):
        super().render()
        self._window.erase()
        self._window.border()
        self._window.addstr(self.PAD, self.PAD, " > ")
        self._window.refresh()

    def read_input(self):
        self._window.refresh()

        curses.curs_set(1)  # show cursor

        prompt = " > "
        input_win = curses.newwin(1, self.max_w - len(prompt) - self.PAD * 2, 7, 4)
        # input_win.bkgd(curses.color_pair(CYAN_ON_BLACK.id | curses.A_BOLD))
        input_pad = curses.textpad.Textbox(input_win, insert_mode=True)

        def validate(ch):

            # exit input with the escape key
            escape = 27
            if ch == escape:
                ch = curses.ascii.BEL # Control-G
            
            # exit input to resize windows
            elif ch == curses.KEY_RESIZE:
                ch = curses.ascii.BEL # Control-G

            return ch

        input_pad.edit(validate)
        cmd = input_pad.gather()

        curses.curs_set(0)  # hide cursor

        self._window.erase()

        return cmd.strip()

    def handle_input(self, ch):
        if ch == ord(':'):
            return self.read_input()
    
    def erase(self):
        super().erase()

class ContentWindow(CursesWindow):
    UP = -1
    DOWN = 1
    PAD = 1

    def __init__(self, h, w, y, x):
        """
        A curses content window wrapper class. For example:

        ┌─────────────────── Topics[4] ──────────────────┐
        │ TOPIC                              PARTITION   │
        │ _schemas                           1           │
        │ connect-configs                    1         <---- scroll window
        │ connect-offsets                    25          │
        │ connect-status                     5           │<- content window
        │                                                │
        └────────────────────────────────────────────────┘
        """
        super().__init__(h, w, y, x)
        self._window.border()
        self._window.refresh()

        self.scroll_h = h-2
        self.scroll_w = w-4
        self._scroll_window = curses.newwin(self.scroll_h, self.scroll_w, y+self.PAD, x+(self.PAD*2))

        self.max_lines = self.scroll_h
        self.top = 0
        self.bottom = 0
        self.current = 1 # line 0 should be the tabulated headers

        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.max_h = curses.LINES
        self.max_w = curses.COLS
    
    @property
    def scroll_window(self):
        return self._scroll_window
    
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

        self.h = self.max_h-6-3
        self._window.resize(self.h, self.max_w)
        self._scroll_window.resize(self.h-self.PAD*2, self.max_w-self.PAD*3)

        # Scrolling controls
        self.scroll_h = self.h - self.PAD * 2 # bottom horizontal content borders
        self.scroll_w = self.max_w - self.PAD * 3  # 1 PAD and 2 vertical content borders
        self.max_lines = self.scroll_h
        self.current = min(self.current, self.max_lines)  # Make sure the current selected line is always on screen

        self._window.box()

        self._window.refresh()
        self._scroll_window.refresh()
    
    def render(self, banner=None, contents=[]):
        super().render()
        self._scroll_window.erase()

        # display banner
        if banner:
            banner = f" {banner}s[{len(contents[1:])}] "
            w_center = self.max_w // 2 - len(banner) // 2
            self._window.addstr(0, w_center, banner)
            self._window.refresh()

            self.bottom = len(contents)  # update bottom for scrolling calculations

        # Only display the scrollable lines in focus
        if contents:
            headers = contents[0]

        for idx, item in enumerate(contents[self.top:self.top + self.max_lines]):

            # Truncate the item to the width of the window
            text = item[:self.scroll_w - self.PAD * 2]

            # Add right PAD to the item for cursor highlighting
            right_pad = ' ' * (self.scroll_w - 1 - len(item)) 

            # Highlight the current cursor headers line
            if item == headers and self.current == 0:
                self._scroll_window.addstr(idx, 0, text + right_pad, curses.color_pair(20))
            elif item == headers:
                self._scroll_window.addstr(idx, 0, text, curses.color_pair(10))
            
            # Highlight the current cursor line
            elif idx == min(self.current, self.max_lines - 1):
                self._scroll_window.addstr(idx, 0, text + right_pad, curses.color_pair(20))
            else:
                self._scroll_window.addstr(idx, 0, text, curses.color_pair(10))

        self._window.refresh()
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
    
    def erase(self):
        super().erase()
