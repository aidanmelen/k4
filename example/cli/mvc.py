from curses_wrapper.color import CursesColor, CursesColorPair

import curses
import curses.textpad
import textwrap

class BaseModel:
    def __init__(self):
        self._data = {}

    @property
    def data(self):
        raise NotImplemented

class TopicModel(BaseModel):
    @property
    def data(self):
        return {
            "name": "Topic",
            "info": {
                "context": None,
                "cluster": None,
                "user": None
            },
            "options": {
                "1": "internal",
            },
            "controls": {
                "ctrl-d": "Delete",
                "d": "Describe",
                "e": "Edit",
                "?": "Help"
            },
            "contents": [
                "TOPIC                              PARTITION",
                "_schemas_schemaregistry_confluent  1        ",
                "confluent.connect-configs          1        ",
                "confluent.connect-offsets          25       ",
                "confluent.connect-status           5        "
            ]
        }

class ConsumerGroupModel(BaseModel):
    @property
    def data(self):
        return {
            "name": "ConsumerGroup",
            "info": {
                "context": None,
                "cluster": None,
                "user": None
            },
            "options": {
                "1": "only_stable",
                "2": "only_high_level",
            },
            "controls": {
                "ctrl-d": "Delete",
                "d": "Describe",
                "e": "Edit",
                "?": "Help"
            },
            "contents": [
                "GROUP                              TOPIC                                                                                          PARTITION    CURRENT-OFFSET    LOG-END-OFFSET    LAG    CONSUMER-ID                                                                                                                                 HOST        CLIENT-ID",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MetricsAggregateStore-repartition                             9            -                 20404             20404  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-ONE_MINUTE-repartition     9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-THREE_HOURS-repartition    9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer"
            ]
        }


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
        self.window.bkgd(curses_color_pair["WHITE_ON_BLACK"])
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
            self.top_win.bkgd(curses_color_pair["WHITE_ON_BLACK"])
        elif self.max_y > self.bottom_h:
            self.top_win = self.window.subwin(self.bottom_y, self.max_x, 0, 0)
            self.top_win.bkgd(curses_color_pair["WHITE_ON_BLACK"])
        else:
            self.top_win = None
        
        # Create the middle window
        if self.middle_h > 1:
            self.middle_win = self.window.subwin(self.middle_h, self.max_x, self.middle_y, 0)
            self.middle_win.bkgd(curses_color_pair["SKY_ON_BLACK"])
            self.middle_win.box()
        else:
            self.middle_win = None

        # Create the bottom window
        self.bottom_win = self.window.subwin(1, self.max_x, self.bottom_y, 0)

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
            self.input_win.bkgd(curses_color_pair["AQUAMARINE_ON_BLACK"])
            self.input_win.box()
            self.input_win.addstr(1, 1, prompt)
            self.input_win.refresh()
            
            # Edit and gather user input
            textpad_window = curses.newwin(1, self.max_x - len(prompt) - 2, self.input_y + 1, len(prompt) + 1)
            textpad_window.bkgd(curses_color_pair["PEACOCK_ON_BLACK"])
            result = self.textpad_edit(textpad_window)

        # Clear input window
        self.input_win.clear()
        self.input_win = None

        return result
        
    def display_top_win(self, data):
        if not self.top_win or self.top_h < 0:
            return

        max_x = self.max_x - 1
        
        # Display info
        info = data['info']
        for y, k in enumerate(list(info.keys())[:self.bottom_y]):
            key = f"{k.capitalize()}: "
            n = max(max_x - len(key) - len(self.LOGO[0]), 0)
            if n > 0:
                self.top_win.addnstr(y, 1, key, max_x, curses_color_pair["GOLDENROD_ON_BLACK"])
                self.top_win.addnstr(y, 1 + len(key), str(info[k]), n, curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD)
        
        # Display options
        options = data['options']
        for y, k in enumerate(list(options.keys())[:self.bottom_y]):
            
            # Format key
            key_str = f"<{k}> "
            n = max_x - 40
            if n > 0:
                self.top_win.addnstr(y, 40, key_str, n, curses_color_pair["MAGENTA_ON_BLACK"] | curses.A_BOLD)

            # Format value
            n -= len(key_str)
            if n > 0:
                self.top_win.addnstr(y, 40 + len(key_str), str(options[k]), n, curses_color_pair["GRAY_ON_BLACK"])
        
        # Display controls
        controls = data['controls']
        for y, k in enumerate(list(controls.keys())[:self.bottom_y]):

            # Format key
            key_str = f"<{k}> "
            if self.max_x - 60 > 0:
                self.top_win.addnstr(y, 60, key_str, max_x - 60, curses_color_pair["AZURE_ON_BLACK"] | curses.A_BOLD)

            # Format value
            n = max_x - 60 - len(key_str)
            if n > 0:
                self.top_win.addnstr(y, 60 + len(key_str), str(controls[k]), n, curses_color_pair["GRAY_ON_BLACK"])

        # Display Logo
        for y, line in enumerate(self.LOGO[:self.bottom_y]):
            x = max(self.max_x - len(self.LOGO[0]) - 1, 0)
            self.top_win.addnstr(y, x, line, max_x, curses_color_pair["GOLDENROD_ON_BLACK"] | curses.A_BOLD)
    
    def display_middle_win(self, data):
        if not self.middle_win:
            return

        # Display banner
        banner_line = f" {data['name']}s({len(data['contents'])}) "
        x = max(self.max_x // 2 - len(banner_line) // 2, 0)
        self.middle_win.addnstr(0, x, banner_line, self.max_x - 2)

        # Display contents
        for y, line in enumerate(data["contents"]):
            if y < self.middle_h - 2:
                max_x_with_box = self.max_x - 4
                self.middle_win.addnstr(y + 1, 2, line, max_x_with_box)
    
    def display_bottom_win(self, data):
        # Display footer
        self.bottom_win.addnstr(0, 1, f" <{data['name'].lower()}> ", self.max_x - 2, curses_color_pair["GOLDENROD_ON_BLACK"] | curses.A_REVERSE)

    def display(self, data):
        self.display_top_win(data)
        self.display_middle_win(data)
        self.display_bottom_win(data)

    def get_ch(self):
        return self.window.getch()

class TopicView(BaseView):
    def __init__(self, window):
        super().__init__(window)

class ConsumerGroupView(BaseView):
    def __init__(self, window):
        super().__init__(window)

class Navigation:
    def __init__(self):
        self.current_focus = 'topics'
        self.focus = {
            'topics': (TopicView, TopicModel),
            'consumergroups': (ConsumerGroupView, ConsumerGroupModel)
        }

    def navigate(self, command):
        if command in ("topics", "tops", "t"):
            self.current_focus = 'topics'

        elif command in ("consumergroups", "groups", "grps", "g"):
            self.current_focus = 'consumergroups'

    def get_current_focus(self, window):
        view = self.focus[self.current_focus][0](window)
        model = self.focus[self.current_focus][1]()
        return view, model

class Controller:
    def __init__(self):
        self.screen = curses.initscr()

        # Setup screen
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # Start colors and init color pairs
        global curses_color_pair
        curses_color = CursesColor()
        curses_color_pair = CursesColorPair(curses_color)
        curses_color.start_color()
        curses_color.init_colors()
        curses_color_pair.init_pairs(bg_color_name="BLACK")

        self.navigation = Navigation()

    def run(self):
        try:
            view, model = self.navigation.get_current_focus(self.screen.subwin(0, 0))

            while True:
                model_data = model.data
                
                view.display(model_data)

                # handle user input
                ch = view.get_ch()

                if ch == ord(':'):
                    command = view.get_input(model_data)
                    self.navigation.navigate(command)
                    view, model = self.navigation.get_current_focus(self.screen.subwin(0, 0))
                    
                    if command in ('quit', 'q'):
                        break
                
                elif ch == curses.KEY_RESIZE:
                    view.handle_resize()

        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        curses.nocbreak()
        self.screen.keypad(True)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    controller = Controller()
    controller.run()