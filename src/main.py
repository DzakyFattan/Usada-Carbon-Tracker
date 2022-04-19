"""main module"""

from sqlite3 import Error
from process.dbhandler import create_connection

def main():
    """main function"""
    conn = create_connection()
    if conn is None:
        input("Error! cannot create the database connection.")
        return None

    print("Database connection created successfully.")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    except Error as error:
        input(error)
        return None
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
    input("Press Enter to continue...")
    return 0

if __name__ == "__main__":
    main()
