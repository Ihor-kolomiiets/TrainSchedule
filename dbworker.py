import config
import sqlite3


# Set FSM value to db
def set_state(user_id, state):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('SELECT state FROM user_info WHERE user_id=?', (user_id, ))
    db_state = cursor.fetchone()
    if db_state[0] is None:
        cursor.execute('INSERT INTO user_info (user_id, state) VALUES (?, ?)', (user_id, state))
    else:
        cursor.execute('UPDATE user_info SET state=? WHERE user_id=?', (state, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True


# Get FSM value from db
def get_state(user_id):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('SELECT state FROM user_info WHERE user_id=?', (user_id, ))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result[0] is None:
        return False
    else:
        return result[0]


# Set department_id in db according to user select
def set_department_value(user_id, department_id):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('UPDATE user_info SET department_id=?, station_id=NULL WHERE user_id=?', (department_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_department_value(user_id):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('SELECT department_id FROM user_info WHERE user_id=?', (user_id, ))
    department_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return department_id[0]


# Fetch 4 station which name start from station_name for 2 different table
def fetch_stations(station_name, user_id):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('SELECT department_id FROM user_info WHERE user_id=?', (user_id, ))
    department_id = cursor.fetchone()
    if department_id[0] == 1:
        cursor.execute('SELECT stations.station_id, stations.name_ru, regions.name_ru '
                       'FROM stations INNER JOIN regions ON regions.id = stations.region_id '
                       'AND stations.name_ru LIKE ? ORDER BY stations.name_ru', (station_name.upper() + '%',))
    else:
        cursor.execute('SELECT lviv_stations.station_id, lviv_stations.name_ua, regions.name_ua '
                       'FROM lviv_stations INNER JOIN regions ON regions.id = lviv_stations.region_id '
                       'AND lviv_stations.name_ua LIKE ? ORDER BY lviv_stations.name_ua', (station_name.upper() + '%',))
    stations = cursor.fetchmany(4)
    print(stations)
    cursor.close()
    conn.close()
    return stations


# next two function using for save first station id nd using this id for route search
def add_first_station(user_id, station_id):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('UPDATE user_info SET station_id=? WHERE user_id=?', (station_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_first_station(user_id):
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    cursor.execute('SELECT station_id FROM user_info WHERE user_id=?', (user_id, ))
    station_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return station_id


# fetch_stations(input())
