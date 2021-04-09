from apscheduler.schedulers.blocking import BlockingScheduler
from lister import month_path, filter_file
from consts import src_path, SRC_EXT, DEBUG, export_path, backup_path, backup_db_name, SQLITE3_CONNECTION_TIMEOUT
import os
import shutil
import sqlite3

# 阻塞调度
scheduler = BlockingScheduler()


def scan_list(src_path, src_ext, last_l_file, last_g_file):
    m_path = month_path()

    if DEBUG:
        list_path = os.path.join(src_path, m_path)
        print('lister: list_path {}'.format(list_path))
        print('lister: last_l_file {}, last_g_file {}'.format(last_l_file, last_g_file))

    # list mmi files
    filenames = [filename for filename in os.listdir(os.path.join(src_path, m_path)) if src_ext in filename]
    if DEBUG:
        print('lister: got {} available files'.format(len(filenames)))

    if len(filenames) == 0:
        return last_l_file, last_g_file

    new_l_files, _last_l_file = filter_file(filenames, 'L', last_l_file)
    new_g_files, _last_g_file = filter_file(filenames, 'G', last_g_file)

    conn = sqlite3.connect(backup_db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=SQLITE3_CONNECTION_TIMEOUT)
    cursor = conn.cursor()

    try:
        # 备份不需要区分
        for filename in new_l_files + new_g_files:
            shutil.copy(os.path.join(export_path, filename), os.path.join(backup_path, filename))
            # todo 数据库记录，更新last_filename
            cursor.execute('')
    except KeyboardInterrupt:
        # 保存中断前的更新记录
        conn.commit()
        raise KeyboardInterrupt
    return _last_l_file, _last_g_file


def list_and_backup_job():
    last_l_mmi = ''
    last_g_mmi = ''
    last_l_mmi, last_g_mmi = scan_list(
        src_path, SRC_EXT,
        last_l_mmi, last_g_mmi
    )


scheduler.add_job(list_and_backup_job, 'interval', minutes=5)
scheduler.start()
