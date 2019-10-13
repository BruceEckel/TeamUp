import sys
from pathlib import Path
sys.path.append('..')
from pairings import Pairings


def display(capsys, item):
    "Show item on stdout"
    with capsys.disabled():
        print(item)


def test_small(capsys):
    pairings = Pairings.from_list(
        ["Emilio Lizardo", "Penny Priddy", "John Whorfin", "John Parker"])
    assert pairings.bound == 3
    assert len(pairings) == 3
    assert pairings.all[0] == [
        ["Emilio Lizardo", "John Parker"],
        ["Penny Priddy", "John Whorfin"]
    ]
    assert pairings.all[1] == [
        ["Emilio Lizardo", "John Whorfin"],
        ["John Parker", "Penny Priddy"]
    ]
    assert pairings.all[2] == [
        ["Emilio Lizardo", "Penny Priddy"],
        ["John Whorfin", "John Parker"]
    ]
    assert pairings[0] == [
        ["Emilio Lizardo", "John Whorfin"],
        ["John Parker", "Penny Priddy"]
    ]
    assert pairings[1] == [
        ["Emilio Lizardo", "John Parker"],
        ["Penny Priddy", "John Whorfin"]
    ]
    assert pairings[2] == [
        ["Emilio Lizardo", "Penny Priddy"],
        ["John Whorfin", "John Parker"]
    ]
    assert pairings.json() == ""


def test_single_pairing(capsys):
    pairings = Pairings.from_file(Path("Banzai.txt"))
    assert pairings.bound == 47
    assert len(pairings) == 47
    assert pairings[7] == [
        ["John Rajeesh", "John Parrot"],
        ["John Ready To Fly", "John Parker"],
        ["John Repeat Dance", "John Omar"],
        ["John Roberts", "John O'Connor"],
        ["John Scott", "John Nolan"],
        ["John Smallberries", "John Nephew"],
        ["John Starbird", "John Mud Head"],
        ["John Take Cover", "John Milton"],
        ["John Thorny Stick", "John Many Jars"],
        ["John Two Horns", "John Littlejohn"],
        ["John Valuk", "John Lee"],
        ["John Whorfin", "John Kim Chi"],
        ["John Wood", "John Joseph"],
        ["John Wright", "John Icicle Boy"],
        ["John Ya Ya", "John Guardian"],
        ["Penny Priddy", "John Grim"],
        ["Buckaroo Banzai", "John Gomez"],
        ["Emilio Lizardo", "John Gant"],
        ["John Barnett", "John Fledgling"],
        ["John Bigboote", "John Fish"],
        ["John Camp", "John Emdall"],
        ["John Careful Walker", "John Edwards"],
        ["John Chief Crier", "John Coyote", "John Cooper"]
    ]
    # display(capsys, pairings[46])
    assert pairings[46] == [
        ["John Camp", "John Bigboote"],
        ["John Careful Walker", "John Barnett"],
        ["John Chief Crier", "Emilio Lizardo"],
        ["John Cooper", "Buckaroo Banzai"],
        ["John Coyote", "Penny Priddy"],
        ["John Edwards", "John Ya Ya"],
        ["John Emdall", "John Wright"],
        ["John Fish", "John Wood"],
        ["John Fledgling", "John Whorfin"],
        ["John Gant", "John Valuk"],
        ["John Gomez", "John Two Horns"],
        ["John Grim", "John Thorny Stick"],
        ["John Guardian", "John Take Cover"],
        ["John Icicle Boy", "John Starbird"],
        ["John Joseph", "John Smallberries"],
        ["John Kim Chi", "John Scott"],
        ["John Lee", "John Roberts"],
        ["John Littlejohn", "John Repeat Dance"],
        ["John Many Jars", "John Ready To Fly"],
        ["John Milton", "John Rajeesh"],
        ["John Mud Head", "John Parrot"],
        ["John Nephew", "John Parker"],
        ["John Nolan", "John Omar", "John O'Connor"]
    ]
