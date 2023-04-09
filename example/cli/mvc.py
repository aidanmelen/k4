import curses

class Model:
    def __init__(self):
        self.data = []

    def add_data(self, data):
        self.data.append(data)

class BaseView:
    def __init__(self, window):
        self.window = window
        self.window.clear()

        max_y, max_x = self.window.getmaxyx()

        # sub-window height and y-position book-keeping
        top_h = 6
        middle_h = max_y - 8
        bottom_h = 2
        bottom_y = max_y - 2

        if max_y > top_h + bottom_h:
            self.top_win = window.subwin(6, max_x, 0, 0)
            self.top_win.bkgd(curses.color_pair(10) | curses.A_REVERSE)
        elif max_y > bottom_h:
            self.top_win = window.subwin(bottom_y, max_x, 0, 0)
            self.top_win.bkgd(curses.color_pair(10) | curses.A_REVERSE)
        else:
            self.top_win = None
        
        if middle_h > 1:
            self.middle_win = window.subwin(middle_h, max_x, top_h, 0)
            self.middle_win.box()
        else:
            self.middle_win = None

        self.bottom_win = window.subwin(1, max_x, bottom_y, 0)
    
    def handle_resize(self):
        max_y, max_x = self.window.getmaxyx()

        self.window.resize(max_y, max_x)
        self.window.clear()

        # sub-window height and y-position book-keeping
        top_h = 6
        middle_h = max_y - 8
        bottom_h = 2
        bottom_y = max_y - 2

        if self.top_win:
            if max_y > top_h + bottom_h:
                self.top_win.resize(5, max_x)
            elif max_y > bottom_h:
                self.top_win.resize(bottom_y, max_x)

        if self.middle_win:
            if middle_h > 1:
                self.middle_win.resize(middle_h, max_x)
            else:
                self.middle_win.clear()

        self.bottom_win.mvwin(bottom_y, 0)
        self.bottom_win.resize(1, max_x)

    def display_data(self, data):
        raise NotImplementedError

    def get_input(self):
        return self.window.getch()

class TopicView(BaseView):
    def __init__(self, window):
        super().__init__(window)
    
    # def handle_resize(self):
    #     y, x = self.window.getmaxyx()
    #     self.window.resize(y, x)
    #     self.window.clear()

    def display_data(self, data):
        y, x = self.window.getmaxyx()

        # top
        idx = 0
        if y > idx + 2:
            self.top_win.addstr(idx, 1, "first")
        
        idx = 3
        if y > idx + 2:
            self.top_win.addstr(idx, 1, "second")

        # middle
        if self.middle_win:
            self.middle_win.addstr(0, x // 2 - 4, " Topics ")
            # for item in data:
            #     self.middle_win.addstr(1, 1 ,str(item) + "\n")
        
        # bottom
        self.bottom_win.addnstr(0, 1, " <Topic> ".lower(), x - 2, curses.color_pair(10) | curses.A_REVERSE)

    # def get_input(self):
    #     return self.window.getch()

class ConsumerGroupView(BaseView):
    def __init__(self, window):
        super().__init__(window)

    def display_data(self, data):
        y, x = self.window.getmaxyx()

        # top
        idx = 0
        if y > idx + 2:
            self.top_win.addstr(idx, 1, "first")
        
        idx = 3
        if y > idx + 2:
            self.top_win.addstr(idx, 1, "second")

        # middle
        if self.middle_win:
            self.middle_win.addstr(0, x // 2 - 4, " ConsumerGroups ")
            # for item in data:
            #     self.middle_win.addstr(1, 1 ,str(item) + "\n")
        
        # bottom
        self.bottom_win.addnstr(0, 1, " <ConsumerGroup> ".lower(), x - len(" <ConsumerGroup> ") - 1, curses.color_pair(10) | curses.A_REVERSE)

    # def get_input(self):
    #     return self.window.getch()

    # def handle_resize(self):
    #     y, x = self.window.getmaxyx()
    #     self.window.resize(y, x)
    #     self.window.clear()

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
        while True:
            data = self.model.data
            view = self.navigation.get_current_view(self.screen.subwin(0, 0))
            view.display_data(data)
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