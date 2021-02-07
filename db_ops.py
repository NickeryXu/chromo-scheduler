from datetime import datetime
import sqlite3
from consts import *

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)

# cursor.execute('create table case(id integer autoincrement primary key, name varchar(50), status int, scan_count int, score_count int, [timestamp] create_time, [timestamp] update_time)')

def createNewCase(db_name, case_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where name=?', (case_name,))
        cases = cursor.fetchall()

        if len(cases) >= 1:
            print('createNewCase error, got {} case(s): {}'.format(len(cases), case_name))

            return False
        else:
            insert_tuple = (
                case_name,
                STATUS['SCANNING'],
                1
            )

            cursor.execute('''insert into cases (name, status, scan_count, create_time, update_time) values (?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))''', insert_tuple)
            conn.commit()

            cursor.close()

            return True
    except sqlite3.Error as error:
        print('createNewCase sqlite3 error, {}'.format(error))
        return False, 0, 0
    finally:
        if conn:
            conn.close()

def getCaseStatus(db_name, case_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where name=?', (case_name,))
        cases = cursor.fetchall()

        cursor.execute('select count(*) from scores where case_name=?', (case_name,))
        score_count = cursor.fetchone()[0]

        cursor.close()

        if len(cases) > 1:
            print('getCaseStatus error, got {} same cases: {}'.format(len(cases), case_name))
        elif len(cases) == 1:
            _, _, status, scan_count, _, _ = cases[0]

            return status, scan_count, score_count
        else:
            return STATUS['NEW'], 0, 0
    except sqlite3.Error as error:
        print('getCaseStatus sqlite3 error, {}'.format(error))
        return False, 0, 0
    finally:
        if conn:
            conn.close()

def updateCaseStatus(db_name, case_name, status):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where name=?', (case_name,))
        cases = cursor.fetchall()

        if len(cases) > 1:
            print('updateCaseStatus error, got {} case(s): {}'.format(len(cases), case_name))

            return False
        elif len(cases) == 1:
            case_id = cases[0][0]

            update_tuple = (
                status,
                case_id
            )

            cursor.execute('''update cases set status=?, update_time=datetime('now', 'localtime') where id=?''', update_tuple)

            conn.commit()

            return True
    except sqlite3.Error as error:
        print('updateCaseStatus sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

def incrementScanCount(db_name, case_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where name=?', (case_name,))
        cases = cursor.fetchall()

        if len(cases) > 1:
            print('incrementScanCount error, got {} case(s): {}'.format(len(cases), case_name))

            return False
        elif len(cases) == 1:
            case_id, _, case_status, case_scan_count, _, _ = cases[0]

            if case_status == STATUS['SCANNING']:
                update_tuple = (
                    case_scan_count+1,
                    case_id
                )

                cursor.execute('''update cases set scan_count=?, update_time=datetime('now', 'localtime') where id=?''', update_tuple)
                conn.commit()
                cursor.close()

                return True
            else: # status != STATUS['SCANNING']
                print('incrementScanCount error, desired status: SCANNING, actual status: {}'.format(case_status))
                cursor.close()

                return False
    except sqlite3.Error as error:
        print('incrementScanCount sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

# cursor.execute('create table score(id integer autoincrement primary key, case_name varchar(50), sample_id int, score real, [timestamp] create_time)')

def createNewScore(db_name, case_name, sample_id, score):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
    
        insert_tuple = (
            case_name,
            sample_id,
            score
        )
        cursor.execute('''insert into scores values (NULL, ?, ?, ?, datetime('now', 'localtime'))''', insert_tuple)
        conn.commit()

        cursor.close()

        return True
    except sqlite3.Error as error:
        print('createNewScore sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

def sortCaseByScore(db_name, case_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()

        cursor.execute('select * from scores where case_name=?', (case_name,))
        scores = cursor.fetchall()

        cursor.close()

        sample_ids = [score[2] for score in scores]
        score_list = [score[3] for score in scores]

        sorted_indices = argsort(score_list)
        sorted_indices.reverse()

        sorted_sample_ids = [sample_ids[index] for index in sorted_indices]

        return sorted_sample_ids
    except sqlite3.Error as error:
        print('sortCaseByScore sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()