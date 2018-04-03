import pytest
from pathlib import Path
from pprint import pprint
import sys
sys.path.append('..')
from pair_programming import Person, Pairings


def test_empty(capsys):
    Person("")
    Person(" ")
    with capsys.disabled():
        pprint(Pairings.all)


def test_single_name(capsys):
    Person("Bob")  # How do we capture the error message for this????


def test_basic(capsys):
    assert Person("bruce eckel") == Person("Bruce Eckel")
    assert Person("Bruce eckel") == Person("Bruce Eckel")
    assert Person("bruce Eckel") == Person("Bruce Eckel")
    assert Person("bruce eckel") == "Bruce Eckel"
    assert Person("Bruce eckel") == "Bruce Eckel"
    assert Person("bruce Eckel") == "Bruce Eckel"
    assert Pairings.all == {'Bruce Eckel'}


def test_group(capsys):
    [Person(name) for name in Path("Banzai.txt").read_text().splitlines()]
    assert Pairings.all == {
        'Bruce Eckel',
        'Buckaroo Banzai',
        'Emilio Lizardo',
        'John Barnett',
        'John Bigboote',
        'John Camp',
        'John Careful Walker',
        'John Chief Crier',
        'John Cooper',
        'John Coyote',
        'John Edwards',
        'John Emdall',
        'John Fish',
        'John Fledgling',
        'John Gant',
        'John Gomez',
        'John Grim',
        'John Guardian',
        'John Icicle Boy',
        'John Jones',
        'John Joseph',
        'John Kim Chi',
        'John Lee',
        'John Littlejohn',
        'John Many Jars',
        'John Milton',
        'John Mud Head',
        'John Nephew',
        'John Nolan',
        "John O'connor",
        'John Omar',
        'John Parker',
        'John Parrot',
        'John Rajeesh',
        'John Ready To Fly',
        'John Repeat Dance',
        'John Roberts',
        'John Scott',
        'John Smallberries',
        'John Starbird',
        'John Take Cover',
        'John Thorny Stick',
        'John Two Horns',
        'John Valuk',
        'John Whorfin',
        'John Wood',
        'John Wright',
        'John Ya Ya',
        'John Yaya',
        'Penny Priddy'
    }
