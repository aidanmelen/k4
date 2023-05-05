from typing import Type, Tuple, Dict
from confluent_kafka.admin import AdminClient
from .color import curses_color, curses_color_pair
from .model import *
from .view import *
from .error import K4Error

import asyncio
import curses
import time

class Navigation:
    def __init__(self) -> None:
        self.current_focus = "topics"
        self.focuses = {
            "topics": {
                "view": TopicView,
                "model": TopicModel,
            },
            "consumergroups": {
                "view": ConsumerGroupView,
                "model": ConsumerGroupModel,
            },
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

    def navigate(self, command: str) -> None:
        if command == "brokers" or command in self.aliases["brokers"]:
            self.current_focus = "brokers"

        elif command == "topics" or command in self.aliases["topics"]:
            self.current_focus = "topics"

        elif command == "consumergroups" or command in self.aliases["consumergroups"]:
            self.current_focus = "consumergroups"

    def get_current_focus(self, window: Type[curses.window], kafka_admin_client_config) -> Tuple[Any, Any]:
        view = self.focuses[self.current_focus]["view"](window)
        model = self.focuses[self.current_focus]["model"](kafka_admin_client_config)
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
        curses_color.init_colors(
            color_names=[
                "BLACK",
                "CADET_BLUE",
                "CYAN",
                "DODGER_BLUE",
                "ORANGE",
                "ORANGE_RED",
                "GRAY",
                "LIGHT_SKY_BLUE",
                "FUCHSIA",
                "MEDIUM_PURPLE",
                "RED",
                "STEEL_BLUE",
                "WHITE",
            ]
        )
        curses_color_pair.init_pairs(bg_color_name="BLACK")

        self.navigation = Navigation()

    def run(self, kafka_admin_client_config: Dict[str, str]) -> None:
        try:
            # Initialize home screen
            view, model = self.navigation.get_current_focus(self.screen, kafka_admin_client_config)
            model.update_input(view.input)
            asyncio.run(model.refresh())

            while True:
                asyncio.run(model.refresh(wait_seconds=10))
                view.display(model)

                line = view.select_item_line().split(" ")[0]

                # Handle user input
                ch = view.get_ch()

                # Handle user command
                if ch == ord(":"):
                    command = view.get_command(model)
                    self.navigation.navigate(command)
                    
                    view, model = self.navigation.get_current_focus(self.screen, kafka_admin_client_config)
                    asyncio.run(model.refresh())

                    if command == "quit" or command in self.navigation.aliases["quit"]:
                        break
                
                # Handle user controls
                elif ch in [ord(k[-1]) for k in model.controls.keys()]:
                    view.top_win.erase()
                    model.update_input(view.input)
                    view.display(model)
                    asyncio.run(model.refresh())

                # Handle screen resize
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
