from .color import curses_color, curses_color_pair
from .model import *
from .view import *
from .error import K4Error

import curses


class Navigation:
    def __init__(self):
        self.current_focus = "topics"
        self.focus = {
            "topics": (TopicView, TopicModel),
            "consumergroups": (ConsumerGroupView, ConsumerGroupModel),
        }

    def navigate(self, command):
        if command in ("topics", "tops", "t"):
            self.current_focus = "topics"

        elif command in ("consumergroups", "groups", "grps", "g"):
            self.current_focus = "consumergroups"

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

        # Start colors and init color pairs using globals
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

                if ch == ord("b"):
                    self.screen.addstr(100000, 10000, "break")

                if ch == ord(":"):
                    command = view.get_input(model_data)
                    self.navigation.navigate(command)
                    view, model = self.navigation.get_current_focus(self.screen.subwin(0, 0))

                    if command in ("quit", "q"):
                        break

                elif ch == curses.KEY_RESIZE:
                    view.handle_resize()

        except KeyboardInterrupt:
            pass
        except curses.error as ce:
            return K4Error("Curses! Something went wrong!", ce)
        finally:
            self.cleanup()

    def cleanup(self):
        self.screen.clear()
        curses.nocbreak()
        self.screen.keypad(True)
        curses.echo()
        curses.endwin()
