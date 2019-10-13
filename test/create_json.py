import sys
from pathlib import Path
sys.path.append('..')
from pairings import Pairings

def simple():
    pairings = Pairings.from_list(
        ["Emilio Lizardo", "Penny Priddy", "John Whorfin", "John Parker"])
    print(pairings.json())


def simple2():
    pairings = Pairings.from_file(Path("Banzai.txt"))
    print(pairings.json())


def simple3():
    pairings = Pairings.from_file(Path("Attendees.txt"))
    print(pairings.json())


if __name__ == '__main__':
    # simple()
    # simple2()
    simple3()
