DEBUG = True
TRACK = False

STATUS = {
    'NEW': 0,
    'SCANNING': 1,
    'EXPORTING': 2,
    'MOVING': 3,
    'SCORING': 4,
    'SORTING': 5,
    'FINISHED': 6
}

LONG_STATUS = {
    'SCANNED': 0,
    'EXPORTED': 1,
    'SCORED': 2
}

# sqlite3
db_name = './scheduler.db'
SQLITE3_CONNECTION_TIMEOUT = 30  # to reslove "database is locked"
backup_db_name = './backup.db'

# worker
WORKER_CHECK_INTERVAL = 10  # sec

# lister
LIST_CHECK_INTERVAL = 3  # sec

# scheduler
SCHEDULE_CHECK_INTERVAL = 3  # sec

# mover
MOVE_CHECK_INTERVAL = 10  # sec

# scorer
SCORE_CHECK_INTERVAL = 10  # sec

# sorter
SORT_CHECK_INTERVAL = 10  # sec
SORT_SIMULATION = True  # VERY IMPORTANT! SET TO FALSE AFTER DEBUGGING!

# global config
src_path = '/media/msd'
export_path = '/media/cs/test'
dest_path = '/media/scheduler'
tmp_path = './tmp'
backup_path = './backup'

SRC_EXT = 'MMI'  # must consider case
EXPORT_EXT = 'JPG'
