import pytest
from pathlib import Path
from pprint import pprint
import sys
sys.path.append('..')
from pair_programming import Person, People


def test_single_add(capsys):
    people = People()
    people.add(Person("bruce eckel"))
    assert people.all == ["Bruce Eckel"]


def test_duplicate_add():
    with pytest.raises(AssertionError):
        people = People()
        people.add(Person("Bruce Eckel"))
        people.add(Person("Bruce Eckel"))
    with pytest.raises(AssertionError):
        people = People()
        people.add(Person("bruce eckel"))
        people.add(Person("bruce Eckel"))
    with pytest.raises(AssertionError):
        people = People()
        people.add(Person("bruce eckel"))
        people.add(Person("Bruce eckel"))


def test_short_list():
    people = People().add_list(["Bob Dobbs", "Ralph Kramden"])
    assert people.all == ["Bob Dobbs", "Ralph Kramden"]


def test_from_file(capsys):
    attendees = People.from_file(Path("Banzai.txt"))
    # with capsys.disabled():
    #     pprint(attendees)
    assert attendees.all == [
        "Buckaroo Banzai",
        "Emilio Lizardo",
        "Penny Priddy",
        "John Whorfin",
        "John Parker",
        "John Valuk",
        "John Emdall",
        "John Gant",
        "John Bigboote",
        "John Yaya",
        "John Smallberries",
        "John Barnett",
        "John Camp",
        "John Careful Walker",
        "John Chief Crier",
        "John Cooper",
        "John Coyote",
        "John Edwards",
        "John Fish",
        "John Fledgling",
        "John Gomez",
        "John Grim",
        "John Guardian",
        "John Icicle Boy",
        "John Jones",
        "John Joseph",
        "John Kim Chi",
        "John Lee",
        "John Littlejohn",
        "John Many Jars",
        "John Milton",
        "John Mud Head",
        "John Nephew",
        "John Nolan",
        "John O'Connor",
        "John Omar",
        "John Parrot",
        "John Rajeesh",
        "John Ready To Fly",
        "John Repeat Dance",
        "John Roberts",
        "John Scott",
        "John Starbird",
        "John Take Cover",
        "John Thorny Stick",
        "John Two Horns",
        "John Wood",
        "John Wright",
        "John Ya Ya",
    ]
