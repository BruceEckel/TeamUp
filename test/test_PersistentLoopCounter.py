import sys
import pytest
from pathlib import Path
sys.path.append('..')
from pairings import PersistentLoopCounter

base = "LoopCounter"
counter_path = Path(base + "_count.txt")
bound = 10


def test_create(capsys):
    PersistentLoopCounter.delete(base)
    assert counter_path.exists() == False
    plc = PersistentLoopCounter(base, bound)
    assert counter_path.exists() == True
    assert plc.count() == 0


def test_next(capsys):
    plc = PersistentLoopCounter(base, bound)
    assert plc.count() == 0
    assert plc.next() == 1
    assert plc.count() == 1


def test_bound(capsys):
    plc = PersistentLoopCounter(base, bound)
    sequence = [(plc.count(), plc.next()) for i in range(0, bound + 1)]
    assert sequence == [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 0), (0, 1), (1, 2)
    ]


def test_delete(capsys):
    assert counter_path.exists()
    PersistentLoopCounter.delete(base)
    assert not counter_path.exists()

