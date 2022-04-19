'''testing tips_and_tricks'''
import sys
import os

cwd = os.getcwd()
cwd = os.path.join(cwd,"process")
sys.path.insert(0, cwd)
from process.dbhandler import create_test_connection
import process.tips_and_tricks_module as tnt

create_test_connection()

def test_add_data():
    ''' test add data '''
    # create_test_connection()
    title = "judul1"
    subtitle = "konten1"
    konten = tnt.lorem.sentence()
    timestamp = tnt.generate_timestamp()
    data = (title, subtitle, konten, timestamp)
    tnt.add_tips_tricks_data(data)
    test1 = tnt.get_tips_tricks_by_id(1)
    assert test1[1] == data[0]
    assert test1[2] == data[1]
    assert test1[3] == data[2]
    assert test1[4] == data[3]
    tnt.clear_tips_and_tricks()

def test_edit_data():
    ''' test edit data '''
    # create_test_connection()
    title = "judul2"
    subtitle = "konten2"
    konten = tnt.lorem.sentence()
    timestamp = tnt.generate_timestamp()
    data = [title, subtitle, konten, timestamp]
    tnt.add_tips_tricks_data(data)
    data = tnt.get_tips_tricks_by_id(1)
    data = list(data)
    data[1] = "tesGantiJudul"
    tnt.edit_tips_tricks_data(data)
    test1 = tnt.get_tips_tricks_by_id(1)
    assert test1[1] == "tesGantiJudul"
    tnt.clear_tips_and_tricks()

def test_get_all_data():
    ''' test get all data '''
    # create_test_connection()
    data_length = 10
    tnt.generate_data(data_length)
    data = tnt.get_recent_data(data_length)
    assert len(data) == data_length
    tnt.clear_tips_and_tricks()
    assert tnt.get_all_tips_and_tricks() == []

def test_delete_data():
    ''' test delete data '''
    # create_test_connection()
    data_length = 10
    tnt.generate_data(data_length)
    data = tnt.get_recent_data(data_length)
    for i in data:
        tnt.del_tips_tricks_by_id(i[0])
    data = tnt.get_recent_data(data_length)
    assert len(data) == 0
