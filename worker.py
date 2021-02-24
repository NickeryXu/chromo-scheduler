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
    
    last_l_export = ''
    last_g_export = ''

    while True:
        tik = time.time()
        
        try:
            # list
            last_l_mmi, last_g_mmi = scan_list(
                src_path, SRC_EXT,
                last_l_mmi, last_g_mmi
            )

            # schedule
            last_l_export, last_g_export = export_scheduler(
                export_path, EXPORT_EXT,
                last_l_export, last_g_export
            )

            # move
            cases = getCasesByStatus(db_name, STATUS['MOVING'])

            if len(cases) > 0:
                [move_case(case_name, export_path, dest_path) for _, case_name, _, _, _ in cases]

            # score
            cases = getCasesByStatus(db_name, STATUS['SCORING'])

            if len(cases) > 0:
                [score_case(case_name, dest_path, EXPORT_EXT) for _, case_name, _, _, _ in cases]

            # sort
            cases = getCasesByStatus(db_name, STATUS['SORTING'])

            if len(cases) > 0:
                for _, case_name, _, _, _ in cases:
                    sorted_sample_ids = sortCaseByScore(db_name, case_name)
                    sort_case(src_path, tmp_path, case_name, sorted_sample_ids, SRC_EXT)
        except Exception as err:
            print('worker error: {}'.format(err))
            traceback.print_exc()
        finally:
            tok = time.time()
            duration = tok - tik

            sleep_time = WORKER_CHECK_INTERVAL - duration

            if sleep_time > 0:
                time.sleep(sleep_time)
