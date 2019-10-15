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
html = Path() / "html"


@click.group()
@click.version_option()
def main():
    """
    Generates and displays all combinations of 2-person teams using a
    round-robin algorithm. Requires an Attendees.txt file containing
    one name per line. Remove the 'html' directory to restart.
    """


def display(index):
    pairing = html / f"pairing{index}.html"
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
    if not html.exists():
        pairings.create_html_files()
        PersistentLoopCounter.create(html, pairings.bound)
    display(PersistentLoopCounter.get(html).index())


@main.command()
def next():
    """
    Moves to next team grouping and shows
    """
    if not html.exists():
        print("No 'html' directory, first run 'teamup current'")
        sys.exit(1)
    display(PersistentLoopCounter.get(html).next())


# @main.command()
# def clean():
#     """
#     Erases the 'html' directory
#     """
#     if html.exists():
#         html.unlink()


if __name__ == "__main__":
    main()
