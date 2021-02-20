import os
import glob
import sys
import time
import logging
import shutil
from datetime import datetime

from db_ops import *
from consts import *

def binary_search(sorted, target):
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
    files = [filename for filename in filenames if filename[0] == start].sort()

    last_index = binary_search(files, last_file)

    new_files = []

    if last_index > 0:
        new_files = files[last_index+1:]

    return new_files, files[-1]

def get_cases(new_files):
    pass
    return []

if __name__ == '__main__':
    last_l_file = ''
    last_g_file = ''

    while True:
        tik = time.time()

        # list mmi files
        filenames = [filename for filename in os.listdir(src_path) if SRC_EXT in filename]

        # filter
        new_l_files = filter_file(filenames, 'L', last_l_file)
        new_g_files = filter_file(filenames, 'G', last_g_file)

        # get cases
        new_l_cases = get_cases(new_l_files)
        new_g_cases = get_cases(new_g_files)

        # this might be problemic for partially scanned cases
        # we should record detailed scanning progress in db
        
        # check and create new cases

        # update scan count
        

        tok = time.time()
        duration = tok - tik

        sleep_time = LIST_CHECK_INTERVAL - duration

        if sleep_time > 0:
            time.sleep(sleep_time)
