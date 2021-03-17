import os
import glob
import sys
import time
import logging
import shutil
from datetime import datetime
import traceback

from db_ops import *
from consts import *
from utils import *

def filter_file(filenames, start):
    files = [filename for filename in filenames if filename[0] == start]
    files.sort()

    return files

# re-exporting - reset case and scores to beginning of exporting status
def reset_export(db_name, case_name, sample_id):
    status, scan_count, export_count, score_count = getCaseStatus(db_name, case_name)

    # 1. reset scores
    scores = getScores(db_name, case_name, LONG_STATUS['SCORED'])
    sample_ids = [sid for _, _, sid, _, _, _ in scores]

    removeCaseScores(db_name, case_name, LONG_STATUS['SCORED'])
    createCaseScore(db_name, case_name, sample_ids, LONG_STATUS['SCANNED'], -1.)

    # 2. export current score
    updateScoreStatus(db_name, case_name, int(sample_id), LONG_STATUS['EXPORTED'])

    # 3. reset case status
    updateCaseStatus(db_name, case_name, STATUS['EXPORTING'])

def update_score(filename):
    case_name, sample_id = split_filename(filename)
    status, scan_count, export_count, score_count = getCaseStatus(db_name, case_name)
    
    if status == STATUS['SCANNING']:
        updateScoreStatus(db_name, case_name, int(sample_id), LONG_STATUS['EXPORTED'])
        updateCaseStatus(db_name, case_name, STATUS['EXPORTING'])
    elif (status == STATUS['EXPORTING']) and (scan_count == 0) and (export_count > 0):
        updateScoreStatus(db_name, case_name, int(sample_id), LONG_STATUS['EXPORTED'])
        updateCaseStatus(db_name, case_name, STATUS['MOVING'])
    else:
        reset_export(db_name, case_name, sample_id)

def export_scheduler(export_path, export_ext):
    # list export files
    filenames = [filename for filename in os.listdir(export_path) if export_ext in filename]
    
    if DEBUG:
        print('scheduler: got {} available files'.format(len(filenames)))

    if len(filenames) == 0:
        return

    # filter
    new_l_files = filter_file(filenames, 'L')
    new_g_files = filter_file(filenames, 'G')

    if DEBUG:
        print('scheduler: got {} new_l_files'.format(len(new_l_files)))
        print('scheduler: got {} new_g_files'.format(len(new_g_files)))

    # update export count
    [update_score(new_l_file) for new_l_file in new_l_files]
    [update_score(new_g_file) for new_g_file in new_g_files]

    return
