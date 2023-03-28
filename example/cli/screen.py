from cli.screen import BaseScreen

import curses


STATIC_TOPICS_CONTENTS = [
    "TOPIC                              PARTITION",
    "_schemas_schemaregistry_confluent  1        ",
    "confluent.connect-configs          1        ",
    "confluent.connect-offsets          25       ",
    "confluent.connect-status           5        "
]


def main():
    # Initialize screen and windows
    screen = BaseScreen()

    # Default screen
    screen.banner = "Topic"
    screen.contents = STATIC_TOPICS_CONTENTS

    last_command = None

    # Run screen
    while True:
        
        # Render screen windows
        screen.render()

        # Get input ascii character
        ch = screen.stdscr.getch()

        # Handle input command
        command = screen.command_window.handle_input(ch)
        
        # Handle command navigation
        if command in ["topics", "tops", "t"]:
            screen.banner = "Topic"

            # Get dynamically
            screen.contents = STATIC_TOPICS_CONTENTS

            last_command = command

        elif command and command not in ["topics", "tops", "t"]:
            screen.focus = "unknown"
            screen.contents = ["Wow, such empty"]

        # Handle input for other windows
        screen.menu_window.handle_input(ch)
        screen.content_window.handle_input(ch)

        # Handle resize event
        if ch == curses.KEY_RESIZE:
            screen.resize()
        
        elif ch == ord('q'):
            break

if __name__ == '__main__':
    main()
