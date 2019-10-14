import sys
import pytest
from pathlib import Path
sys.path.append('..')
from pairings import Pairings


def test_create_html_files(capsys):
    pairings = Pairings.from_file(Path("Banzai.txt"))
    pairings.create_html_files()
