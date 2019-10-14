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
from display_page import html_page


class People:

    def __init__(self):
        self.all : List[Person] = []

    def __len__(self):
        return len(self.all)

    def __getitem__(self, key):
        return self.all[key]

    def add(self, person: Person):
        assert person not in self.all, f"Duplicate person name: {person}"
        self.all.append(person)

    def add_list(self, attendee_list):
        for a in attendee_list:
            a = a.strip()
            if a:
                self.add(Person(a))
        return self

    def __repr__(self):
        return pprint.pformat(self.all)

    @staticmethod
    def from_file(filepath):
        return People().add_list(filepath.read_text().splitlines())


class Pairing:
    """
    Captures all information about a single pairing (that is, a variation
    of all the combined teams). You use one pairing to produce one session.
    """

    def __init__(self, pairing_number: int, people: People):
        assert pairing_number >= 0
        assert len(people) >= 3
        rr = round_robin(len(people))
        self.pairing_number_bound = len(rr)
        assert pairing_number < self.pairing_number_bound, f"pairing_number must be < {self.pairing_number_bound}"
        self.pairing_number = pairing_number
        self.people = people
        self.groups = rr[self.pairing_number]
        self.teams = [[people[i] for i in group] for group in self.groups]

    def __str__(self):
        return f"Pairing {self.pairing_number}:\n{pprint.pformat(self.teams)}"

    def __repr__(self):
        return f"{pprint.pformat(self.teams)}"

    def __eq__(self, other):
        if isinstance(other, list):
            return self.teams == other
        return False

    def __iter__(self):
        return iter(self.teams)


class PairingEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pairing):
            return obj.teams
        if isinstance(obj, Person):
            return obj.name
        # Base class default() raises TypeError:
        return json.JSONEncoder.default(self, obj)


class Pairings:
    """
    All possible combinations of groups (every round-robin possibility).
    Typical usage of this library is:
    pairings = Pairings.from_file(filepath)
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

