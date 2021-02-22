import os
import sys
import time
import logging
import shutil
from datetime import datetime
import traceback

from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

from db_ops import *
from consts import *
from utils import *

class DestHandler(FileSystemEventHandler):
    def on_created(self, event):
        super(DestHandler, self).on_created(event)

        if not event.is_directory:
            filename = os.path.basename(event.src_path)

            if check_ext(filename, EXPORT_EXT):
                case_name, sample_id = split_filename(filename)

                # update status
                updateScoreStatus(db_name, case_name, sample_id, LONG_STATUS['EXPORTED'])
                status, scan_count, export_count, _ = getCaseStatus(db_name, case_name)

                if status == STATUS['SCANNING']:
                    updateCaseStatus(db_name, case_name, STATUS['EXPORTING'])
                elif status == STATUS['EXPORTING']:
                    if (scan_count == 0) and (export_count > 0):
                        updateCaseStatus(db_name, case_name, STATUS['MOVING'])         
                else:
                    # TODO : if export is too close to scan, we may get NEW status

                    print('DestHandler::on_created error, unexpected status: {}'.format(list(STATUS.keys())[status]))
                    return

if __name__ == "__main__":
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    dest_handler = DestHandler()
    observer = Observer()
    observer.schedule(dest_handler, export_path, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
