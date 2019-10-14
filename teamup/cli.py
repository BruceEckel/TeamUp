# -*- coding: utf-8 -*-
"""
    Combine people for group activities
"""
from pathlib import Path
import os, sys
import click
from teamup.pairings import Pairings

attendees = Path("Attendees.txt")
pairings = Path("pairings")

@click.group()
@click.version_option()
def main():
    """
    Generates and displays all combinations of 2-person teams using a
    round-robin algorithm. Requires an Attendees.txt file containing
    one name per line.
    """


@main.command()
def current():
    """
    Show current teams
    """
    if not attendees.exists():
        print("Attendees.txt not found")
        sys.exit(1)
    pairings = Pairings.from_file(Path("Attendees.txt"))


@main.command()
def next():
    """
    Moves to next team grouping and shows
    """
    if not pairings.exists():
        print("No 'pairings' directory, first run 'teamup current'")
        sys.exit(1)


if __name__ == '__main__':
    main()
