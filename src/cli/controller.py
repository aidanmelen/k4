from confluent_kafka.admin import AdminClient
from .color import curses_color, curses_color_pair
from .model import *
from .view import *
from .error import K4Error

import curses
import time


class Navigation:
    def __init__(self):
        self.current_focus = "topics"
        self.focuses = {
            "topics": {
                "view": TopicView,
                "model": TopicModel,
            },
            # "consumergroups": {
            #     "view": ConsumerGroupView,
            #     "model": ConsumerGroupModel,
            # },
        }

        self.aliases = {
            "brokers": ("broker", "bros", "bro", "brkrs", "brkr", "b"),
            "topics": ("topic", "tops", "top", "t"),
            "consumergroups": (
                "consumers",
                "consumer",
                "cons",
                "con",
                "c",
                "groups",
                "group",
                "grps",
                "grp",
                "g",
                "subscribers",
                "subscriber",
                "subs",
                "sub",
                "s",
            ),
            "aliases": ("alias", "a"),
            "quit": ("Q", "q"),
        }

    def navigate(self, command):
        if command == "brokers" or command in self.aliases["brokers"]:
            self.current_focus = "brokers"

        elif command == "topics" or command in self.aliases["topics"]:
            self.current_focus = "topics"

        elif command == "consumergroups" or command in self.aliases["consumergroups"]:
            self.current_focus = "consumergroups"


    def get_current_focus(self, window, kafka_admin_client):
        view = self.focuses[self.current_focus]["view"](window)
        model = self.focuses[self.current_focus]["model"](kafka_admin_client)
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

    def run(self, kafka_admin_client: AdminClient):
        try:
            # Initialize home screen
            view, model = self.navigation.get_current_focus(self.screen, kafka_admin_client)

            while True:
                view.display(model)

                # handle user input
                ch = view.get_ch()

                # handle user command
                if ch == ord(":"):
                    command = view.get_command(model_data)
                    self.navigation.navigate(command)
                    view, model = self.navigation.get_current_focus(self.screen, kafka_admin_client)

                    if command == "quit" or command in self.navigation.aliases["quit"]:
                        break

                # handle screen resize
                elif ch == curses.KEY_RESIZE:
                    view.handle_resize()

        except KeyboardInterrupt:
            pass
        except Exception as e:
            return K4Error("Curses! Something went wrong!", e)
        finally:
            self.cleanup()

    def cleanup(self):
        self.screen.clear()
        curses.endwin()
