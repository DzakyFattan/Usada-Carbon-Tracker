'''import random'''
import random
import lorem
from dbhandler import create_connection

mydb = create_connection()

mycursor = mydb.cursor()



def generate_timestamp():
    ''' generate random timestamp '''
    year = random.randint(2021, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    time = f"{year}-{month}-{day} {hour}:{minute}:{second}"
    return time


def generate_data(data_length):
    ''' generate n random data '''
    for i in range(data_length):
        cmd = "INSERT INTO tips_and_trick(judul, subtitle, konten, timestamp_key)"
        waktu_pesan = generate_timestamp()
        data = ("Tips and Trick" + str(i), "Tips and Trick" + str(i), lorem.sentence(), waktu_pesan)
        cmd += f" VALUES (\"{data[0]}\", \"{data[1]}\", \"{str(data[2])}\", \"{data[3]}\");"
        print(cmd)
        mycursor.execute(cmd)
        mydb.commit()


def add_tips_tricks_data(data):
    ''' add new tips and tricks data (one by one) '''
    cmd = "INSERT INTO tips_and_trick(judul, subtitle, konten, timestamp_key)"
    cmd +=  f" VALUES (\"{data[0]}\", \"{data[1]}\", \"{str(data[2])}\", \"{data[3]}\")"
    mycursor.execute(cmd)
    mydb.commit()

def edit_tips_tricks_data(data):
    ''' commit the changes in a data '''
    data2 = (data[1], data[2], data[3], data[4], data[0])
    cmd = f"UPDATE tips_and_trick SET judul = \"{data2[0]}\", subtitle = \"{data2[1]}\", "
    cmd += f"konten = \"{data2[2]}\", timestamp_key = \"{data2[3]}\" WHERE tntid = \"{data2[4]}\""
    mycursor.execute(cmd)
    mydb.commit()

def get_recent_data(data_length):
    ''' get top n data based on the latest timestamp pass -99 to get all data '''
    cmd = "SELECT * FROM tips_and_trick ORDER BY timestamp_key DESC"
    if data_length!=-99:
        cmd += " LIMIT " + str(data_length)
    fetched_data = mycursor.execute(cmd)
    data = []
    for i in fetched_data:
        data.append(i)
    return data

def get_older_data(data_length):
    ''' get top n data based on the oldest timestamp pass -99 to get all data '''
    cmd = "SELECT * FROM tips_and_trick ORDER BY timestamp_key ASC"
    if data_length!=-99:
        cmd += " LIMIT " + str(data_length)
    fetched_data = mycursor.execute(cmd)
    data = []
    for i in fetched_data:
        data.append(i)
    return data

def get_tips_tricks_by_id(id_tips):
    ''' return a tuple of data based on the id '''
    cmd = f"SELECT * FROM tips_and_trick WHERE tntid = {id_tips}"
    mycursor.execute(cmd)
    return mycursor.fetchone()

def del_tips_tricks_by_id(id_tips):
    ''' delete data based on the id '''
    cmd = f"DELETE FROM tips_and_trick WHERE tntid = {id_tips}"
    mycursor.execute(cmd)
    mydb.commit()

def get_all_tips_and_tricks():
    ''' return all data '''
    cmd = "SELECT * FROM tips_and_trick ORDER BY timestamp_key DESC"
    mycursor.execute(cmd)
    data = []
    for i in mycursor:
        data.append(i)
    return data
