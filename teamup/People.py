# -*- coding: utf-8 -*-
"""
    Manage a group of Person
"""
from teamup.Person import Person


class People:
    def __init__(self):
        self.all: List[Person] = []

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
