import config
import sqlite3


def set_state(user_id, state):
    conn = sqlite3.connect(config.users_database)
    cursor = conn.cursor()
    cursor.execute('SELECT stage FROM stages WHERE user_id="%s"' % (str(user_id)))
    check = cursor.fetchone()
    if check is None:
        cursor.execute('INSERT INTO stages (user_id, stage) VALUES ("%s", "%s")' % (str(user_id), state))
        conn.commit()
    else:
        cursor.execute('UPDATE stages SET stage="%s" WHERE user_id="%s"' % (state, str(user_id)))
        conn.commit()
    cursor.close()
    conn.close()


def get_state(user_id):
    conn = sqlite3.connect(config.users_database)
    cursor = conn.cursor()
    cursor.execute('SELECT stage FROM stages WHERE user_id="%s"' % (str(user_id)))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result is None:
        return False
    else:
        return result[0]


def db_get(station_name):
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
    cursor.execute('SELECT station_id FROM stations WHERE name_ru="%s"' % station_name.upper())
    station_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return station_id


def fetch_stations(station_name):
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
    cursor.execute('SELECT stations.station_id, stations.name_ru, regions.name_ru '
                   'FROM stations INNER JOIN regions ON regions.id = stations.region_id '
                   'AND stations.name_ru LIKE ? ORDER BY stations.name_ru', (station_name.upper() + '%',))
    stations = cursor.fetchmany(4)
    print(stations)
    return stations


def add_first_station(user_id, station_id):
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO station_storage (user_id, station_id) VALUES ("%s", "%s")'
                   % (str(user_id), str(station_id)))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_first_station(user_id):
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
    cursor.execute('SELECT station_id FROM station_storage WHERE user_id="%s"' % str(user_id))
    station_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return station_id


# fetch_stations(input())
