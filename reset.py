import shutil
import sqlite3
import os

src_path = '/voyager/home/2103-bak'
month_path = '2103'
new_path = '2103-bak02'
db_name = 'scheduler.db'
SQLITE3_CONNECTION_TIMEOUT = 30 # to reslove "database is locked"

conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
cursor = conn.cursor()

cursor.execute("select scores.case_name, scores.sample_id, scores.score from cases left join scores on cases.name=scores.case_name where cases.status=6 and cases.update_time >= '2021-03-25'")
cases = cursor.fetchall()
case_dict = {}
for case_name, sample_id, score in cases:
    if case_name not in case_dict:
        case_dict[case_name] = [{'sample_id': str(sample_id).zfill(3), 'score': score, 'case_name': case_name}]
    else:
        case_dict[case_name].append({'sample_id': str(sample_id).zfill(3), 'score': score, 'case_name': case_name})
for value in case_dict.values():
    value.sort(key=lambda x: x['score'], reverse=True)
    no = 1
    for x in value:
        x['No'] = str(no).zfill(3)
        no += 1
cursor.close()
# print(case_dict['L2103123132'])
for value in case_dict.values():
    for x in value:
        try:
            f_name = x['case_name'] + '.' + x['sample_id'] + '.MMI' 
            res_name = x['case_name'] + '.' + x['No'] + '.MMI'
            ori_file = os.path.join(src_path, month_path, f_name)
            tmp_file = os.path.join(src_path, new_path, res_name)
            # shutil.copy(ori_file, tmp_file)
            print(f'ori_file: {ori_file}\ntmp_file: {tmp_file}')
            break
        except OSError as e:
            if 'busy' in str(e):
                print(e)
                print(f'ori_file: {ori_file}\ntmp_file: {tmp_file}')
            else:
                print(e)
                raise KeyboardInterrupt
        except Exception as e:
            print(e)
    # break
