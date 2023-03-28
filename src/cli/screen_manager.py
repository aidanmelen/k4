from cli.screen import BaseScreen
from kafka_wrapper.broker import Broker
from kafka_wrapper.topic import Topic
from kafka_wrapper.consumer_group import ConsumerGroup
import curses


STATIC_TOPICS_CONTENTS = [
    "TOPIC                              PARTITION",
    "_schemas_schemaregistry_confluent  1        ",
    "confluent.connect-configs          1        ",
    "confluent.connect-offsets          25       ",
    "confluent.connect-status           5        ",
]


def display(admin_client_config, timeout=10):
    """
    Display the k4 curses screen
    """
    broker_client = Broker(admin_client_config, timeout=timeout)
    topic_client = Topic(admin_client_config, timeout=timeout)
    consumer_group_client = ConsumerGroup(admin_client_config, timeout=timeout)

    current_client = topic_client

    try:
        # Initialize screen and windows
        screen = BaseScreen()

        # Default landing screen
        screen.banner = str(current_client)
        # screen.contents = current_client.list()
        screen.contents = STATIC_TOPICS_CONTENTS
        screen.render()

        command = ""

        # Continuously render screen changes
        while True:

            # Render screen windows
            screen.render()

            # Get input ascii character
            ch = screen.stdscr.getch()

            # Handle input command
            command = screen.command_window.handle_input(ch)

            if command:

                # Refresh content banner
                screen.content_window.erase()
                screen.content_window.window.border()
                screen.content_window.render()

                # Handle navigation
                if command in ["brokers", "bros"]:
                    current_client = broker_client

                elif command in ["topics", "tops"]:
                    current_client = topic_client

                elif command in ["consumergroups", "groups", "grps"]:
                    current_client = consumer_group_client

                elif command in ["quit", "q"]:
                    break

            if ch == 27:  # 27 is the ASCII code for Escape
                break

            screen.banner = str(current_client)
            # screen.contents = current_client.list()
            screen.contents = STATIC_TOPICS_CONTENTS

            # Handle resize event
            if ch == curses.KEY_RESIZE:
                screen.resize()

            # Handle input for other windows
            screen.menu_window.handle_input(ch)
            screen.content_window.handle_input(ch)

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
