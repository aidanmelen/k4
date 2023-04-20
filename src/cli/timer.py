import time

class Timer:
    def __init__(self, clock=time.perf_counter):
        self.clock = clock
        self.start_time = self.clock()

    @property
    def elapsed_time(self) -> float:
        return self.clock() - self.start_time

    def has_elapsed(self, seconds) -> bool:
        return self.elapsed_time >= seconds

    def reset(self) -> None:
        self.start_time = self.clock()