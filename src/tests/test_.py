"""test for main.py"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

from process.dbhandler import create_connection
from main import main

def test_connection():
    """test for connection"""
    assert create_connection() is not None

def test_main(monkeypatch):
    """test main"""
    monkeypatch.setattr('builtins.input', lambda _: 13)
    main()
