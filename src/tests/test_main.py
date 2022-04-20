"""test for main.py"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

from main import main

if(os.path.exists("usada_carbon_tracker.db")):
    os.remove("usada_carbon_tracker.db")
    
def test_main(monkeypatch):
    """test main"""
    monkeypatch.setattr('builtins.input', lambda _: 13)
    main()
