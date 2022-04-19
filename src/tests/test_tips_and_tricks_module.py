'''testing tips_and_tricks'''
import sys
import os
import pytest

cwd = os.getcwd()
cwd = os.path.join(cwd,"process")
sys.path.insert(0, cwd)
from dbhandler import create_test_connection
create_test_connection()
from tips_and_tricks_module import *


def test_add_data():
    ''' test add data '''
    # create_test_connection()
    title = "judul1"
    subtitle = "konten1"
    konten = lorem.sentence()
    timestamp = generate_timestamp()
    data = (title, subtitle, konten, timestamp)
    add_tips_tricks_data(data)
    test1 = get_tips_tricks_by_id(1)
    assert test1[1] == data[0]
    assert test1[2] == data[1]
    assert test1[3] == data[2]
    assert test1[4] == data[3]
    clear_tips_and_tricks()

def test_edit_data():
    ''' test edit data '''
    # create_test_connection()
    title = "judul2"
    subtitle = "konten2"
    konten = lorem.sentence()
    timestamp = generate_timestamp()
    data = [title, subtitle, konten, timestamp]
    add_tips_tricks_data(data)
    data = get_tips_tricks_by_id(1)
    data = list(data)
    data[1] = "tesGantiJudul"
    edit_tips_tricks_data(data)
    test1 = get_tips_tricks_by_id(1)
    assert test1[1] == "tesGantiJudul"
    clear_tips_and_tricks()

def test_get_all_data():
    ''' test get all data '''
    # create_test_connection()
    data_length = 10
    generate_data(data_length)
    data = get_recent_data(data_length)
    assert len(data) == data_length
    clear_tips_and_tricks()
    assert get_all_tips_and_tricks() == []

def test_delete_data():
    ''' test delete data '''
    # create_test_connection()
    data_length = 10
    generate_data(data_length)
    data = get_recent_data(data_length)
    for i in data:
        del_tips_tricks_by_id(i[0])
    data = get_recent_data(data_length)
    assert len(data) == 0