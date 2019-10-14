from pathlib import Path
import pprint
import sys
import pytest
sys.path.append('..')
from Person import Person
from People import People
from Pairing import Pairing


def display(capsys, item):
    "Show item on stdout"
    # with capsys.disabled():
    #     print(item)


def test_small(capsys):
    attendees = People().add_list(
        ["Emilio Lizardo", "Penny Priddy", "John Whorfin", "John Parker"])
    p = Pairing(0, attendees)
    assert p.pairing_number_bound == 3
    every = [Pairing(n, attendees) for n in range(p.pairing_number_bound)]
    assert every[0] == [
        ["Emilio Lizardo", "John Parker"],
        ["Penny Priddy", "John Whorfin"]
    ]
    assert every[1] == [
        ["Emilio Lizardo", "John Whorfin"],
        ["John Parker", "Penny Priddy"]
    ]
    assert every[2] == [
        ["Emilio Lizardo", "Penny Priddy"],
        ["John Whorfin", "John Parker"]
    ]


def test_pairing_upper_bound(capsys):
    attendees = People().add_list(
        ["Emilio Lizardo", "Penny Priddy", "John Whorfin", "John Parker"])
    with pytest.raises(AssertionError):
        pairing_3 = Pairing(3, attendees)
    attendees.add(Person("Buckaroo Banzai"))
    pairing_3 = Pairing(3, attendees)
    assert pairing_3 == [
        ["John Whorfin", "Penny Priddy"],
        ["John Parker", "Emilio Lizardo", "Buckaroo Banzai"]
    ]
    display(capsys, f"pairing_3.pairing_number_bound {pairing_3.pairing_number_bound}")
    for n in range(pairing_3.pairing_number_bound):
        pn = Pairing(n, attendees)
        display(capsys, pn)
    with pytest.raises(AssertionError):
        Pairing(pairing_3.pairing_number_bound + 1, attendees)


def test_single_pairing(capsys):
    attendees = People.from_file(Path("Banzai.txt"))
    pairing_7 = Pairing(7, attendees)
    display(capsys, pairing_7)
    assert pairing_7 == [
        ["John Two Horns", "John Thorny Stick"],
        ["John Valuk", "John Take Cover"],
        ["John Whorfin", "John Starbird"],
        ["John Wood", "John Smallberries"],
        ["John Wright", "John Scott"],
        ["John Ya Ya", "John Roberts"],
        ["Penny Priddy", "John Repeat Dance"],
        ["Buckaroo Banzai", "John Ready To Fly"],
        ["Emilio Lizardo", "John Rajeesh"],
        ["John Barnett", "John Parrot"],
        ["John Bigboote", "John Parker"],
        ["John Camp", "John Omar"],
        ["John Careful Walker", "John O'Connor"],
        ["John Chief Crier", "John Nolan"],
        ["John Cooper", "John Nephew"],
        ["John Coyote", "John Mud Head"],
        ["John Edwards", "John Milton"],
        ["John Emdall", "John Many Jars"],
        ["John Fish", "John Littlejohn"],
        ["John Fledgling", "John Lee"],
        ["John Gant", "John Kim Chi"],
        ["John Gomez", "John Joseph"],
        ["John Grim", "John Icicle Boy", "John Guardian"]
    ]


def test_pairing_duplicates(capsys):
    attendees = People.from_file(Path("Banzai.txt"))
    p = Pairing(0, attendees)
    every = [Pairing(n, attendees) for n in range(p.pairing_number_bound)]
    flat = [pair for each in every for pair in each]
    Path("test_pairing_all.txt").write_text(pprint.pformat(flat))
    dups = []
    while flat:
        next_pair = flat.pop()
        if len(next_pair) == 3:
            continue
        for pair in flat:
            if next_pair[0] in pair and next_pair[1] in pair and len(pair) < 3:
                dups.append(f"{next_pair}, {pair}\n")
    assert not dups, f"duplicates: {pprint.pformat(dups)}"

