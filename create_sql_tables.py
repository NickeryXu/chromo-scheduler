import sqlite3

from consts import *

def create_sql_tables(db_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        cursor.execute('create table cases(id integer primary key autoincrement, name varchar(50), status int, scan_count int, create_time text, update_time text)')
        cursor.execute('create table scores(id integer primary key autoincrement, case_name varchar(50), sample_id int, score real, create_time text)')

        conn.commit()
    except sqlite3.Error as error:
        print('sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_sql_tables(db_name)
