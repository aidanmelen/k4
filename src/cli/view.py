from .color import curses_color_pair

import curses
import curses.textpad
import itertools

class BaseView:
    LOGO = [
        ' ____      _____  ',
        '|    | __ /  |  | ',
        '|    |/ //   |  |_',
        '|      </    ^   /',
        '|____|_ \\____   |',
        '       \\/    |__|'
    ]

    def __init__(self, window):
        # Initialize and clear the main window
        self.window = window
        self.window.bkgd(curses_color_pair["WHITE_ON_NONE"])
        self.handle_resize()
    
    def handle_resize(self):
        self.window.clear()

        # Set window height and y-position book-keeping
        self.max_y, self.max_x = self.window.getmaxyx()
        self.top_h = len(self.LOGO)
        self.input_h = 0
        self.bottom_h = 2
        self.bottom_y = self.max_y - self.bottom_h
        self.middle_h = self.max_y - self.top_h - self.input_h - self.bottom_h
        self.middle_y = self.top_h + self.input_h
        self.input_y = self.top_h
        self.input_win = None

        # Create the top window
        if self.max_y > self.top_h + self.bottom_h:
            self.top_win = self.window.subwin(self.top_h, self.max_x, 0, 0)
            self.top_win.bkgd(curses_color_pair["WHITE_ON_NONE"])
        elif self.max_y > self.bottom_h:
            self.top_win = self.window.subwin(self.bottom_y, self.max_x, 0, 0)
            self.top_win.bkgd(curses_color_pair["WHITE_ON_NONE"])
        else:
            self.top_win = None
        
        # Create the middle window
        if self.middle_h > 1:
            self.middle_win = self.window.subwin(self.middle_h, self.max_x, self.middle_y, 0)
            self.middle_win.bkgd(curses_color_pair["SKY_ON_NONE"])
            self.middle_win.box()
        else:
            self.middle_win = None

        # Create the bottom window
        self.bottom_win = self.window.subwin(1, self.max_x, self.bottom_y, 0)
        
    def display_top_win(self, data):
        if not self.top_win or self.top_h < 0:
            return

        max_x = self.max_x - 1
        
        # Display info
        info = data.get('info', {})
        max_k = max(len(str(k)) + 1 for k in info.keys())
        max_v = max(len(str(v)) + 1 for v in info.values())
        for y, k in enumerate(itertools.islice(info, self.bottom_y)):

            # Format key
            key = f"{k.capitalize()}: "
            n = max_x - max_k
            if n > 0:
                self.top_win.addnstr(y, 1, key, max_k + len(": "), curses_color_pair["GOLDENROD_ON_NONE"])

            # Format value
            n = max_x - max_k - max_v
            if n > 0:
                self.top_win.addnstr(y, max_k + len(": "), str(info[k]), n, curses_color_pair["WHITE_ON_NONE"])
        
        # Display options
        options = data.get('options', {})
        max_k = max(len(str(k)) + 1 for k in options.keys())
        for y, k in enumerate(itertools.islice(options, self.bottom_y)):
            
            # Format key
            key_str = f"<{k}> "
            n = max_x - max_k - 50
            if n > 0:
                self.top_win.addnstr(y, 50, key_str, n, curses_color_pair["MAGENTA_ON_NONE"] | curses.A_BOLD)

            # Format value
            n = max_x - max_k - max_v - 50
            if n > 0:
                self.top_win.addnstr(y, 50 + max_k + len("> "), str(options[k]), n, curses_color_pair["GRAY_ON_NONE"])
        
        # Display controls
        controls = data.get('controls', {})
        max_k = max(len(str(k)) + 1 for k in controls.keys())
        for y, k in enumerate(itertools.islice(controls, self.bottom_y)):
            
            # Format key
            key_str = f"<{k}> "
            n = max_x - max_k - 70
            if n > 0:
                self.top_win.addnstr(y, 70, key_str, n, curses_color_pair["AZURE_ON_NONE"] | curses.A_BOLD)

            # Format value
            n = max_x - max_k - max_v - 70
            if n > 0:
                self.top_win.addnstr(y, 70 + max_k + len("> "), str(controls[k]), n, curses_color_pair["GRAY_ON_NONE"])
        
        # Display Logo
        for y, line in enumerate(self.LOGO[:self.bottom_y]):
            x = max(self.max_x - len(self.LOGO[0]) - 1, 0)
            self.top_win.addnstr(y, x, line, max_x, curses_color_pair["GOLDENROD_ON_NONE"] | curses.A_BOLD)
    
    def display_middle_win(self, data):
        if not self.middle_win:
            return

        # Display banner
        banner_line = f" {data['name']}s({len(data['contents']) - 1}) "
        banner_1 = f" {data['name']}"
        banner_2 = "("
        banner_3 = "all"
        banner_4 = ")["
        banner_5 = f"{len(data['contents']) - 1}"  # do not count header
        banner_6 = f"] "
        center_x = max(self.max_x // 2 - len(banner_line) // 2 - 2, 0)

        # Colorize banner
        if len(banner_line) < self.max_x - 6:
            self.middle_win.addstr(0, center_x, banner_1, curses_color_pair["CYAN_ON_NONE"] | curses.A_BOLD)
            self.middle_win.addstr(banner_2, curses_color_pair["CYAN_ON_NONE"])
            self.middle_win.addstr(banner_3, curses_color_pair["MAGENTA_ON_NONE"] | curses.A_BOLD)
            self.middle_win.addstr(banner_4, curses_color_pair["CYAN_ON_NONE"])
            self.middle_win.addstr(banner_5, curses_color_pair["WHITE_ON_NONE"] | curses.A_BOLD)
            self.middle_win.addstr(banner_6, curses_color_pair["CYAN_ON_NONE"])

            # Ensure banner is drawn ontop of window box
            self.middle_win.refresh()

        # Display contents
        for y, line in enumerate(data["contents"]):
            if y < self.middle_h - 2:
                max_x_with_box = self.max_x - 4
                self.middle_win.addnstr(y + 1, 2, line, max_x_with_box)
    
    def display_bottom_win(self, data):
        # Display footer
        self.bottom_win.addnstr(0, 1, f" <{data['name'].lower()}> ", self.max_x - 2, curses_color_pair["GOLDENROD_ON_NONE"] | curses.A_REVERSE)

    def display(self, data):
        self.display_top_win(data)
        self.display_middle_win(data)
        self.display_bottom_win(data)

    def get_ch(self):
        return self.window.getch()
    
    def textpad_edit(self, window):
        # Show cursor
        curses.curs_set(1)

        # Minimize ESCAPE delay
        curses.set_escdelay(1)

        input_pad = curses.textpad.Textbox(window, insert_mode=True)

        def validate(ch):
            # Exit input with the escape key
            escape = 27
            if ch == escape:
                ch = curses.ascii.BEL # Control-G
            
            # Delete the character to the left of the cursor
            elif ch in (curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
                ch = curses.KEY_BACKSPACE

            # Exit input to resize windows
            elif ch == curses.KEY_RESIZE:
                ch = curses.ascii.BEL # Control-G

            return ch

        input_pad.edit(validate)
        cmd = input_pad.gather()

        # Hide cursor
        curses.curs_set(0)
        
        # Reset ESCAPE delay
        curses.set_escdelay(1000)

        return cmd.strip()

    def get_input(self, data, prompt = " > "):
        # Set input window height
        self.input_h = 3
        self.max_y, self.max_x = self.window.getmaxyx()
        
        # Shift the middle window downward to make room for the input window
        self.middle_h -= self.input_h
        if self.middle_win and self.middle_h > 1:
            self.middle_win.resize(self.middle_h, self.max_x)
            self.middle_win.mvwin(self.input_y + self.input_h, 0)
            self.middle_win.box()
            self.display_middle_win(data)
            self.middle_win.refresh()
        
        # Create the input window
        result = None
        if self.max_y > self.top_h + self.input_h - 1:
            self.input_win = self.window.subwin(self.input_h, self.max_x, self.input_y, 0)
            self.input_win.bkgd(curses_color_pair["AQUAMARINE_ON_NONE"])
            self.input_win.box()
            self.input_win.addstr(1, 1, prompt)
            self.input_win.refresh()
            
            # Edit and gather user input
            textpad_window = curses.newwin(1, self.max_x - len(prompt) - 2, self.input_y + 1, len(prompt) + 1)
            textpad_window.bkgd(curses_color_pair["PEACOCK_ON_NONE"])
            result = self.textpad_edit(textpad_window)

        # Clear input window
        self.input_win.clear()
        self.input_win = None

        return result

class TopicView(BaseView):
    def __init__(self, window):
        super().__init__(window)

class ConsumerGroupView(BaseView):
    def __init__(self, window):
        super().__init__(window)