import random
import json
import pprint
from collections import deque
from pathlib import Path

class PersistentLoopCounter:
    """
    Counts from zero to bound -1, then restarts at zero.
    Stores the current count in a text file. When it starts,
    it looks for that file and reads it as the current count
    if it exists, and initializes a new zeroed file if it doesn't
    exist.
    """
    def __init__(self, file_name_stem, bound):
        self.file_path = Path(file_name_stem + "_count.txt")
        self.bound = bound
        if self.file_path.exists():
            self.__count = eval(self.file_path.read_text().strip())
        else:
            self.__count = 0
            self.file_path.write_text(f"{self.__count}")
        assert self.__count >= 0

    def count(self):
        return self.__count

    def next(self):
        if self.__count == self.bound - 1:
            self.__count = 0
        else:
            self.__count += 1
        assert self.__count >= 0
        self.file_path.write_text(f"{self.__count}")
        return self.__count

    @staticmethod
    def delete(file_name_stem):
        counter_file = Path(file_name_stem + "_count.txt")
        if counter_file.exists():
            counter_file.unlink()
