import sys
import pytest
from pathlib import Path
from teamup.PersistentLoopCounter import PersistentLoopCounter

counter_path = Path()
bound = 10


def test_create(capsys):
    PersistentLoopCounter.delete(counter_path)
    assert not PersistentLoopCounter.exists(counter_path)
    plc = PersistentLoopCounter.create(counter_path, bound)
    assert PersistentLoopCounter.exists(counter_path)
    assert plc.index() == 0


def test_next(capsys):
    plc = PersistentLoopCounter.get(counter_path)
    assert plc.index() == 0
    assert plc.next() == 1
    assert plc.index() == 1


def test_bound(capsys):
    plc = PersistentLoopCounter.get(counter_path)
    sequence = [(plc.index(), plc.next()) for i in range(0, bound + 1)]
    assert sequence == [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 0), (0, 1), (1, 2)
    ]


def test_delete(capsys):
    assert PersistentLoopCounter.exists(counter_path)
    PersistentLoopCounter.delete(counter_path)
    assert not PersistentLoopCounter.exists(counter_path)

