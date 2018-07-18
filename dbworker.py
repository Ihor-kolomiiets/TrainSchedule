import config
import mysql.connector


def push_to_db(station_info):
    conn = mysql.connector.connect(user=config.user, password=config.password,
                                   host=config.host, database=config.stations_database)
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO stations_new (id, ua_station_name, region) VALUES (%s, %s, %s)", station_info)
    conn.commit()
    print('OK: ', station_info[0])
    cursor.close()
    conn.close()


def push_to_region(station_info):
    conn = mysql.connector.connect(user=config.user, password=config.password,
                                   host=config.host, database=config.stations_database)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO region (id, ua_region_name, ru_region_name, en_region_name) VALUES (%s, %s, %s, %s)",
                   station_info)
    conn.commit()
    print('OK: ', station_info[0])
    cursor.close()
    conn.close()


def find_train(search_pattern):
    conn = mysql.connector.connect(user=config.user, password=config.password,
                                   host=config.host, database=config.stations_database)
    cursor = conn.cursor()
    cursor.execute("SELECT id, ua_station_name FROM stations_new WHERE ua_station_name LIKE '%%%s%%'" % search_pattern)
    return cursor.fetchone()