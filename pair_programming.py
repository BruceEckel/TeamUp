# -*- coding: utf-8 -*-
"""
    Produces & Displays Pair Programming pairs
"""
from pathlib import Path
from collections import deque
import sys
import click
database = Path('SeminarAttendees.txt')
attendees = Path("Attendees.txt")


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


attendees = set()


class Person:

    @staticmethod
    def sanitize(unclean):
        def san(nm):
            return " ".join([part.strip().capitalize().replace(",", "") for part in nm.split()])
        first, last = unclean.rsplit(" ", 1)
        return san(first) + " " + san(last)

    def __init__(self, name):
        if name.strip() == "":
            self.name = None
            return
        if " " not in name:
            print(f"Error: at least first and last name required [{name}]")
            self.name = None
            return
        self.name = Person.sanitize(name)
        attendees.add(self.name)

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

# This should be a single Pairing, then just create a list of them.
class Pairings:

    pairing_number = -1  # Need to init based on existing pairings file

    @staticmethod
    def nextPairingNumber():
        assert len(attendees), "Database empty"
        index = Pairings.pairing_number + 1
        if index > 0 and index % len(attendees) == 0:
            index = 0
        Pairings.pairing_number = index
        return index

    @staticmethod
    def generateNextPairings():
        size = len(attendees)
        assert size, "empty database"
        groups = round_robin(size)[Pairings.nextPairingNumber()]
        teams = []
        for group in groups:
            teams.append([attendees[i] for i in group])
        return teams

    @staticmethod
    def generate_pairs():
        "Generate new pairs"
        def divideList(seq, num):
            avg = len(seq) / float(num)
            result = []
            last = 0.0
            while last < len(seq):
                result.append(seq[int(last):int(last + avg)])
                last += avg
            return result
        return divideList(Pairings.generateNextPairings(), 4)


@click.group()
@click.version_option()
def cli():
    """Pair Programming

    Generates and displays pair-programming teams using a round-robin algorithm.
    """


@cli.command()
def create_attendee_database():
    if not attendees.exists():
        print("Attendees.txt not found")
        sys.exit(1)
    return generate_new_database(attendees.read_text().splitlines())


@cli.command("genNewDB")
def generate_new_database(nameList):
    "Create new database"

    if database.exists():
        database.unlink()
    # Eliminate duplicate sanitized names
    return [Person(nm) for nm in {sanitize(nm) for nm in nameList}]


if __name__ == '__main__':
    cli()
