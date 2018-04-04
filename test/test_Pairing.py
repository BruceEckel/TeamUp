import pytest
from pathlib import Path
from pprint import pprint
import sys
sys.path.append('..')
from pair_programming import Person, People, Pairing


def test_small(capsys):
    attendees = People().add_list(
        ["Emilio Lizardo", "Penny Priddy", "John Whorfin", "John Parker"])
    pairing_2 = Pairing(2, attendees)
    assert pairing_2 == [
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
    with capsys.disabled():
        print("pairing_3.pairing_number_bound", pairing_3.pairing_number_bound)
    for n in range(pairing_3.pairing_number_bound):
        pn = Pairing(n, attendees)
        with capsys.disabled():
            print(pn)
    with pytest.raises(AssertionError):
        pairing_plus_one = Pairing(
            pairing_3.pairing_number_bound + 1, attendees)


def test_single_pairing(capsys):
    attendees = People.from_file(Path("Banzai.txt"))
    pairing_7 = Pairing(7, attendees)
    assert pairing_7 == [
        ["John Starbird", "John Scott"],
        ["John Take Cover", "John Roberts"],
        ["John Thorny Stick", "John Repeat Dance"],
        ["John Two Horns", "John Ready To Fly"],
        ["John Wood", "John Rajeesh"],
        ["John Wright", "John Parrot"],
        ["John Ya Ya", "John Omar"],
        ["Buckaroo Banzai", "John O'Connor"],
        ["Emilio Lizardo", "John Nolan"],
        ["Penny Priddy", "John Nephew"],
        ["John Whorfin", "John Mud Head"],
        ["John Parker", "John Milton"],
        ["John Valuk", "John Many Jars"],
        ["John Emdall", "John Littlejohn"],
        ["John Gant", "John Lee"],
        ["John Bigboote", "John Kim Chi"],
        ["John Yaya", "John Joseph"],
        ["John Smallberries", "John Jones"],
        ["John Barnett", "John Icicle Boy"],
        ["John Camp", "John Guardian"],
        ["John Careful Walker", "John Grim"],
        ["John Chief Crier", "John Gomez"],
        ["John Cooper", "John Fledgling"],
        ["John Coyote", "John Fish", "John Edwards"]
    ]
