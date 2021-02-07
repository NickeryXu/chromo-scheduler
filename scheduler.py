import os
import sys
import time
import logging
import shutil
from datetime import datetime

from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

from core_handler import *
from core_config import *

from db_ops import *
from consts import *

# configs
src_path = '/media/msd'
dest_path = '/media/cs'
tmp_path = './tmp'

SRC_EXT = 'mmi' # must consider case
DEST_EXT = 'tiff'

# sqlite3
db_name = 'scheduler.db'

# ai core
handler = CoreHandler(use_core)

def check_ext(filename, ext='mmi'):
    if ext.upper() in filename.upper():
        return True

    return False

def split_filename(filename):
    arr = filename.split('.')
    case_name = arr[0]
    sample_id = arr[1]

    return case_name, sample_id

def sort_case(dest_path, tmp_path, case_name, sorted_sample_ids, ext):
    all_tmp_filenames = []

    for i, sorted_sample_id in enumerate(sorted_sample_ids):
        ori_filename = '{}.{:03d}.{}'.format(case_name, sorted_sample_id, ext)
        mod_filename = '{}.{:03d}.{}'.format(case_name, i+1, ext)

        ori_file = os.path.join(dest_path, ori_filename)
        tmp_file = os.path.join(tmp_path, mod_filename)

        all_tmp_filenames.append(tmp_file)

        shutil.move(ori_file, tmp_file)

    for tmp_file in all_tmp_filenames:
        base_filename = os.path.basename(tmp_file)
        dest_file = os.path.join(dest_path, base_filename)

        shutil.move(tmp_file, dest_file)

class SrcHandler(FileSystemEventHandler):
    def on_created(self, event):
        super(SrcHandler, self).on_created(event)

        if (not event.is_directory):
            filename = os.path.basename(event.src_path)
            
            if check_ext(filename, SRC_EXT):
                case_name, _ = split_filename(filename)
                status, _, _ = getCaseStatus(db_name, case_name)

                if (status == STATUS['NEW']):
                    createNewCase(db_name, case_name)
                elif (status == STATUS['SCANNING']):
                    incrementScanCount(db_name, case_name)
                elif (status == STATUS['SCORING']):
                    print('SrcHandler::on_created error, unexpected status: {}'.format(status))

class DestHandler(FileSystemEventHandler):
    def on_created(self, event):
        super(DestHandler, self).on_created(event)

        if not event.is_directory:
            filename = os.path.basename(event.src_path)

            if check_ext(filename, DEST_EXT):
                case_name, sample_id = split_filename(filename)
                status, _, _ = getCaseStatus(db_name, case_name)

                if status == STATUS['SCANNING']:
                    updateCaseStatus(db_name, case_name, STATUS['SCORING'])
                elif status != STATUS['SCORING']:
                    print('DestHandler::on_created error, unexpected status: {}'.format(status))
                    return

                # TODO : call celery task to get file score
                image_path = os.path.join(dest_path, filename)

                with open(image_path, 'rb') as img:
                    # score = handler.get_score(img)
                    import random
                    score = random.random()

                createNewScore(db_name, case_name, int(sample_id), score)
                _, scan_count, score_count = getCaseStatus(db_name, case_name)

                if scan_count == score_count:
                    updateCaseStatus(db_name, case_name, STATUS['SORTING'])
                    
                    sorted_sample_ids = sortCaseByScore(db_name, case_name)
                    sort_case(src_path, tmp_path, case_name, sorted_sample_ids, SRC_EXT)

                    updateCaseStatus(db_name, case_name, STATUS['FINISHED'])

if __name__ == "__main__":
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    src_handler = SrcHandler()
    dest_handler = DestHandler()

    observer = Observer()

    observer.schedule(src_handler, src_path, recursive=False)
    observer.schedule(dest_handler, dest_path, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
