# -*- coding: utf-8 -*-
"""
Captures all information about a single pairing (that is, a variation
of all the combined teams). You use one pairing to produce one session.
"""
import json
import pprint
from round_robin import round_robin
from Person import Person
from People import People


class Pairing:

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
