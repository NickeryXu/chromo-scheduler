import os
import sys
import time
import logging
import shutil
from datetime import datetime

from core_handler import *
from core_config import *

from db_ops import *
from consts import *

# ai core
handler = CoreHandler(activate_core_name)

def score_case(case_name, dest_path, export_ext, rescore=False):
    try:
        if DEBUG:
            print('scoring: {}'.format(case_name))

        status, scan_count, export_count, _ = getCaseStatus(db_name, case_name)

        if rescore == False:
            if status == STATUS['SCORING']:
                if (scan_count == 0) and (export_count > 0):
                    # score case in batch
                    filenames = ['{}.{:03d}.A.{}'.format(case_name, i+1, export_ext) for i in range(export_count)]
                    img_paths = [os.path.join(dest_path, filename) for filename in filenames]

                    scores = handler.get_all_scores(img_paths)
                    [updateScore(db_name, case_name, i+1, score) for i, score in enumerate(scores)]

                    updateCaseStatus(db_name, case_name, STATUS['SORTING'])
                else:
                    print('score_case error, mismatched scan_count / export_count: {} / {}'.format(
                        scan_count,
                        export_count
                    ))
            else:
                print('score_case error, unexpected status: {}'.format(status))
        else:
            # TODO : re-score case
            pass
    except Exception as err:
        print('score_case error: {}'.format(err))

'''
if __name__ == '__main__':
    while True:
        tik = time.time()

        # check scoring cases
        cases = getCasesByStatus(db_name, STATUS['SCORING'])

        if len(cases) > 0:
            [score_case(case_name) for _, case_name, _, _, _ in cases]

        tok = time.time()
        duration = tok - tik

        sleep_time = SCORE_CHECK_INTERVAL - duration

        if sleep_time > 0:
            time.sleep(sleep_time)
'''
