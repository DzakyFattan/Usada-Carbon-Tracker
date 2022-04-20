"""test for credentials.py"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import process.credentials as cred

def test_username_registered():
    """test username registered"""
    assert cred.is_username_registered("Peko") is False

def test_register_new():
    """test register new user"""
    cred.register_account("Peko", "Peko@Pe.ko", "usausa")
    assert cred.is_username_registered("Peko")

def test_invalid_input():
    """test invalid input"""
    assert cred.register_account("", "pe@pe.ga", "") == 3

def test_is_logged_in():
    """test is logged in"""
    assert cred.is_logged_in("Peko") is False

def test_login():
    """test login"""
    cred.login_account("Peko", "usausa")
    assert cred.is_logged_in("Peko")

def test_login_not_registered():
    """test login not registered"""
    assert cred.login_account("Moona", "Hoshinova") == 2

def test_logout():
    """test logout"""
    cred.login_account("Peko", "usausa")
    cred.logout_account("Peko")
    assert cred.is_logged_in("Peko") is False
