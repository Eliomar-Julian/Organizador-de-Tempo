import sqlite3 as sql

def ler_database():
    query = sql.connect('./db/data.db')
    cursor = query.cursor()
    cursor.execute('SELECT * FROM alarmes;')
    dict_alarmes = dict()
    for alarm in cursor.fetchall():
        dict_alarmes[str(alarm[0])] = list(alarm)
    query.close()

    return dict_alarmes
