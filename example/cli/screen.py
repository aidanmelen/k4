from cli.screen import Screen

import curses


def main():
    try:
        screen = Screen()

        while True:
            screen.render()
            ch = screen.stdscr.getch()
            command = screen.command_window.handle_input(ch)
            
            if command in ["topics", "tops", "t"]:
                screen.focus = "topics"

                # TODO get dynamically
                screen.contents = [
                    "TOPIC                              PARTITION",
                    "_schemas_schemaregistry_confluent  1        ",
                    "confluent.connect-configs          1        ",
                    "confluent.connect-offsets          25       ",
                    "confluent.connect-status           5        "
                ]

            screen.menu_window.handle_input(ch)
            screen.content_window.handle_input(ch)

            if ch == curses.KEY_RESIZE:
                screen.resize()
            
            elif ch == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == '__main__':
    main()

    