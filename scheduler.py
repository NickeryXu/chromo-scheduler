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

def binary_search(sorted, target):
    if len(sorted) == 0:
        return -1

    l = 0
    r = len(sorted)

    while (l < r):
        mid = l + (r - l) // 2

        if sorted[mid] < target:
            l = mid + 1
        elif sorted[mid] > target:
            r = mid
        else:
            return mid

    if l == len(sorted) or sorted[l] != target:
        return -1

    return l

def filter_file(filenames, start, last_file):
    files = [filename for filename in filenames if filename[0] == start]
    files.sort()

    if files is None or len(files) == 0:
        return [], ''

    if last_file == '':
        last_index = -1
    else:
        last_index = binary_search(files, last_file)

    new_files = files[last_index+1:]

    return new_files, files[-1]

def update_score(filename):
    case_name, sample_id = split_filename(filename)
    updateScoreStatus(db_name, case_name, int(sample_id), LONG_STATUS['EXPORTED'])

    status, scan_count, export_count, score_count = getCaseStatus(db_name, case_name)

    if status == STATUS['SCANNING']:
        updateCaseStatus(db_name, case_name, STATUS['EXPORTING'])
    elif (status == STATUS['EXPORTING']) and (scan_count == 0) and (export_count > 0):
        updateCaseStatus(db_name, case_name, STATUS['MOVING'])

def export_scheduler(export_path, export_ext, last_l_file, last_g_file):
    # list export files
    filenames = [filename for filename in os.listdir(export_path) if export_ext in filename]
    
    if len(filenames) == 0:
        return last_l_file, last_g_file

    # filter
    new_l_files, _last_l_file = filter_file(filenames, 'L', last_l_file)
    new_g_files, _last_g_file = filter_file(filenames, 'G', last_g_file)

    if DEBUG:
        print('scheduler: got {} new_l_files'.format(len(new_l_files)))
        print('scheduler: got {} new_g_files'.format(len(new_g_files)))

    # update export count
    [update_score(new_l_file) for new_l_file in new_l_files]
    [update_score(new_g_file) for new_g_file in new_g_files]

    return _last_l_file, _last_g_file
