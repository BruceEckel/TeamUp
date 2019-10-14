# -*- coding: utf-8 -*-
"""
    Information about a single person
"""


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
