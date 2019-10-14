# -*- coding: utf-8 -*-
"""
    Pairs people for group activities
"""
import random
import json
import pprint
from collections import deque
from pathlib import Path
from round_robin import round_robin
from Person import Person
from People import People
from Pairing import Pairing, PairingEncoder
from display_page import html_page


class Pairings:
    """
    All possible combinations of groups (every round-robin possibility).
    Typical usage of this library is:
    pairings = Pairings.from_file(filepath)
    pairings.create_html_files()
    """

    def __init__(self, people: People, seed=47):
        assert len(people) >= 3, f"Number of people must be >= 3; Is {len(people)}"
        self.bound = Pairing(0, people).pairing_number_bound
        self.all = [Pairing(n, people) for n in range(self.bound)]
        random.seed(seed)
        self.sequence = random.sample(list(range(self.bound)), self.bound)

    def __getitem__(self, n):
        assert isinstance(n, int)
        assert n >= 0 and n < self.bound
        return self.all[self.sequence[n]]

    def  __len__(self): return self.bound

    def json(self):
        return json.dumps([self.all[n] for n in self.sequence], cls=PairingEncoder, indent=2)

    @staticmethod
    def from_list(lst):
        return Pairings(People().add_list(lst))

    @staticmethod
    def from_file(filepath):
        return Pairings(People.from_file(filepath))

    def create_html_files(self):
        build = Path() / "build"
        if not build.exists():
            build.mkdir()
        for n, pairing in enumerate([self.all[n] for n in self.sequence]):
            html_file = build / (f"pairing{n}.html")
            print(html_file)
            # Strip outer brackets of array to fit in Javascript Array() constructor:
            html_file.write_text(html_page % (('%s' % pairing.teams)[1:-1], len(pairing.teams)))

    @staticmethod
    def divideList(seq, num):
        avg = len(seq) / float(num)  # Need to test this for Python 3
        result = []
        last = 0.0
        while last < len(seq):
            result.append(seq[int(last):int(last + avg)])
            last += avg
        return result

