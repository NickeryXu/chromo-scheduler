from datetime import datetime
import sqlite3
from consts import *

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)

# cases

def createNewCase(db_name, case_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where name=?', (case_name,))
        cases = cursor.fetchall()

        if len(cases) > 0:
            # print('createNewCase error, got {} case(s): {}'.format(len(cases), case_name))
            return True
        else:
            insert_tuple = (
                case_name,
                STATUS['SCANNING']
            )

            cursor.execute('''insert into cases (name, status, create_time, update_time) values (?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))''', insert_tuple)
            conn.commit()

            cursor.close()

            return True
    except sqlite3.Error as error:
        print('createNewCase sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

def getCaseStatus(db_name, case_name):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where name=?', (case_name,))
        cases = cursor.fetchall()

        cursor.execute(
            'select count(*) from scores where case_name=? and status=?',
            (case_name, LONG_STATUS['SCANNED'])
        )
        scan_count = cursor.fetchone()[0]

        cursor.execute(
            'select count(*) from scores where case_name=? and status=?',
            (case_name, LONG_STATUS['EXPORTED'])
        )
        export_count = cursor.fetchone()[0]

        cursor.execute(
            'select count(*) from scores where case_name=? and status=?',
            (case_name, LONG_STATUS['SCORED'])
        )
        score_count = cursor.fetchone()[0]

        cursor.close()

        if len(cases) > 1:
            print('getCaseStatus error, got {} same cases: {}'.format(len(cases), case_name))
        elif len(cases) == 1:
            _, _, status, _, _ = cases[0]

            return status, scan_count, export_count, score_count
        else:
            return STATUS['NEW'], 0, 0, 0
    except sqlite3.Error as error:
        print('getCaseStatus sqlite3 error, {}'.format(error))
        return False, 0, 0, 0
    finally:
        if conn:
            conn.close()

def getCasesByStatus(db_name, status):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()
    
        cursor.execute('select * from cases where status=?', (status,))
        cases = cursor.fetchall()

        cursor.close()

        return cases
    except sqlite3.Error as error:
        print('getCaseStatus sqlite3 error, {}'.format(error))
        return None
    finally:
        if conn:
            conn.close()

def updateCaseStatus(db_name, case_name, status):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
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

# scores

def createNewScore(db_name, case_name, sample_id, status, score):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()

        # check if this score is already created
        cursor.execute('select * from scores where case_name=? and sample_id=?', (case_name, sample_id))
        scores = cursor.fetchall()

        if len(scores) > 0:
            # print('createNewScore error, got {} score(s): {}.{}'.format(len(scores), case_name, sample_id))
            return True
    
        insert_tuple = (
            case_name,
            sample_id,
            status,
            score
        )
        cursor.execute('''insert into scores values (NULL, ?, ?, ?, ?, datetime('now', 'localtime'))''', insert_tuple)
        conn.commit()

        cursor.close()

        return True
    except sqlite3.Error as error:
        print('createNewScore sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

def createCaseScore(db_name, case_name, sample_ids, status, score):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()

        cursor.execute(
            'select sample_id from scores where case_name=?',
            (case_name, )
        )
        existed_sample_ids = [id_tuple[0] for id_tuple in cursor.fetchall()]

        for sample_id in sample_ids:
            if sample_id not in existed_sample_ids:
                insert_tuple = (
                    case_name,
                    sample_id,
                    status,
                    score
                )
                cursor.execute('''insert into scores values (NULL, ?, ?, ?, ?, datetime('now', 'localtime'))''', insert_tuple)

        conn.commit()
        cursor.close()

        return True
    except sqlite3.Error as error:
        print('createCaseScore sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

def getScores(db_name, case_name, status):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()

        cursor.execute(
            'select * from scores where case_name=? and status=?',
            (case_name, status)
        )
        scores = cursor.fetchall()

        cursor.close()

        return scores
    except sqlite3.Error as error:
        print('getCaseStatus sqlite3 error, {}'.format(error))
        return None
    finally:
        if conn:
            conn.close()

def updateScore(db_name, case_name, sample_id, score):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()
    
        update_tuple = (
            LONG_STATUS['SCORED'],
            score,
            case_name,
            sample_id
        )
        cursor.execute(
            '''update scores set status=?, score=? where case_name=? and sample_id=?''',
            update_tuple
        )
        conn.commit()

        cursor.close()

        return True
    except sqlite3.Error as error:
        print('updateScore sqlite3 error, {}'.format(error))
        return False
    finally:
        if conn:
            conn.close()

def updateScoreStatus(db_name, case_name, sample_id, status):
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()
    
        update_tuple = (
            status,
            case_name,
            sample_id
        )
        cursor.execute(
            '''update scores set status=? where case_name=? and sample_id=?''',
            update_tuple
        )
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
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
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
