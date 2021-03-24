import os
import sys
import time
import logging
import shutil
from datetime import datetime

from db_ops import *
from consts import *
from utils import *

def sort_case(dest_path, tmp_path, case_name, sorted_sample_ids, ext, month_path):
    try:
        if DEBUG:
            print('sorting: {}'.format(case_name))
            
        all_tmp_filenames = []

        for i, sorted_sample_id in enumerate(sorted_sample_ids):
            ori_filename = '{}.{:03d}.{}'.format(case_name, sorted_sample_id, ext)
            mod_filename = '{}.{:03d}.{}'.format(case_name, i+1, ext)

            ori_file = os.path.join(dest_path, month_path, ori_filename)
            tmp_file = os.path.join(tmp_path, mod_filename)

            all_tmp_filenames.append(tmp_file)

            if not SORT_SIMULATION:
                shutil.move(ori_file, tmp_file)
            else:
                print('{} -> {}'.format(ori_file, tmp_file))

        for tmp_file in all_tmp_filenames:
            base_filename = os.path.basename(tmp_file)
            dest_file = os.path.join(dest_path, month_path, base_filename)

            if not SORT_SIMULATION:
                shutil.move(tmp_file, dest_file)
            else:
                print('{} -> {}'.format(tmp_file, dest_file))

        updateCaseStatus(db_name, case_name, STATUS['FINISHED'])
    except Exception as err:
        print('sort_case error: {}'.format(err))
        updateCaseStatus(db_name, case_name, STATUS['SORTING'])

if __name__ == '__main__':
    while True:
        tik = time.time()

        # check sorting cases
        cases = getCasesByStatus(db_name, STATUS['SORTING'])

        if len(cases) > 0:
            for _, case_name, _, _, month_path, _, _ in cases:
                # 1. compute new id list
                sorted_sample_ids = sortCaseByScore(db_name, case_name)

                # 2. update db
                updateCaseScoreSampleIds(db_name, case_name, sorted_sample_ids)

                # 3. update file system
                sort_case(src_path, tmp_path, case_name, sorted_sample_ids, SRC_EXT, month_path)

        tok = time.time()
        duration = tok - tik

        sleep_time = SORT_CHECK_INTERVAL - duration

        if sleep_time > 0:
            time.sleep(sleep_time)
