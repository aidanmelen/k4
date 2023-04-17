import traceback


class K4Error(Exception):
    """The k4 error class."""

    LOGO = [
        " ____      _____  ",
        "|    | __ /  |  | ",
        "|    |/ //   |  |_",
        "|      </    ^   /",
        "|____|_ \\____   |",
        "       \\/    |__|",
    ]

    def __init__(self, message, error):
        self.message = message
        self.error = error
        super().__init__(self.message)
