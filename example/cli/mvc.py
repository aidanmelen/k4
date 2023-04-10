import curses
import textwrap


MOCK_TOPIC_DATA = {
    "name": "topic",
    "content": [
        "TOPIC                              PARTITION",
        "_schemas_schemaregistry_confluent  1        ",
        "confluent.connect-configs          1        ",
        "confluent.connect-offsets          25       ",
        "confluent.connect-status           5        "
    ]
}

MOCK_CONSUMER_GROUP_DATA = {
    "name": "topic",
    "content": [
        "CONSUMER-GROUP                     PARTITION",
        "_schemas_schemaregistry_confluent  1        ",
        "confluent.connect-configs          1        ",
        "confluent.connect-offsets          25       ",
        "confluent.connect-status           5        "
    ]
}

class Model:
    def __init__(self):
        self.data = []

    def add_data(self, data):

        assert "name" in data
        assert "content" in data


        self.data.append(data)

class BaseView:
    LOGO = [
        ' ____      _____   ',
        '|    | __ /  |  |  ',
        '|    |/ //   |  |_ ',
        '|      </    ^   / ',
        '|____|_ \\____   | ',
        '       \\/    |__| '
    ]

    def __init__(self, window):
        self.window = window
        self.window.clear()

        # sub-window height and y-position book-keeping
        self.max_y, self.max_x = self.window.getmaxyx()
        self.top_h = 6
        self.middle_h = self.max_y - 8
        self.bottom_h = 2
        self.bottom_y = self.max_y - 2

        if self.max_y > self.top_h + self.bottom_h:
            self.top_win = window.subwin(6, self.max_x, 0, 0)
            self.top_win.bkgd(curses.color_pair(10) | curses.A_REVERSE)
        elif self.max_y > self.bottom_h:
            self.top_win = window.subwin(self.bottom_y, self.max_x, 0, 0)
            self.top_win.bkgd(curses.color_pair(10) | curses.A_REVERSE)
        else:
            self.top_win = None
        
        if self.middle_h > 1:
            self.middle_win = window.subwin(self.middle_h, self.max_x, self.top_h, 0)
            self.middle_win.box()
        else:
            self.middle_win = None

        self.bottom_win = window.subwin(1, self.max_x, self.bottom_y, 0)
    
    def handle_resize(self):
        # update sub-window height and y-position book-keeping
        self.max_y, self.max_x = self.window.getmaxyx()
        self.middle_h = self.max_y - 8
        self.bottom_y = self.max_y - 2

        self.window.resize(self.max_y, self.max_x)
        self.window.clear()

        if self.top_win:
            if self.max_y > self.top_h + self.bottom_h:
                self.top_h = 5
                self.top_win.resize(self.top_h, self.max_x)
            elif self.max_y > self.bottom_h:
                self.top_h = self.bottom_y
                self.top_win.resize(self.top_h, self.max_x)
                self.top_win.clear()
            else:
                self.top_win.clear()

        if self.middle_win:
            if self.middle_h > 1:
                self.middle_win.resize(self.middle_h, self.max_x)
            else:
                self.middle_win.clear()

        self.bottom_win.mvwin(self.bottom_y, 0)
        self.bottom_win.resize(1, self.max_x)

    def display_top_win(self, data):
        if self.top_win:
            # logo
            for y, line in enumerate(self.LOGO):
                x = max(self.max_x - len(self.LOGO[0]), 0)
                
                if y < min(self.top_h, self.bottom_y - 1):
                    self.top_win.addnstr(max(y, 0), x, line[:self.max_x], self.max_x - 1, curses.A_BOLD)

    
    def display_middle_win(self, data):
        if self.middle_win:
            # banner
            banner_line = f" {data['name'].capitalize()}s "
            self.middle_win.addnstr(0, self.max_x // 2 - len(banner_line) // 2, banner_line, self.max_x - 2)

            # content
            for y, line in enumerate(data["content"]):
                if y < self.middle_h - 2:
                    self.middle_win.addnstr(y + 1, 1, line, self.max_x - 2) # adjust for window box edges
    
    def display_bottom_win(self, data):
        self.bottom_win.addnstr(0, 1, f" <{data['name'].lower()}> ", self.max_x - 2, curses.color_pair(10) | curses.A_REVERSE)

    def display(self, data):
        self.display_top_win(data)
        self.display_middle_win(data)
        self.display_bottom_win(data)

    def get_input(self):
        return self.window.getch()

class TopicView(BaseView):
    def __init__(self, window):
        super().__init__(window)
    
    # def display(self, data):
    #     super().display(data)

    # def get_input(self):
    #     input = super().get_input(data)
    #     return input

class ConsumerGroupView(BaseView):
    def __init__(self, window):
        super().__init__(window)

class Navigation:
    def __init__(self):
        self.current_view = 'TopicView'
        self.views = {
            'TopicView': TopicView,
            'ConsumerGroupView': ConsumerGroupView
        }

    def navigate(self, key):
        if key == ord('1'):
            self.current_view = 'TopicView'
        elif key == ord('2'):
            self.current_view = 'ConsumerGroupView'

    def get_current_view(self, window):
        return self.views[self.current_view](window)

class Controller:
    def __init__(self):
        self.model = Model()
        self.screen = curses.initscr()

        # Setup screen
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # Start colors
        curses.start_color()
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.navigation = Navigation()

    def run(self):

        # initialize model data
        self.model.data = MOCK_TOPIC_DATA

        while True:
            data = self.model.data
            view = self.navigation.get_current_view(self.screen.subwin(0, 0))
            view.display(data)
            user_input = view.get_input()
            if user_input == ord('q'):
                break
            elif user_input == curses.KEY_RESIZE:
                view.handle_resize()
            else:
                self.navigation.navigate(user_input)
                self.model.add_data(user_input)

        self.cleanup()

    def cleanup(self):
        curses.nocbreak()
        self.screen.keypad(True)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    controller = Controller()
    controller.run()