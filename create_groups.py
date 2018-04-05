# -*- coding: utf-8 -*-
"""
    Combine people for group activities
"""
from pathlib import Path
import sys
import click


@click.group()
@click.version_option()
def cli():
    """Create Teams

    Generates and displays 2 or 3 person teams using a round-robin algorithm.
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
