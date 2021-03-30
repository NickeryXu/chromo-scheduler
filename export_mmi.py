import shutil
import sqlite3
import os

# src_path = '/media/msd'
new_path = '/home/voyager/2103-bak/fix_target'
# month_path = '2103'
# db_name = 'scheduler.db'
# SQLITE3_CONNECTION_TIMEOUT = 30 # to reslove "database is locked"

# conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
# cursor = conn.cursor()

# cursor.execute("select scores.case_name, scores.sample_id from scores left join cases on cases.name=scores.case_name where cases.update_time>'2021-03-25'")
# cases = cursor.fetchall()
# for case_name, sample_id in cases:
#     try:
#         f_name = case_name + '.' + str(sample_id).zfill(3) + '.MMI'
#         ori_file = os.path.join(src_path, month_path, f_name)
#         tmp_file = os.path.join(new_path, f_name)
#         shutil.copy(ori_file, tmp_file)
#         # print(f'ori_file: {ori_file}, tmp_file: {tmp_file}')
#     except Exception as e:
#         print(e)
with open('/media/cs/fix_target.txt', 'w', encoding='utf-8') as f:
    filenames = [x + '\n' for x in os.listdir(new_path)]
    f.writelines(filenames)
