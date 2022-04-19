import enum
from dbhandler import create_connection
import random
import datetime

mydb = create_connection()

mycursor = mydb.cursor()

def get_logged_user():
    cmd = f"SELECT username FROM logged_user LIMIT 1"
    mycursor.execute(cmd)
    return mycursor.fetchone()[0]

current_username = get_logged_user()

class Category(enum.Enum):
    Kendaraan = 1
    Elektronik = 2

'''Input data rekaman jejak karbon'''
def input_data():
    nama_aktivitas = str(input('Nama Aktivitas: '))
    kategori = str(input('Jenis Aktivitas (Kendaraan / Elektronik): '))
    jumlah = int(input('Jumlah dalam KWh atau dalam Liter bensin: '))
    waktu = str(input('Waktu dalam format \"YYYY-MM-DD HH:MM:SS\": '))
    if waktu == '':
        ct = datetime.datetime.now()
        year = ct.date().year
        month = ct.date().month
        day = ct.date().day
        hour = ct.hour
        minute = ct.minute
        second = ct.second
        waktu = f"{year}-{month}-{day} {hour}:{minute}:{second}"
    if kategori == 'Kendaraan':
        data = (current_username, nama_aktivitas, Category.Kendaraan, jumlah, None, waktu)
    elif kategori == 'Elektronik':
        data = (current_username, nama_aktivitas, Category.Elektronik, None, jumlah, waktu)
    return data

''' generate random timestamp '''
def generate_timestamp():
    year = random.randint(2021, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    time = f"{year}-{month}-{day} {hour}:{minute}:{second}"
    return time

'''generate n random data'''
def generate_data(n):
    cmd = "INSERT INTO activity_history(username, nama_aktivitas, kategori, jumlah_bensin, total_watt, timestamp_key)"
    for i in range(n):
        waktu = generate_timestamp()
        value = random.randrange(1, 100)
        if i % 2 == 0:
            kategori = Category.Kendaraan
            data = (current_username, "Activity " + str(i), kategori, value, None, waktu)
        else:
            kategori = Category.Elektronik
            data = (current_username, "Activity " + str(i), kategori, None, value, waktu)
        cmd += f" VALUES (\"{data[0]}\", \"{data[1]}\", \"{str(data[2])}\", \"{data[3]}\", \"{data[4]}\", \"{data[5]}\");"
        mycursor.execute(cmd)
        mydb.commit()

'''add new activity data (one by one)'''
def add_activity(data):
    cmd = "INSERT INTO activity_history(username, nama_aktivitas, kategori, jumlah_bensin, total_watt, timestamp_key)"
    cmd += f" VALUES (\"{data[0]}\", \"{data[1]}\", \"{str(data[2])}\", \"{data[3]}\", \"{data[4]}\", \"{data[5]}\");"
    mycursor.execute(cmd)
    mydb.commit()

'''commit the changes in a data'''
def edit_activity(data):
    data2 = (data[2], data[3], data[4], data[5], data[6], data[0])
    cmd = f"UPDATE activity_history SET nama_aktivitas = \"{data2[0]}\", kategori = \"{data[1]}\", jumlah_bensin = \"{data[2]}\", total_watt = \"{data[3]}\", timestamp_key = \"{data[4]}\" WHERE username = \"{current_username}\" AND activityid = \"{data[5]}\""
    mycursor.execute(cmd)
    mydb.commit()

def delete_activity(data):
    cmd = f"DELETE FROM activity_history WHERE username = \"{current_username}\"  AND activityid = \"{data[0]}\""
    mycursor.execute(cmd)
    mydb.commit()

def get_recent_data(data_length):
    ''' get top n data based on the latest timestamp pass -99 to get all data '''
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\" ORDER BY timestamp_key DESC"
    if data_length!=-99:
        cmd += " LIMIT " + str(data_length)
    fetched_data = mycursor.execute(cmd)
    data = []
    for i in fetched_data:
        data.append(i)
    return data

def get_older_data(data_length):
    ''' get top n data based on the oldest timestamp pass -99 to get all data '''
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\" ORDER BY timestamp_key ASC"
    if data_length!=-99:
        cmd += " LIMIT " + str(data_length)
    fetched_data = mycursor.execute(cmd)
    data = []
    for i in fetched_data:
        data.append(i)
    return data

'''return a tuple of data based on the id'''
def get_data_from_id(activityid):
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\" AND activityid = {activityid}"
    mycursor.execute(cmd)
    return mycursor.fetchone()

def get_all_tips_and_tricks():
    ''' return all data '''
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\""
    mycursor.execute(cmd)
    data = []
    for i in mycursor:
        data.append(i)
    return data

'''
1 jumlah_bensin = 2.232 kg CO2 emission
1 total_watt = 0.233 kg CO2 emission
'''
def get_total_emission():
    cmd = f"SELECT SUM(jumlah_bensin), SUM(total_watt) FROM activity_history WHERE username = \"{current_username}\""
    mycursor.execute(cmd)
    return mycursor[0]*2.232 + mycursor[1]*0.233

def get_previous_day_emission(n):
    cmd = f"SELECT SUM(jumlah_bensin), SUM(total_watt) FROM activity_history WHERE username = \"{current_username}\" AND DATEDIFF(NOW(), timestamp_key) <= {n}"
    mycursor.execute(cmd)
    return mycursor[0]*2.232 + mycursor[1]*0.233

def get_previous_week_emission(n):
    return get_previous_day_emission(n*7)

def get_previous_month_emission(n):
    return get_previous_day_emission(n*30)