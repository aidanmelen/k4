import curses
import curses.textpad


KEY_ESCAPE = 27


def validate(ch: int) -> int:
    """
    Validate character in a curses textbox and return the valid character.

    Args:
        ch (int): The character to be validated.

    Returns:
        int: The validated character.
    """
    # Exit input with the escape key
    if ch == KEY_ESCAPE:
        ch = curses.ascii.BEL  # Control-G

    # Delete the character to the left of the cursor
    elif ch in (curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
        ch = curses.KEY_BACKSPACE

    # Exit input to resize windows
    elif ch == curses.KEY_RESIZE:
        ch = curses.ascii.BEL  # Control-G

    return ch


def edit(window: curses.window) -> str:
    """
    Edit text in a curses window and return the edited text.

    Args:
        window (curses.window): The curses window to edit text in.

    Returns:
        str: The edited text after stripping any leading or trailing whitespace.
    """
    # Show cursor
    curses.curs_set(1)

    # Minimize KEY_ESCAPE delay
    curses.set_escdelay(1)

    input_pad = curses.textpad.Textbox(window, insert_mode=True)

    input_pad.edit(validate)
    cmd = input_pad.gather()

    # Hide cursor
    curses.curs_set(0)

    # Reset KEY_ESCAPE delay
    curses.set_escdelay(1000)

    return cmd.strip()
