import pytest
from pathlib import Path
from pprint import pprint
import sys
sys.path.append('..')
from pair_programming import Person, attendees

# with capsys.disabled():

def test_empty(capsys):
    Person("")
    Person(" ")
    assert attendees == set()


def test_single_name(capsys):
    Person("Bob")
    assert capsys.readouterr().out == "Error: at least first and last name required [Bob]\n"


def test_basic(capsys):
    assert Person("bruce eckel") == Person("Bruce Eckel")
    assert Person("Bruce eckel") == Person("Bruce Eckel")
    assert Person("bruce Eckel") == Person("Bruce Eckel")
    assert Person("bruce eckel") == "Bruce Eckel"
    assert Person("Bruce eckel") == "Bruce Eckel"
    assert Person("bruce Eckel") == "Bruce Eckel"
    assert attendees == {'Bruce Eckel'}


def test_group(capsys):
    [Person(name) for name in Path("Banzai.txt").read_text().splitlines()]
    assert attendees == {
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
