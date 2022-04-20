"""test for dbhandler.py"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

from process.dbhandler import create_connection

if(os.path.exists("usada_carbon_tracker.db")):
    os.remove("usada_carbon_tracker.db")
def test_connection():
    """test for connection"""
    assert create_connection() is not None
