# -*- coding: utf-8 -*-
"""
    Pairs people for group activities
"""
from collections import deque
import random
import pprint


def round_robin_even(d, n):
    for i in range(n - 1):
        yield [[d[j], d[-j-1]] for j in range(n//2)]
        d[0], d[-1] = d[-1], d[0]
        d.rotate()


def round_robin_odd(d, n):
    for i in range(n):
        h = [[d[j], d[-j-1]] for j in range(n//2)]
        h[-1].append(d[n//2])
        yield h
        d.rotate()


def round_robin(n):
    assert n > 1
    d = deque(range(n))
    if n % 2 == 0:
        return list(round_robin_even(d, n))
    else:
        return list(round_robin_odd(d, n))


class Person:

    @staticmethod
    def sanitize(unclean):
        def san(nm):
            return " ".join([part.strip().title().replace(",", "") for part in nm.split()])
        first, last = unclean.rsplit(" ", 1)
        return san(first) + " " + san(last)

    def __init__(self, name):
        assert name.strip(), "Empty 'name'"
        assert " " in name, f"At least first and last name required [{name}]"
        self.name = Person.sanitize(name)

    def __repr__(self):
        return '"' + self.name + '"'

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name


class People:

    def __init__(self):
        self.all = []

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
    "Captures all information about a single pairing"

    def __init__(self, pairing_number, people: People):
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


class Pairings:

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

    @staticmethod
    def from_list(lst):
        return Pairings(People().add_list(lst))

    @staticmethod
    def from_file(filepath):
        return Pairings(People.from_file(filepath))

    # pairing_number = -1  # Need to init based on existing pairings file

    # @staticmethod
    # def nextPairingNumber():
    #     index = Pairings.pairing_number + 1
    #     if index > 0 and index % len(attendees) == 0:
    #         index = 0
    #     Pairings.pairing_number = index
    #     return index

    # @staticmethod
    # def generateNextPairings():
    #     size = len(attendees)
    #     assert size, "empty database"
    #     groups = round_robin(size)[Pairings.nextPairingNumber()]
    #     teams = []
    #     for group in groups:
    #         teams.append([attendees[i] for i in group])
    #     return teams

    @staticmethod
    def divideList(seq, num):
        avg = len(seq) / float(num)  # Need to test this for Python 3
        result = []
        last = 0.0
        while last < len(seq):
            result.append(seq[int(last):int(last + avg)])
            last += avg
        return result

    @staticmethod
    def generate_pairs():
        "Generate new pairs"
        # return Pairings.divideList(Pairings.generateNextPairings(), 4)


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
            self.count = eval(self.file_path.read_text().strip())
        else:
            self.count = 0

    def next(self):
        result = self.count
        if self.count > 0 and self.count % self.bound == 0:
            self.count = 0
        else:
            self.count += 1
        self.file_path.write_text(f"{self.count}")
        return result
