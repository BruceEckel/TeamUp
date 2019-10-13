# -*- coding: utf-8 -*-
"""
    Combine people for group activities
"""
from pathlib import Path
import os, sys
import click
from pairings import Pairings

attendees = Path("Attendees.txt")

@click.group()
@click.version_option()
def cli():
    """Create Teams

    Generates and displays all combinations of 2-person teams using a
    round-robin algorithm.
    """


@cli.command()
def teams():
    """
    Show next iteration of team combinations
    """
    print("Hello world")
    if not attendees.exists():
        print("Attendees.txt not found")
        sys.exit(1)
    pairings = Pairings.from_file(Path("Attendees.txt"))
    print(pairings.json())


@cli.command()
def test():
    """
    Run pytests
    """
    os.chdir("test")
    os.system("pytest")

# @cli.command()
# def create_attendee_database():
#     if not attendees.exists():
#         print("Attendees.txt not found")
#         sys.exit(1)
#     return generate_new_database(attendees.read_text().splitlines())


# @cli.command("genNewDB")
# def generate_new_database(nameList):
#     "Create new database"

#     if database.exists():
#         database.unlink()
#     # Eliminate duplicate sanitized names
#     return [Person(nm) for nm in {sanitize(nm) for nm in nameList}]


if __name__ == '__main__':
    cli()
