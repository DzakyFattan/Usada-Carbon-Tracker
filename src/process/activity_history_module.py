'''Module to handle activity record'''
import enum
import random
import datetime
from dbhandler import create_connection

mydb = create_connection()

mycursor = mydb.cursor()

def get_logged_user():
    ''' return logged user '''
    cmd = "SELECT username FROM logged_user LIMIT 1"
    mycursor.execute(cmd)
    return mycursor.fetchone()[0]

class Category(enum.Enum):
    Kendaraan = 1
    Elektronik = 2

# def input_data():
#     '''Input data rekaman jejak karbon'''
#     nama_aktivitas = str(input('Nama Aktivitas: '))
#     kategori = str(input('Jenis Aktivitas (Kendaraan / Elektronik): '))
#     jumlah = int(input('Jumlah dalam KWh atau dalam Liter bensin: '))
#     waktu = str(input('Waktu dalam format \"YYYY-MM-DD HH:MM:SS\": '))
#     if waktu == '':
#         now = datetime.datetime.now()
#         year = now.date().year
#         month = now.date().month
#         day = now.date().day
#         hour = now.hour
#         minute = now.minute
#         second = now.second
#         waktu = f"{year}-{month}-{day} {hour}:{minute}:{second}"
#     if kategori == 'Kendaraan':
#         data = (current_username, nama_aktivitas, Category.Kendaraan, jumlah, None, waktu)
#     elif kategori == 'Elektronik':
#         data = (current_username, nama_aktivitas, Category.Elektronik, None, jumlah, waktu)
#     return data

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

def generate_data(count, current_username):
    '''generate n random data'''
    cmd = "INSERT INTO activity_history"
    cmd += "(username, nama_aktivitas, kategori, jumlah_bensin, total_watt, timestamp_key)"
    for i in range(count):
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

def add_activity(data):
    '''add new activity data (one by one)'''
    cmd = "INSERT INTO activity_history"
    cmd += "(username, nama_aktivitas, kategori, jumlah_bensin, total_watt, timestamp_key)"
    cmd += f" VALUES (\"{data[0]}\", \"{data[1]}\", \"{str(data[2])}\", \"{data[3]}\", \"{data[4]}\", \"{data[5]}\");"
    mycursor.execute(cmd)
    mydb.commit()

def edit_activity(data):
    '''commit the changes in a data'''
    data2 = (data[2], data[3], data[4], data[5], data[6], data[0])
    cmd = f"UPDATE activity_history SET nama_aktivitas = \"{data2[0]}\", kategori = \"{data[1]}\", jumlah_bensin = \"{data[2]}\", total_watt = \"{data[3]}\", timestamp_key = \"{data[4]}\" WHERE username = \"{current_username}\" AND activityid = \"{data[5]}\""
    mycursor.execute(cmd)
    mydb.commit()

def delete_activity(data):
    '''delete a data based on the id and username'''
    cmd = f"DELETE FROM activity_history WHERE activityid = \"{data[0]}\""
    mycursor.execute(cmd)
    mydb.commit()

def get_recent_data(data_length, current_username):
    ''' get top n data based on the latest timestamp pass -99 to get all data '''
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\" ORDER BY timestamp_key DESC"
    if data_length!=-99:
        cmd += " LIMIT " + str(data_length)
    fetched_data = mycursor.execute(cmd)
    data = []
    for i in fetched_data:
        data.append(i)
    return data

def get_older_data(data_length, current_username):
    ''' get top n data based on the oldest timestamp pass -99 to get all data '''
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\" ORDER BY timestamp_key ASC"
    if data_length!=-99:
        cmd += " LIMIT " + str(data_length)
    fetched_data = mycursor.execute(cmd)
    data = []
    for i in fetched_data:
        data.append(i)
    return data

def get_data_from_id(activityid):
    '''return a tuple of data based on the id'''
    cmd = f"SELECT * FROM activity_history WHERE activityid = {activityid}"
    mycursor.execute(cmd)
    return mycursor.fetchone()

def get_all_tips_and_tricks(current_username):
    ''' return all data '''
    cmd = f"SELECT * FROM activity_history WHERE username = \"{current_username}\""
    mycursor.execute(cmd)
    data = []
    for i in mycursor:
        data.append(i)
    return data


#1 jumlah_bensin = 2.232 kg CO2 emission
#1 total_watt = 0.233 kg CO2 emission

def get_total_emission(current_username):
    ''' return total emission '''
    cmd = f"SELECT SUM(jumlah_bensin), SUM(total_watt) FROM activity_history WHERE username = \"{current_username}\""
    mycursor.execute(cmd)
    return mycursor[0]*2.232 + mycursor[1]*0.233

def get_previous_day_emission(current_username,count):
    ''' return total emission for count days '''
    cmd = "SELECT SUM(jumlah_bensin), SUM(total_watt) FROM activity_history "
    cmd += f"WHERE username = \"{current_username}\" AND DATEDIFF(NOW(), timestamp_key) <= {count}"
    mycursor.execute(cmd)
    return mycursor[0]*2.232 + mycursor[1]*0.233

def get_previous_day_sum(current_username,count):
    ''' return total sum for count days '''
    cmd = "SELECT SUM(jumlah_bensin), SUM(total_watt) FROM activity_history "
    cmd += f"WHERE username = \"{current_username}\" AND DATEDIFF(NOW(), timestamp_key) <= {count}"
    mycursor.execute(cmd)
    return mycursor.fetchone()

def get_previous_day_count(current_username,count):
    ''' return total count for count days '''
    cmd = "SELECT COUNT(jumlah_bensin) FROM activity_history "
    cmd += f"WHERE username = \"{current_username}\" AND DATEDIFF(NOW(), timestamp_key) <= {count} AND kategori = 1"
    mycursor.execute(cmd)
    count_kendaraan = mycursor.fetchone()[0]
    data2 = []
    cmd = "SELECT COUNT(total_watt) FROM activity_history "
    cmd += f"WHERE username = \"{current_username}\" AND DATEDIFF(NOW(), timestamp_key) <= {count} AND kategori = 2"
    mycursor.execute(cmd)
    count_elektronik = mycursor.fetchone()[0]
    data2.append(count_kendaraan)
    data2.append(count_elektronik)
    return data2

def get_grades(current_username,count):
    ''' return grades based on the previous days' performance'''
    cmd = "SELECT SUM(jumlah_bensin), SUM(total_watt) FROM activity_history "
    cmd += f"WHERE username = \"{current_username}\" AND DATEDIFF(NOW(), timestamp_key) <= {count}"
    mycursor.execute(cmd)
    data1 = mycursor.fetchone()
    data2 = get_previous_day_count(current_username,count)
    
    if(data1[0]/data2[0] + data1[1]/data2[1]<= 1):
        return "A"
    elif(data1[0]/data2[0] + data1[1]/data2[1]<= 3):
        return "B"
    else:
        return "C"