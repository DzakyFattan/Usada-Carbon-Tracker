"""credentials handler"""

from process.dbhandler import create_connection

mydb = create_connection()

mycursor = mydb.cursor()

def is_username_registered(username):
    """Check if username is registered"""
    sql = f"SELECT * FROM account WHERE username = '{username}'"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if result:
        return True
    return False

def get_account_status(username):
    """Get account status"""
    sql = f"SELECT account_status FROM account WHERE username = \"{username}\""
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if result:
        return result[0]
    return None

def is_email_registered(email):
    """Check if email is registered"""
    sql = f"SELECT * FROM account WHERE email = '{email}'"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if result:
        return True
    return False

def register_account(username, email, password):
    """Register account"""
    if username is None or email is None or password is None:
        return 3 # invalid input
    if username == "" or email == "" or password == "":
        return 3 # invalid input too
    if is_username_registered(username):
        return 1 # username already registered
    if is_email_registered(email):
        return 2 # email already registered
    sql = "INSERT INTO account (username, email, password, credit_card, no_telp)"
    sql += f"VALUES ('{username}', '{email}', '{password}', '{None}', '{None}')"
    mycursor.execute(sql)
    mydb.commit()
    return 0

def is_logged_in(username):
    """check if username already logged in"""
    sql = f"SELECT * FROM logged_user WHERE username = '{username}'"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if result:
        return True
    return False

def login_account(username, password):
    """Login account"""
    if is_logged_in(username):
        return 1 # username already logged in
    sql = f"SELECT * FROM account WHERE username = '{username}' AND password = '{password}'"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if not result:
        return 2 # username or password incorrect
    sql = f"INSERT INTO logged_user (username) VALUES ('{username}')"
    mycursor.execute(sql)
    mydb.commit()
    return 0

def logout_account(username):
    """Logout account"""
    if not is_logged_in(username):
        return 1 # username not logged in
    sql = f"DELETE FROM logged_user WHERE username = '{username}'"
    mycursor.execute(sql)
    mydb.commit()
    return 0
