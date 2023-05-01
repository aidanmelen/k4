from .color import curses_color_pair
from curses_wrapper import ScrollManager, textbox
from .timer import Timer
from . import helper

import curses
import curses.textpad
import itertools
import textwrap


class BaseView:
    LOGO = [
        " ____      _____  ",
        "|    | __ /  |  | ",
        "|    |/ //   |  |_",
        "|      </    ^   /",
        "|____|_ \\____   |",
        "       \\/    |__|",
    ]

    def __init__(self, window):
        # Initialize and clear the main window
        self.window = window
        self.window.bkgd(curses_color_pair["WHITE_ON_BLACK"])

        # Timer used to refresh data
        self.timer = Timer()

        # Initialize scroll manager
        self.scroll_manager = ScrollManager()

        self.handle_resize()

    def handle_resize(self):
        self.window.clear()

        # Set window height and y-position book-keeping
        self.max_y, self.max_x = self.window.getmaxyx()
        self.top_h = min(len(self.LOGO) + 1, self.max_y)
        self.command_h = 0
        self.bottom_h = 2
        self.bottom_y = self.max_y - self.bottom_h
        self.middle_h = self.max_y - self.top_h - self.command_h - self.bottom_h
        self.middle_y = self.top_h + self.command_h
        self.middle_scroll_h = self.middle_h - 2
        self.middle_scroll_w = self.max_x - 4  # 2 box and 1 left indent.
        self.middle_scroll_y = self.middle_y + 1
        self.middle_scroll_x = 2
        self.command_y = self.top_h
        self.command_win = None

        # Create the top window
        if self.max_y > 0:
            self.top_win = self.window.subwin(self.top_h, self.max_x, 0, 0)
            self.top_win.bkgd(curses_color_pair["WHITE_ON_BLACK"])
        else:
            self.top_win = None

        # Create the middle window
        if self.middle_h > 1:
            self.middle_win = self.window.subwin(self.middle_h, self.max_x, self.middle_y, 0)
            self.middle_win.bkgd(curses_color_pair["LIGHT_SKY_BLUE_ON_BLACK"])
            self.middle_win.box()
        else:
            self.middle_win = None

        # Create the scroll contents derived window
        if self.middle_scroll_h > 0:
            self.middle_scroll_win = self.middle_win.derwin(
                self.middle_scroll_h, self.middle_scroll_w, 1, 2
            )
            self.middle_scroll_win.bkgd(curses_color_pair["LIGHT_SKY_BLUE_ON_BLACK"])
            self.scroll_manager.init(self.middle_scroll_win, cursor_start_position=1, has_fixed_header_line=True)
        else:
            self.middle_scroll_win = None

        # Create the bottom window
        self.bottom_win = self.window.subwin(1, self.max_x, self.bottom_y, 0)

    def display_top_win(self, model):
        if not self.top_win or self.top_h < 0:
            return

        max_x = self.max_x - 1

        # Display info
        model_info = model.info
        max_k = max(len(str(k)) + 1 for k in model_info.keys())
        max_v = max(len(str(v)) + 1 for v in model_info.values())
        for y, k in enumerate(itertools.islice(model_info, self.bottom_y)):

            # Format key
            key = f"{k.capitalize()}: "
            n = max_x - max_k
            if n > 0:
                self.top_win.addnstr(
                    y,
                    1,
                    key,
                    max_k + len(": "),
                    curses_color_pair["ORANGE_ON_BLACK"],
                )

            # Format value
            n = max_x - max_k - 5
            if n > 0:
                shortened_model_info_key = helper.shorten(str(model_info[k]), width=39, placeholder='…')
                self.top_win.addnstr(
                    y,
                    max_k + len(": "),
                    shortened_model_info_key,
                    n,
                    curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD,
                )

        # Display namespaces
        namespaces_x = 50
        namespaces_chunks = helper.chunk_dict(model.namespaces)
        for namespaces in namespaces_chunks:
            max_k = max(len(str(k)) + len(" ") for k in namespaces.keys())
            max_v = max(len(str(v)) + len(" ") for v in namespaces.values())
            for y, k in enumerate(itertools.islice(namespaces, self.bottom_y)):

                # Format key
                key_str = f"<{k}> "
                n = max_x - max_k - namespaces_x
                if n > 0:
                    self.top_win.addnstr(
                        y,
                        namespaces_x,
                        key_str,
                        n,
                        curses_color_pair["FUCHSIA_ON_BLACK"] | curses.A_BOLD,
                    )

                # Format value
                n = max_x - max_k - namespaces_x - len(self.LOGO[0])
                if n > 0:
                    self.top_win.addnstr(
                        y,
                        namespaces_x + max_k + len("> "),
                        str(namespaces[k]),
                        n,
                        curses_color_pair["GRAY_ON_BLACK"],
                    )

            # shift next column
            namespaces_x += max_k + max_v + len(">  ")

        # Display controls
        controls_x = namespaces_x
        chunked_controls = helper.chunk_dict(model.get_sorted_controls())
        for controls in chunked_controls:
            max_k = max(len(str(k)) + len(" ") for k in controls.keys())
            max_v = max(len(str(v)) + len(" ") for v in controls.values())
            for y, k in enumerate(itertools.islice(controls, self.bottom_y)):

                # Format key
                key_str = f"<{k}> "
                n = max_x - max_k - controls_x
                if n > 0:
                    self.top_win.addnstr(
                        y,
                        controls_x,
                        key_str,
                        n,
                        curses_color_pair["DODGER_BLUE_ON_BLACK"] | curses.A_BOLD,
                    )

                # Format value
                n = max_x - max_k - max_v - controls_x
                if n > 0:
                    self.top_win.addnstr(
                        y,
                        controls_x + max_k + len("> "),
                        str(controls[k]),
                        n,
                        curses_color_pair["GRAY_ON_BLACK"],
                    )

            # shift next column
            controls_x += max_k + max_v + len(">  ")

        # Display Logo
        for y, line in enumerate(self.LOGO[: self.bottom_y]):
            x = max(self.max_x - len(self.LOGO[0]) - 1, 0)
            self.top_win.addnstr(
                y, x, line, max_x, curses_color_pair["ORANGE_ON_BLACK"] | curses.A_BOLD
            )

    def display_middle_win(self, model):
        if not self.middle_win:
            return

        # Display banner
        banner_line = f" {model.name}s({len(model.contents) - 1}) "
        banner_1 = f" {model.name}s"
        banner_2 = "("
        banner_3 = "all"
        banner_4 = ")["
        banner_5 = f"{len(model.contents) - 1}"  # do not count header
        banner_6 = f"] "
        center_x = max(self.max_x // 2 - len(banner_line) // 2 - 2, 0)

        # Colorize banner
        if len(banner_line) < self.max_x - 6:
            self.middle_win.addstr(
                0, center_x, banner_1, curses_color_pair["CYAN_ON_BLACK"] | curses.A_BOLD
            )
            self.middle_win.addstr(banner_2, curses_color_pair["CYAN_ON_BLACK"])
            self.middle_win.addstr(banner_3, curses_color_pair["FUCHSIA_ON_BLACK"] | curses.A_BOLD)
            self.middle_win.addstr(banner_4, curses_color_pair["CYAN_ON_BLACK"])
            self.middle_win.addstr(banner_5, curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD)
            self.middle_win.addstr(banner_6, curses_color_pair["CYAN_ON_BLACK"])

            # Ensure banner is drawn above of window box
            self.middle_win.refresh()

    def display_middle_scroll_win(self, model):
        if self.middle_scroll_win:

            scroll_manager_items = []
            for y, line in enumerate(model.contents):

                # Colorize header line
                if y == 0:
                    item = {
                        "line": line,
                        "color_pair_id": curses_color_pair["WHITE_ON_BLACK"],
                    }
                    scroll_manager_items.append(item)

                # Colorize BLACK lines
                else:
                    item = {
                        "line": line,
                        "color_pair_id": curses_color_pair["LIGHT_SKY_BLUE_ON_BLACK"],
                    }
                    scroll_manager_items.append(item)

            self.scroll_manager.items = scroll_manager_items
            self.scroll_manager.display()

    def display_bottom_win(self, model):
        # Display footer
        self.bottom_win.addnstr(
            0, 1, f" <{model.name.lower()}> ", self.max_x - 2,  curses_color_pair["ORANGE_ON_BLACK"]
            | curses.A_REVERSE | curses.A_BOLD
        )

    def display(self, model):
        self.display_top_win(model)
        self.display_middle_win(model)
        self.display_middle_scroll_win(model)
        self.display_bottom_win(model)

    def select_item_line(self):
       return self.scroll_manager.select_item_line()
    
    def get_ch(self):
        ch = self.window.getch()
        self.scroll_manager.handle_input(ch)
        return ch

    def get_command(self, model, prompt=" > "):
        # Set command window height
        self.command_h = 3
        self.max_y, self.max_x = self.window.getmaxyx()

        # Shift the middle window downward to make room for the command window
        self.middle_h -= self.command_h
        if self.middle_win and self.middle_h > 1:
            # Content box/banner
            self.middle_win.resize(self.middle_h, self.max_x)
            self.middle_win.mvwin(self.command_y + self.command_h, 0)
            self.middle_win.box()
            self.middle_win.refresh()
            self.display_middle_win(model)

        # Create the command window
        result = None
        if self.max_y > self.top_h + self.command_h - 1:
            self.command_win = self.window.subwin(self.command_h, self.max_x, self.command_y, 0)
            self.command_win.bkgd(curses_color_pair["CADET_BLUE_ON_BLACK"])
            self.command_win.box()
            self.command_win.addstr(1, 1, prompt)
            self.command_win.refresh()

            # Edit and gather user command
            textbox_win = curses.newwin(
                1, self.max_x - len(prompt) - 2, self.command_y + 1, len(prompt) + 1
            )
            textbox_win.bkgd(curses_color_pair["CADET_BLUE_ON_BLACK"])
            result = textbox.edit(textbox_win)

        # Clear command window
        self.command_win.clear()
        self.command_win = None

        return result


class TopicView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.show_internal = False

    def get_ch(self):
        ch = super().get_ch()

        if ch == ord("c"):
            pass
        elif ch == 67: # shift-c
            self.window.addstr(self.max_y -1, self.max_x // 2, 'shift-c')
        elif ch == curses.ascii.EOT: # ctrl-d
            self.window.addstr(self.max_y -1, self.max_x // 2, 'ctrl-d')
        elif ch == ord("d"):
            pass
        elif ch == ord("e"):
            pass
        elif ch == ord("?"):
            pass
        elif ch == ord("i"):
            self.show_internal = not self.show_internal
            self.window.addstr(self.max_y -1, self.max_x // 2, 'i')
        elif ch == ord("P"):
            pass

        return ch


class ConsumerGroupView(BaseView):
    def __init__(self, window):
        super().__init__(window)
