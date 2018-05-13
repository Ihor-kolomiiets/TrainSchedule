import config
import mysql.connector


def push_to_db(station_info):
    conn = mysql.connector.connect(user=config.user, password=config.password,
                                   host=config.host, database=config.stations_database)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stations (id, ua_name, ru_name, en_name) VALUES (%d, %s, %s, %s)", station_info)
    conn.commit()
    cursor.close()
    conn.close()