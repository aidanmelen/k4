import time

class Timer:
    def __init__(self):
        self.__current_time = time.perf_counter()
        self.__last_time = self.__current_time
        self.__elapsed_time = 0

    def has_time_elapsed(self, delta_time_seconds: int):
        return self.__elapsed_time > delta_time_seconds
    
    def update_elapsed_time(self):
        self.__current_time = time.perf_counter()
        self.__elapsed_time = self.current_time - self.__last_time
        self.__last_time = self.current_time