from cli.window import MenuWindow, CommandWindow, ContentWindow

import curses

STATIC_TOPICS_CONTENTS = [
    "TOPIC                              PARTITION",
    "_schemas_schemaregistry_confluent  1        ",
    "confluent.connect-configs          1        ",
    "confluent.connect-offsets          25       ",
    "confluent.connect-status           5        "
]

def main():
    try:
        # Initialize screen
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(True)
        
        # Initialize windows
        menu_window = MenuWindow(6, curses.COLS, 0, 0)
        command_window = CommandWindow(3, curses.COLS, 6, 0)
        content_window = ContentWindow(curses.LINES-(6+3), curses.COLS, 6+3, 0)

        # Refresh screen after creating new windows
        stdscr.refresh()

        last_command = None
        banner = "Topic"
        contents = STATIC_TOPICS_CONTENTS
        
        # Run screen
        while True:
            
            # Render windows
            menu_window.render()
            command_window.render()
            content_window.render(banner=banner, contents=contents)

            # Get input ascii character
            ch = stdscr.getch()

            # Handle input command
            command = command_window.handle_input(ch)
            
            # Handle command navigation
            if command in ["topics", "tops", "t"]:
                banner = "topic"

                # Get dynamically
                contents = STATIC_TOPICS_CONTENTS
                last_command = command

            elif command and command not in ["topics", "tops", "t"]:
                banner = "unknown"
                contents = ["Wow, such empty"]
            

            # Handle input for other windows
            menu_window.handle_input(ch)
            content_window.handle_input(ch)

            # Handle resize event
            if ch == curses.KEY_RESIZE:
                # screen
                stdscr.resize()

                # screen windows
                menu_window.resize()
                command_window.resize()
                content_window.resize()
            
            elif ch == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == '__main__':
    main()

    