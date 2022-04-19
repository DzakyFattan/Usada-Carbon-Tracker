"""sqlite db handler"""

import sqlite3
from sqlite3 import Error
import os
import sys

def create_connection():
    """create a database connection to the SQLite database"""
    conn = None
    sql = resource_path("usada_carbon_tracker.sql")
    print(sql)
    sql_script = None
    try:
        if not os.path.exists("usada_carbon_tracker.db"):
            print("db not exist, creating new...")
            with open(sql, "r", encoding="utf-8") as sql_script:
                sql_script = sql_script.read()
                print("Running .sql...")
        conn = sqlite3.connect("usada_carbon_tracker.db")
        if sql_script:
            conn.executescript(sql_script)
    except Error as error:
        print(error)
        conn.close()
        os.remove("usada_carbon_tracker.db")
        print("Remove db...")
        return None

    return conn

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = ""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        pass

    if base_path == "":
        tmp_path = os.getcwd()
        if tmp_path.endswith("tests"):
            base_path = os.path.join("..", "sqlscript")
        else:
            base_path = os.path.join(os.getcwd(), "sqlscript")

    return os.path.join(base_path, relative_path)

def create_test_connection():
    """create a database connection to the SQLite test database"""
    conn = None
    sql = resource_path("usada_carbon_tracker.sql")
    sql_script = None
    try:
        if os.path.exists("usada_carbon_tracker_test.db"):
            os.remove("usada_carbon_tracker_test.db")
        with open(sql, "r", encoding="utf-8") as sql_script:
                sql_script = sql_script.read()
        conn = sqlite3.connect("usada_carbon_tracker_test.db")
        if sql_script:
            conn.executescript(sql_script)
    except Error as error:
        print(error)
        conn.close()
        os.remove("usada_carbon_tracker.db")
        print("Remove db...")
        return None

    return conn
