"""test for main.py"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

from main import main

def test_main(monkeypatch):
    """test main"""
    monkeypatch.setattr('builtins.input', lambda _: 13)
    assert main() is not None
