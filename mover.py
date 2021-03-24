import os
import sys
import time
import logging
import shutil
from datetime import datetime

from db_ops import *
from consts import *

def move_case(case_name, export_path, dest_path):
    try:
        if DEBUG:
            print('moving: {}'.format(case_name))
            
        status, scan_count, export_count, _ = getCaseStatus(db_name, case_name)

        if status == STATUS['MOVING']:
            if (scan_count == 0) and (export_count > 0):
                filenames = os.listdir(export_path)
                case_filenames = [filename for filename in filenames if case_name in filename]

                src_paths = [os.path.join(export_path, case_filename) for case_filename in case_filenames]
                dest_paths = [os.path.join(dest_path, case_filename) for case_filename in case_filenames]

                for s, d in zip(src_paths, dest_paths):
                    shutil.move(s, d)

                updateCaseStatus(db_name, case_name, STATUS['SCORING'])
            else:
                print('move_case error, unexpected scan_count / export_count: {} / {}'.format(
                    scan_count,
                    export_count
                ))

                # fix this situation
                if scan_count == 1:
                    scores = getScores(db_name, case_name, LONG_STATUS['SCANNED'])
                    _, _, sample_id, _, _, _ = scores[0]
                    updateScoreStatus(db_name, case_name, sample_id, LONG_STATUS['EXPORTED'])
        else:
            print('move_case error, unexpected status: {}'.format(status))
    except Exception as err:
        print('move_case error: {}'.format(err))

'''
if __name__ == '__main__':
    while True:
        tik = time.time()

        # check moving cases
        cases = getCasesByStatus(db_name, STATUS['MOVING'])

        if len(cases) > 0:
            [move_case(case_name, export_path, dest_path) for _, case_name, _, _, _, _ in cases]

        tok = time.time()
        duration = tok - tik

        sleep_time = MOVE_CHECK_INTERVAL - duration

        if sleep_time > 0:
            time.sleep(sleep_time)
'''
