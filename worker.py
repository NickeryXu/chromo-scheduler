import os
import sys
import time
import logging
import shutil
from datetime import datetime
import traceback

from db_ops import *
from consts import *

from lister import scan_list
from scheduler import export_scheduler
from mover import move_case
from scorer import score_case
from sorter import sort_case

if __name__ == '__main__':
    last_l_mmi = ''
    last_g_mmi = ''

    while True:
        tik = time.time()
        
        try:
            # list
            last_l_mmi, last_g_mmi = scan_list(
                src_path, SRC_EXT,
                last_l_mmi, last_g_mmi
            )

            # schedule
            export_scheduler(
                export_path, EXPORT_EXT
            )
            if TRACK:
                track_time = time.time()
            # move
            cases = getCasesByStatus(db_name, STATUS['MOVING'])

            if len(cases) > 0:
                [move_case(case_name, export_path, dest_path) for _, case_name, _, _, _, _ in cases]
            
            if TRACK and len(cases) > 0:
                print(f'Track Info: mover finish {len(cases)} times work in {round(time.time() - track_time, 2)}s')
                print(f'Track Info: Every move spend {round((time.time() - track_time) / len(cases), 2)}s')
                with open('track_info.csv', 'a+', encoding='utf-8') as f:
                    write_lines = [len(cases), ',', round(time.time() - track_time, 2), ',']
                    f.writelines([str(x) for x in write_lines])
                track_time = time.time()
            elif TRACK:
                with open('track_info.csv', 'a+', encoding='utf-8') as f:
                    write_lines = [0, ',', None, ',']
                    f.writelines([str(x) for x in write_lines])
                track_time = time.time()

            # score
            cases = getCasesByStatus(db_name, STATUS['SCORING'])

            if len(cases) > 0:
                [score_case(case_name, dest_path, EXPORT_EXT) for _, case_name, _, _, _, _ in cases]

            if TRACK and len(cases) > 0:
                print(f'Track Info: scorer finish {len(cases)} times work in {round(time.time() - track_time, 2)}s')
                print(f'Track Info: Every score spend {round((time.time() - track_time) / len(cases), 2)}s')
                with open('track_info.csv', 'a+', encoding='utf-8') as f:
                    write_lines = [len(cases), ',', round(time.time() - track_time, 2), ',']
                    f.writelines([str(x) for x in write_lines])
                track_time = time.time()
            elif TRACK:
                with open('track_info.csv', 'a+', encoding='utf-8') as f:
                    write_lines = [0, ',', None, ',']
                    f.writelines([str(x) for x in write_lines])
                track_time = time.time()

            # sort
            cases = getCasesByStatus(db_name, STATUS['SORTING'])

            if len(cases) > 0:
                for _, case_name, _, month_path, _, _ in cases:
                    sorted_sample_ids = sortCaseByScore(db_name, case_name)
                    sort_case(src_path, tmp_path, case_name, sorted_sample_ids, SRC_EXT, month_path)
            
            if len(cases) > 0 and TRACK and not SORT_SIMULATION:
                # 统计进入实际排序的时长
                print(f'Track Info: sorter finish {len(cases)} times work in {round(time.time() - track_time, 2)}s')
                print(f'Track Info: Every sort spend {round((time.time() - track_time) / len(cases), 2)}s')
                with open('track_info.csv', 'a+', encoding='utf-8') as f:
                    write_lines = [len(cases), ',', round(time.time() - track_time, 2), ',']
                    f.writelines([str(x) for x in write_lines])
            elif TRACK:
                with open('track_info.csv', 'a+', encoding='utf-8') as f:
                    write_lines = [None, ',', None, ',', time.time(), '\n']
                    f.writelines([str(x) for x in write_lines])

        except Exception as err:
            print('worker error: {}'.format(err))
            traceback.print_exc()
        finally:
            tok = time.time()
            duration = tok - tik

            sleep_time = WORKER_CHECK_INTERVAL - duration

            if DEBUG:
                print('worker sleep time: {}s\n'.format(sleep_time))

            if sleep_time > 0:
                time.sleep(sleep_time)
