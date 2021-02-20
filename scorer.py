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

def score_case(case_name):
    try:
        status, scan_count, score_count = getCaseStatus(db_name, case_name)

        if status == STATUS['SCORING']:
            if scan_count == score_count:
                # score case in batch
                filenames = ['{}.{}.{}'.format(case_name, i, DEST_EXT) for i in range(score_count)]
                img_paths = [os.path.join(export_path, filename) for filename in filenames]

                scores = handler.get_all_scores(img_paths)
                [updateScore(db_name, case_name, i, score) for i, score in enumerate(scores)]

                updateCaseStatus(db_name, case_name, STATUS['SORTING'])
            else:
                print('score_case error, mismatched scan_count / score_count: {} / {}'.format(
                    scan_count,
                    score_count
                ))
        else:
            print('score_case error, unexpected status: {}'.format(status))
    except Exception as err:
        print('score_case error: {}'.format(err))

if __name__ == '__main__':
    tik = time.time()

    # check scoring cases
    cases = getCasesByStatus(db_name, STATUS['SCORING'])

    if len(cases) > 0:
        [score_case(case_name) for _, case_name, _, _, _, _ in cases]

    tok = time.time()
    duration = tok - tik

    sleep_time = SCORE_CHECK_INTERVAL - duration

    if sleep_time > 0:
        time.sleep(sleep_time)