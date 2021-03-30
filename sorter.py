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

        for i in range(len(sorted_sample_ids)):
            f_name = '{}.{:03d}.{}'.format(case_name, i + 1, ext)

            ori_file = os.path.join(dest_path, month_path, f_name)
            tmp_file = os.path.join(tmp_path, f_name)

            all_tmp_filenames.append(tmp_file)

            if not SORT_SIMULATION:
                shutil.move(ori_file, tmp_file)
            else:
                print('{} -> {}'.format(ori_file, tmp_file))

        for i, (tmp_file, sorted_sample_id) in enumerate(zip(all_tmp_filenames, sorted_sample_ids)):
            ori_filename = '{}.{:03d}.{}'.format(case_name, sorted_sample_id, ext)
            mod_filename = '{}.{:03d}.{}'.format(case_name, i + 1, ext)

            ori_file = os.path.join(tmp_path, ori_filename)
            mod_file = os.path.join(dest_path, month_path, mod_filename)

            if not SORT_SIMULATION:
                shutil.move(ori_file, mod_file)
            else:
                print('{} -> {}'.format(ori_file, mod_file))

        updateCaseStatus(db_name, case_name, STATUS['FINISHED'])
    except Exception as err:
        print('sort_case error: {}'.format(err))

        err_file = err.filename
        err_basename = os.path.basename(err_file)

        # list existed case MMI from tmp_path (fast)
        filenames = [filename for filename in os.listdir(tmp_path) if
                     (case_name in filename) and (err_basename not in filename)]

        # make a safty copy to backup_path (fast)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        for filename in filenames:
            ori_file = os.path.join(tmp_path, filename)
            copy_file = os.path.join(backup_path, filename)

            if not SORT_SIMULATION:
                shutil.copy(ori_file, copy_file)
            else:
                print('{} -> {}'.format(ori_file, copy_file))

        # mv from tmp to dest_path (slow)
        for filename in filenames:
            tmp_file = os.path.join(tmp_path, filename)
            dest_file = os.path.join(dest_path, month_path, filename)

            if not SORT_SIMULATION:
                shutil.move(tmp_file, dest_file)
            else:
                print('{} -> {}'.format(tmp_file, dest_file))

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
