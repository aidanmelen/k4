from curses_wrapper import textbox
import curses

def main(stdscr):

    ch = 0
    while ch != ord("q"):
        max_y, max_x = stdscr.getmaxyx()
        input_h = 3
        input_y = max_y // 2
        prompt = " > "

        # Create the input window
        input_win = stdscr.subwin(3, max_x, input_y, 0)
        input_win.box()
        input_win.addstr(1, 1, prompt)
        input_win.refresh()

        # Edit and gather user input
        textbox_win = curses.newwin(1, max_x - len(prompt) - 2, input_y + 1, len(prompt) + 1)

        result = textbox.edit(textbox_win)

        stdscr.addstr(0,0, result)

        ch = stdscr.getch()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass