'''import random'''
from datetime import datetime
from dbhandler import create_connection

mydb = create_connection()

mycursor = mydb.cursor()

def generate_account_data(data):
    ''' generate n random data '''
    for i in range(len(data)):
        cmd = "INSERT INTO account(username, email, password, account_status)"
        data = ("Orang" + str(i), "Orang" + str(i), "1234", "CUSTOMER")
        cmd += f" VALUES (\"{data[0]}\", \"{data[1]}\", \"{str(data[2])}\", \"{data[3]}\");"
        mycursor.execute(cmd)
        mydb.commit()

def get_acc_by_uname(username):
    ''' return account data based on username '''
    cmd = f"SELECT * FROM account WHERE username = \"{username}\""
    mycursor.execute(cmd)
    return mycursor.fetchone()

def update_acc(data):
    ''' update account data '''
    cmd = f"UPDATE account SET email = \"{data[1]}\", password = \"{data[2]}\", "
    cmd += f"credit_card = \"{data[3]}\", no_telp = \"{data[4]}\", "
    cmd += f"account_status = \"{data[5]}\" WHERE username = \"{data[0]}\""
    mycursor.execute(cmd)
    mydb.commit()

def request_membership(username, no_telp, credit_card):
    ''' request membership no telp dan credit card akan ditambahkan pada tabel account
    untuk sementara status membership akan menandakan -1 yang artinya pending'''
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    cmd = "INSERT INTO pending_membership(username,timestamp_key) "
    cmd += f"VALUES (\"{username}\", \"{date_time}\")"
    print(cmd,"KONTOL")
    mycursor.execute(cmd)
    mydb.commit()

    # update account data
    data = get_acc_by_uname(username)
    data = list(data)
    data[3] = credit_card
    data[4] = no_telp
    data[5] = "PENDING"
    update_acc(data)

def is_member(username):
    ''' return true if user is member '''
    data = get_acc_by_uname(username)
    return data[5] == "MEMBER"

def reject_membership(username):
    ''' menolak membership dan
    mengubah status membership serta mereset credit_card serta no_telp '''
    cmd = f"DELETE FROM pending_membership WHERE username = \"{username}\""
    mycursor.execute(cmd)
    mydb.commit()

    # reset account
    cmd = "UPDATE account SET account_status = \"CUSTOMER\", "
    cmd += f"no_telp = NULL, credit_card = NULL WHERE username = \"{username}\""
    mycursor.execute(cmd)
    mydb.commit()

def accept_membership(username):
    ''' menolak membership dan mengubah status
    membership serta mereset credit_card serta no_telp '''
    cmd = f"DELETE FROM pending_membership WHERE username = \"{username}\""
    mycursor.execute(cmd)
    mydb.commit()
    #set status membership to 1
    cmd = f"UPDATE account SET account_status = \"MEMBER\" WHERE username = \"{username}\""
    mycursor.execute(cmd)
    mydb.commit()

def get_pending_membership_by_id(req_id):
    ''' return data based on id '''
    cmd = f"SELECT * FROM pending_membership WHERE id = {req_id}"
    mycursor.execute(cmd)
    return mycursor.fetchone()

def get_all_pending_membership():
    ''' return all data '''
    cmd = "SELECT * FROM pending_membership"
    mycursor.execute(cmd)
    data = []
    for i in mycursor:
        data.append(i)
    data2 = []
    for j in data:
        tmp_data = [j[0], j[1],j[2]]
        tmp_acc = get_acc_by_uname(j[1])
        tmp_data.append(tmp_acc[3])
        tmp_data.append(tmp_acc[4])
        data2.append(tmp_data)
    return data2

def get_all_account():
    ''' return all data '''
    cmd = "SELECT * FROM account"
    mycursor.execute(cmd)
    data = []
    for i in mycursor:
        data.append(i)
    return data
