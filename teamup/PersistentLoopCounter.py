"""
Counts from zero to bound -1, then restarts at zero. Stores the current count
and bound in a text file. When it starts, it looks for that file and reads it
as the current count if it exists, and initializes a new zeroed file if it
doesn't exist.
"""
from pathlib import Path

plc_name = "PersistentLoopCounter.txt"


class PLC:
    def __update(self):
        assert self.__count >= 0
        assert self.__count < self.__bound
        self.__counter_file.write_text(f"[{self.__count}, {self.__bound}]")

    def __init__(self, count: int, bound: int, counter_file: Path):
        self.__count = count
        self.__bound = bound
        self.__counter_file = counter_file
        if not self.__counter_file.exists():
            self.__update()

    def index(self):
        return self.__count

    def next(self):
        if self.__count == self.__bound - 1:
            self.__count = 0
        else:
            self.__count += 1
        self.__update()
        return self.index()


class PersistentLoopCounter:
    @staticmethod
    def create(path: Path, bound: int):
        counter_file = path / plc_name
        assert not counter_file.exists(), f"{counter_file} already exists"
        return PLC(0, bound, counter_file)

    @staticmethod
    def exists(path: Path):
        counter_file = path / plc_name
        return counter_file.exists()

    @staticmethod
    def get(path: Path):
        counter_file = path / plc_name
        assert counter_file.exists(), f"{counter_file} doesn't exist"
        count, bound = eval(counter_file.read_text().strip())
        return PLC(count, bound, counter_file)

    @staticmethod
    def delete(path: Path):
        counter_file = path / plc_name
        if counter_file.exists():
            counter_file.unlink()
