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
    files = [filename for filename in filenames if (filename[0] == start) and (filename[1] == '2')]
    files.sort()

    if files is None or len(files) == 0:
        return [], ''

    if last_file == '':
        last_index = -1
    else:
        last_index = binary_search(files, last_file)

    new_files = files[last_index + 1:]

    return new_files, files[-1]


def get_cases(new_files):
    cases = []
    case_files = {}

    for new_file in new_files:
        case_name, sample_id = split_filename(new_file)
        cases.append(case_name)

        if case_name in case_files:
            case_files[case_name].append(int(sample_id))
        else:
            case_files[case_name] = [int(sample_id)]

    return list(set(cases)), case_files


def create_case_score(case_name, sample_ids):
    return createCaseScore(db_name, case_name, sample_ids, LONG_STATUS['SCANNED'], -1)


def scan_list(src_path, src_ext, last_l_file, last_g_file):
    event_trick = time.time()
    m_path = month_path()

    if DEBUG:
        list_path = os.path.join(src_path, m_path)
        print('lister: list_path {}'.format(list_path))
        print('lister: last_l_file {}, last_g_file {}'.format(last_l_file, last_g_file))

    # list mmi files
    filenames = [filename for filename in os.listdir(os.path.join(src_path, m_path)) if src_ext in filename]

    if TRACK:
        print(f'Track Info: lister finish scanning files in {round(time.time() - event_trick, 2)}s')
        print(f'Track Info: Number of files: {len(filenames)}')
        with open('track_info.csv', 'a+', encoding='utf-8') as f:
            write_lines = [event_trick, ',', round(time.time() - event_trick, 2), ',', len(filenames), ',']
            f.writelines([str(x) for x in write_lines])
        event_trick = time.time()

    if DEBUG:
        print('lister: got {} available files'.format(len(filenames)))

    if len(filenames) == 0:
        return last_l_file, last_g_file

    # filter
    new_l_files, _last_l_file = filter_file(filenames, 'L', last_l_file)
    new_g_files, _last_g_file = filter_file(filenames, 'G', last_g_file)

    if TRACK:
        print(f'Track Info: lister finish filterring files in {round(time.time() - event_trick, 2)}s')
        print(f'Track Info: Number of new_l_files: {len(new_l_files)}')
        print(f'Track Info: Number of new_g_files: {len(new_g_files)}')
        with open('track_info.csv', 'a+', encoding='utf-8') as f:
            write_lines = [round(time.time() - event_trick, 2), ',', len(new_l_files), ',', len(new_g_files), ',']
            f.writelines([str(x) for x in write_lines])
        event_trick = time.time()

    # get cases
    new_l_cases, l_case_files = get_cases(new_l_files)
    new_g_cases, g_case_files = get_cases(new_g_files)

    if TRACK:
        print(f'Track Info: lister finish getting cases in {round(time.time() - event_trick, 2)}s')
        print(f'Track Info: Number of new_l_cases: {len(new_l_cases)}')
        print(f'Track Info: Number of new_g_cases: {len(new_g_cases)}')
        with open('track_info.csv', 'a+', encoding='utf-8') as f:
            write_lines = [round(time.time() - event_trick, 2), ',', len(new_l_cases), ',', len(new_g_cases), ',']
            f.writelines([str(x) for x in write_lines])
        event_trick = time.time()

    if DEBUG:
        print('lister: got {} new_l_cases'.format(len(new_l_cases)))
        print('lister: got {} new_g_cases'.format(len(new_g_cases)))

    # check and create new cases
    [createNewCase(db_name, case_name, m_path) for case_name in new_l_cases]
    [createNewCase(db_name, case_name, m_path) for case_name in new_g_cases]

    if TRACK:
        print(f'Track Info: lister finish creating new cases in {round(time.time() - event_trick, 2)}s')
        with open('track_info.csv', 'a+', encoding='utf-8') as f:
            write_lines = [round(time.time() - event_trick, 2), ',']
            f.writelines([str(x) for x in write_lines])

    # update scan count
    [create_case_score(case_name, sample_ids) for case_name, sample_ids in l_case_files.items()]
    [create_case_score(case_name, sample_ids) for case_name, sample_ids in g_case_files.items()]

    if TRACK:
        print(f'Track Info: lister finish updating scan count in {round(time.time() - event_trick, 2)}s')
        with open('track_info.csv', 'a+', encoding='utf-8') as f:
            write_lines = [round(time.time() - event_trick, 2), ',']
            f.writelines([str(x) for x in write_lines])

    return _last_l_file, _last_g_file
