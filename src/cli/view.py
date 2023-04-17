from .color import curses_color_pair
from curses_wrapper import ScrollManager, textbox

import curses
import curses.textpad
import itertools


class BaseView:
    LOGO = [
        " ____      _____  ",
        "|    | __ /  |  | ",
        "|    |/ //   |  |_",
        "|      </    ^   /",
        "|____|_ \\____   |",
        "       \\/    |__|",
    ]

    # Scroll constants
    UP = -1
    DOWN = 1

    def __init__(self, window):
        # Initialize and clear the main window
        self.window = window
        self.window.bkgd(curses_color_pair["WHITE_ON_BLACK"])

        # Initialize scroll manager
        self.scroll_manager = ScrollManager()

        self.handle_resize()

    def handle_resize(self):
        self.window.clear()

        # Set window height and y-position book-keeping
        self.max_y, self.max_x = self.window.getmaxyx()
        self.top_h = min(len(self.LOGO), self.max_y)
        self.command_h = 0
        self.bottom_h = 2
        self.bottom_y = self.max_y - self.bottom_h
        self.middle_h = self.max_y - self.top_h - self.command_h - self.bottom_h
        self.middle_y = self.top_h + self.command_h
        self.contents_h = self.middle_h - 2
        self.contents_w = self.max_x - 4
        self.contents_y = self.middle_y + 1
        self.contents_x = 2
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
            self.middle_win.bkgd(curses_color_pair["SKY_ON_BLACK"])
            self.middle_win.box()
        else:
            self.middle_win = None

        # Create the scroll contents derived window
        if self.contents_h > 0:
            self.contents_win = self.middle_win.derwin(self.contents_h, self.contents_w, 1, 2)
            self.contents_win.bkgd(curses_color_pair["SKY_ON_BLACK"])
            self.scroll_manager.init(self.contents_win)
        else:
            self.contents_win = None

        # Create the bottom window
        self.bottom_win = self.window.subwin(1, self.max_x, self.bottom_y, 0)

    def chunk_dict(self, d, chunk_size=6):
        """Split a dictionary into a list of dictionaries, with each sub-dictionary containing at most chunk_size key-value pairs."""
        chunks = []
        chunk = {}
        for k, v in d.items():
            if len(chunk) == chunk_size:
                chunks.append(chunk)
                chunk = {}
            chunk[k] = v
        if chunk:
            chunks.append(chunk)
        return chunks

    def display_top_win(self, data):
        if not self.top_win or self.top_h < 0:
            return

        max_x = self.max_x - 1

        # Display info
        info = data.get("info", {})
        max_k = max(len(str(k)) + 1 for k in info.keys())
        max_v = max(len(str(v)) + 1 for v in info.values())
        for y, k in enumerate(itertools.islice(info, self.bottom_y)):

            # Format key
            key = f"{k.capitalize()}: "
            n = max_x - max_k
            if n > 0:
                self.top_win.addnstr(
                    y, 1, key, max_k + len(": "), curses_color_pair["GOLDENROD_ON_BLACK"]
                )

            # Format value
            n = max_x - max_k - max_v
            if n > 0:
                self.top_win.addnstr(
                    y, max_k + len(": "), str(info[k]), n, curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD
                )

        # Display domains
        domains_x = 50
        chunked_domains = self.chunk_dict(data.get("domains", {}))
        for domains in chunked_domains:
            max_k = max(len(str(k)) + 1 for k in domains.keys())
            max_v = max(len(str(v)) + 1 for v in domains.values())
            for y, k in enumerate(itertools.islice(domains, self.bottom_y)):

                # Format key
                key_str = f"<{k}> "
                n = max_x - max_k - domains_x
                if n > 0:
                    self.top_win.addnstr(
                        y,
                        domains_x,
                        key_str,
                        n,
                        curses_color_pair["MAGENTA_ON_BLACK"] | curses.A_BOLD,
                    )

                # Format value
                n = max_x - max_k - max_v - domains_x
                if n > 0:
                    self.top_win.addnstr(
                        y,
                        domains_x + max_k + len("> "),
                        str(domains[k]),
                        n,
                        curses_color_pair["GRAY_ON_BLACK"],
                    )

            # shift next column
            domains_x += max_k + len("<> ") + max_v + 1

        # Display controls
        controls_x = domains_x
        chunked_controls = self.chunk_dict(data.get("controls", {}))
        for controls in chunked_controls:
            max_k = max(len(str(k)) + 1 for k in controls.keys())
            max_v = max(len(str(v)) + 1 for v in controls.values())
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
                        curses_color_pair["AZURE_ON_BLACK"] | curses.A_BOLD,
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
            controls_x += max_k + len("<> ") + max_v + 1

        # Display Logo
        for y, line in enumerate(self.LOGO[: self.bottom_y]):
            x = max(self.max_x - len(self.LOGO[0]) - 1, 0)
            self.top_win.addnstr(
                y, x, line, max_x, curses_color_pair["GOLDENROD_ON_BLACK"] | curses.A_BOLD
            )

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
            self.middle_win.addstr(
                0, center_x, banner_1, curses_color_pair["CYAN_ON_BLACK"] | curses.A_BOLD
            )
            self.middle_win.addstr(banner_2, curses_color_pair["CYAN_ON_BLACK"])
            self.middle_win.addstr(banner_3, curses_color_pair["MAGENTA_ON_BLACK"] | curses.A_BOLD)
            self.middle_win.addstr(banner_4, curses_color_pair["CYAN_ON_BLACK"])
            self.middle_win.addstr(banner_5, curses_color_pair["WHITE_ON_BLACK"] | curses.A_BOLD)
            self.middle_win.addstr(banner_6, curses_color_pair["CYAN_ON_BLACK"])

            # Ensure banner is drawn above of window box
            self.middle_win.refresh()

    def display_content_win(self, data):
        if self.contents_win:
            self.scroll_manager.display(data["contents"])

    def display_bottom_win(self, data):
        # Display footer
        self.bottom_win.addnstr(
            0,
            1,
            f" <{data['name'].lower()}> ",
            self.max_x - 2,
            curses_color_pair["GOLDENROD_ON_BLACK"] | curses.A_REVERSE,
        )

    def display(self, data):
        self.display_top_win(data)
        self.display_middle_win(data)
        self.display_content_win(data)
        self.display_bottom_win(data)

    def get_ch(self):
        ch = self.window.getch()
        self.scroll_manager.handle_input(ch)
        return ch

    def get_command(self, data, prompt=" > "):
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
            self.display_middle_win(data)

        # Create the command window
        result = None
        if self.max_y > self.top_h + self.command_h - 1:
            self.command_win = self.window.subwin(self.command_h, self.max_x, self.command_y, 0)
            self.command_win.bkgd(curses_color_pair["AQUAMARINE_ON_BLACK"])
            self.command_win.box()
            self.command_win.addstr(1, 1, prompt)
            self.command_win.refresh()

            # Edit and gather user command
            textbox_win = curses.newwin(
                1, self.max_x - len(prompt) - 2, self.command_y + 1, len(prompt) + 1
            )
            textbox_win.bkgd(curses_color_pair["PEACOCK_ON_BLACK"])
            result = textbox.edit(textbox_win)

        # Clear command window
        self.command_win.clear()
        self.command_win = None

        return result


class TopicView(BaseView):
    def __init__(self, window):
        super().__init__(window)


class ConsumerGroupView(BaseView):
    def __init__(self, window):
        super().__init__(window)
