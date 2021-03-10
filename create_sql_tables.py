import sqlite3

from consts import *

def create_sql_tables(db_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        cursor.execute('create table cases(id integer primary key autoincrement, name varchar(50), status int, create_time text, update_time text)')
        cursor.execute('create table scores(id integer primary key autoincrement, case_name varchar(50), sample_id int, status int, score real, create_time text)')

        conn.commit()
    except sqlite3.Error as error:
        print('sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()
def create_sql_web_tables(db_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()

        cursor.execute('create table users(id integer primary key autoincrement, name varchar(50), hash_password varchar(100), salt varchar(100), is_admin bool)')
        cursor.execute('create table setting(id integer primary key autoincrement, debug bool, src_path varchar(200), export_path varchar(200), dest_path varchar(200), tmp_path varchar(200), src_ext varchar(200), export_ext varchar(200), sort_simulation bool, worker_check_interval int)')

        conn.commit()
    except sqlite3.Error as error:
        print('sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()
if __name__ == '__main__':
    create_sql_tables(db_name)
    create_sql_web_tables(db_name)
