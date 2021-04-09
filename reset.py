from consts import LONG_STATUS, STATUS, SQLITE3_CONNECTION_TIMEOUT, db_name
import sqlite3


def reset_case():
    try:
        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
        cursor = conn.cursor()
        case_name = input('please input case_name:\n')
        count_case = cursor.execute(f'select count(*) from cases where name="{case_name}"').fetchone()
        if not count_case:
            raise sqlite3.OperationalError
        count_score = cursor.execute(f'select count(*) from scores where case_name="{case_name}"').fetchone()
        action = input(f'Info: find {count_score[0]} scores\npress Y/y to reset; press other key to quit\n')
        if action == 'Y' or action == 'y':
            # 更新scores表中score为-1, status为SCANNED/0
            cursor.execute(
                f'update scores set score={-1}, status={LONG_STATUS["SCANNED"]} where case_name="{case_name}"')
            # 回滚cases表中status状态为SCANNING/1
            cursor.execute(f'update cases set status={STATUS["SCANNING"]} where case_name="{case_name}"')
            conn.commit()
            print('Info: Reset Success')
        else:
            return None
    except sqlite3.OperationalError as e:
        print(e)
        print("Error: could not find target case in database")


if __name__ == '__main__':
    reset_case()
