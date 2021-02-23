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

def get_cases(new_files):
    cases = []

    for new_file in new_files:
        case_name, _ = split_filename(new_file)
        cases.append(case_name)

    return list(set(cases))

def create_score(filename):
    case_name, sample_id = split_filename(filename)

    return createNewScore(db_name, case_name, int(sample_id), LONG_STATUS['SCANNED'], -1)

def scan_list(src_path, src_ext, last_l_file, last_g_file):
    # list mmi files
    filenames = [filename for filename in os.listdir(os.path.join(src_path, month_path())) if src_ext in filename]
    
    if len(filenames) == 0:
        return last_l_file, last_g_file

    # filter
    new_l_files, _last_l_file = filter_file(filenames, 'L', last_l_file)
    new_g_files, _last_g_file = filter_file(filenames, 'G', last_g_file)

    # get cases
    new_l_cases = get_cases(new_l_files)
    new_g_cases = get_cases(new_g_files)

    # check and create new cases
    [createNewCase(db_name, case_name) for case_name in new_l_cases]
    [createNewCase(db_name, case_name) for case_name in new_g_cases]

    # update scan count
    [create_score(new_l_file) for new_l_file in new_l_files]
    [create_score(new_g_file) for new_g_file in new_g_files]

    return _last_l_file, _last_g_file
