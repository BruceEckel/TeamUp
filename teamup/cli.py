# -*- coding: utf-8 -*-
"""
    Combine people for group activities
"""
from pathlib import Path
import os, sys
import click
import webbrowser
from teamup.pairings import Pairings
from teamup.PersistentLoopCounter import PersistentLoopCounter

attendees = Path("Attendees.txt")
build = Path() / "build"

@click.group()
@click.version_option()
def main():
    """
    Generates and displays all combinations of 2-person teams using a
    round-robin algorithm. Requires an Attendees.txt file containing
    one name per line. Remove the 'build' directory to restart.
    """

def display(index):
    pairing = build / f"pairing{index}.html"
    assert pairing.exists()
    webbrowser.open_new_tab(pairing)


@main.command()
def current():
    """
    Show current teams
    """
    if not attendees.exists():
        print("Attendees.txt not found")
        sys.exit(1)
    pairings = Pairings.from_file(Path("Attendees.txt"))
    if not build.exists():
        pairings.create_html_files()
        PersistentLoopCounter.create(build, pairings.bound)
    display(PersistentLoopCounter.get(build).index())


@main.command()
def next():
    """
    Moves to next team grouping and shows
    """
    if not build.exists():
        print("No 'build' directory, first run 'teamup current'")
        sys.exit(1)
    display(PersistentLoopCounter.get(build).next())


# @main.command()
# def clean():
#     """
#     Erases the 'build' directory
#     """
#     if build.exists():
#         build.unlink()


if __name__ == '__main__':
    main()
