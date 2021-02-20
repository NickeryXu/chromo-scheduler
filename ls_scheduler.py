import os
import sys
import time
import logging
import shutil
from datetime import datetime

from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

from db_ops import *
from consts import *

def check_ext(filename, ext='mmi'):
    if ext.upper() in filename.upper():
        return True

    return False

def split_filename(filename):
    arr = filename.split('.')
    case_name = arr[0]
    sample_id = arr[1]

    return case_name, sample_id

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

                # update case status
                createNewScore(db_name, case_name, int(sample_id), -1)
                status, scan_count, score_count = getCaseStatus(db_name, case_name)

                if status == STATUS['SCANNING']:
                    updateCaseStatus(db_name, case_name, STATUS['EXPORTING'])
                elif status == STATUS['EXPORTING']:
                    if scan_count == score_count:
                        updateCaseStatus(db_name, case_name, STATUS['MOVING'])         
                else:
                    print('DestHandler::on_created error, unexpected status: {}'.format(status))
                    return

if __name__ == "__main__":
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    if not os.path.exists(export_path):
        os.makedirs(export_path)

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
