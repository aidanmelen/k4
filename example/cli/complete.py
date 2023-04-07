import curses
import curses.textpad

class MenuWindow:
    LOGO = [
        ' __      _____  ',
        '|  | __ /  |  | ',
        '|  |/ //   |  |_',
        '|    </    ^   /',
        '|__|_ \\____   |',
        '     \\/    |__|'
    ]
    PAD = 1

    def __init__(self, h, w, y, x):
        self.window = curses.newwin(h, w, y, x)
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.max_h = curses.LINES
        self.max_w = curses.COLS
    
    def resize(self):
        curses.update_lines_cols()
        self.max_h = curses.LINES
        self.max_w = curses.COLS
        
        self.window.clear()
        self.window.resize(self.h, self.max_w)
        self.window.refresh()

    def render(self):
        self.window.addstr(0, 0, "Context: None")
        self.window.addstr(1, 0, "<?> Help")
        self.window.addstr(2, 0, "<:> navigate")
        self.window.addstr(3, 0, "<s> search")
        self.window.addstr(4, 0, "<i> Internal")

        # Display k4 logo and align in top/right
        x = self.max_w - len(self.LOGO[0]) - self.PAD
        for y, line in enumerate(self.LOGO):
            if x >= 0:
                self.window.addstr(y, x, line)

        self.window.refresh()

    def handle_input(self, ch):
        pass

class CommandWindow:
    PAD = 1

    def __init__(self, h, w, y, x):
        self.window = curses.newwin(h, w, y, x)
        self.window.border()
        
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.max_h = curses.LINES
        self.max_w = curses.COLS
    
    def resize(self):
        curses.update_lines_cols()
        self.max_h = curses.LINES
        self.max_w = curses.COLS
        
        self.window.clear()
        self.window.resize(self.h, self.max_w)
        self.window.box()
        self.window.refresh()

    def render(self):
        self.window.clear()
        self.window.border()
        self.window.addstr(self.PAD, self.PAD, " > ")
        self.window.refresh()

    def read_input(self):
        self.window.refresh()

        # show cursor
        curses.curs_set(1)

        # minimize ESCAPE delay
        curses.set_escdelay(1)

        prompt = " > "
        input_win = curses.newwin(1, self.max_w - len(prompt) - self.PAD * 2, 7, 4)
        input_win.bkgd(curses.color_pair(10 | curses.A_BOLD))
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

        self.window.clear()

        return cmd.strip()

    def handle_input(self, ch):
        if ch == ord(':'):
            return self.read_input()

class ContentWindow:
    UP = -1
    DOWN = 1
    PAD = 1

    def __init__(self, h, w, y, x):
        self.window = curses.newwin(h, w, y, x)
        self.window.border()

        self.scroll_h = h-2
        self.scroll_w = w-4
        self.scroll_window = curses.newwin(self.scroll_h, self.scroll_w, y+self.PAD, x+(self.PAD*2))

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
        self.window.clear()
        self.scroll_window.clear()

        curses.update_lines_cols()
        self.max_h = curses.LINES
        self.max_w = curses.COLS

        self.h = self.max_h-6-3
        self.window.resize(self.h, self.max_w)
        self.scroll_window.resize(self.h-self.PAD*2, self.max_w-self.PAD*3)

        # Scrolling controls
        self.scroll_h = self.h - self.PAD * 2 # bottom horizontal content borders
        self.scroll_w = self.max_w - self.PAD * 3  # 1 PAD and 2 vertical content borders
        self.max_lines = self.scroll_h
        self.current = min(self.current, self.max_lines)  # Make sure the current selected line is always on screen

        self.window.box()

        self.window.refresh()
        self.scroll_window.refresh()

    def render(self, banner=None, contents=[]):
        self.scroll_window.clear()

        # display banner
        if banner:
            banner = f" {banner.capitalize()}[{len(contents[1:])}] "
            w_center = self.max_w // 2 - len(banner) // 2
            self.window.addstr(0, w_center, banner)
            self.window.refresh()

            self.bottom = len(contents)  # update bottom for scrolling calculations

        # Only display the scrollable lines in focus
        headers = contents[0]
        for idx, text in enumerate(contents[self.top:self.top + self.max_lines]):

            # Add right PAD to the text for cursor highlighting
            right_pad = ' ' * (self.scroll_w - len(text)) 

            # Highlight the current cursor headers line
            if text == headers and self.current == 0:
                self.scroll_window.addnstr(idx, 0, text + right_pad, self.scroll_w, curses.color_pair(20))
            elif text == headers:
                self.scroll_window.addnstr(idx, 0, text, self.scroll_w, curses.color_pair(10))
            
            # Highlight the current cursor line
            elif idx == min(self.current, self.max_lines - 1):
                self.scroll_window.addnstr(idx, 0, text + right_pad, self.scroll_w, curses.color_pair(20))
            else:
                self.scroll_window.addnstr(idx, 0, text, self.scroll_w, curses.color_pair(10))

        self.scroll_window.refresh()

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
        
        self.menu_window = MenuWindow(6, curses.COLS, 0, 0)
        self.command_window = CommandWindow(3, curses.COLS, 6, 0)
        self.content_window = ContentWindow(curses.LINES-(6+3), curses.COLS, 6+3, 0)

        self.stdscr.refresh()
        self.content_window.window.refresh()

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
        self.stdscr.clear()
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
