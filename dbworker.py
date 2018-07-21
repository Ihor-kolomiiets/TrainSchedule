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
