import os
import sys
import time
import logging
import shutil
from datetime import datetime

from db_ops import *
from consts import *

from mover import move_case
from scorer import score_case
from sorter import sort_case

if __name__ == '__main__':
    tik = time.time()

    # move
    cases = getCasesByStatus(db_name, STATUS['MOVING'])

    if len(cases) > 0:
        [move_case(case_name, dest_path, export_path) for _, case_name, _, _, _, _ in cases]

    # score
    cases = getCasesByStatus(db_name, STATUS['SCORING'])

    if len(cases) > 0:
        [score_case(case_name) for _, case_name, _, _, _, _ in cases]

    # sort
    cases = getCasesByStatus(db_name, STATUS['SORTING'])

    if len(cases) > 0:
        for _, case_name, _, _, _, _ in cases:
            sorted_sample_ids = sortCaseByScore(db_name, case_name)
            sort_case(src_path, tmp_path, case_name, sorted_sample_ids, SRC_EXT)

    tok = time.time()
    duration = tok - tik

    sleep_time = WORKER_CHECK_INTERVAL - duration

    if sleep_time > 0:
        time.sleep(sleep_time)
        