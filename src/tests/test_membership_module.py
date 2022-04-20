"""test for tips_and_tricks_module.py"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import process.membership_module as mm
import process.credentials as cred

cred.register_account("Usada", "usaken@gmail.com", "12345678")

def test_req_membership():
    """test for request membership"""
    mm.request_membership("Usada", "42315", "33334444")
    data = mm.get_acc_by_uname("Usada")
    assert data[0] == "Usada"
    assert data[3] == "33334444"
    assert data[4] == "42315"
    assert data[5] == "PENDING"

def test_acc_membership():
    """test for accept membership"""
    mm.accept_membership("Usada")
    data = mm.get_acc_by_uname("Usada")
    assert data[0] == "Usada"
    assert data[3] == "33334444"
    assert data[4] == "42315"
    assert data[5] == "MEMBER"

def test_reject_membership():
    """test for reject membership"""
    mm.request_membership("Usada","1234","4444")
    mm.reject_membership("Usada")
    data = mm.get_acc_by_uname("Usada")
    assert data[0] == "Usada"
    assert data[3] is None
    assert data[4] is None
    assert data[5] == "CUSTOMER"
