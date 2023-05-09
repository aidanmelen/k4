class State:
    def __init__(self) -> None:
        self._data = {}

    @setter
    def topic(self, data) -> str:
        self._data["topic"] = data

    @name.setter
    def name(self, value: str) -> None:
        self._name = value