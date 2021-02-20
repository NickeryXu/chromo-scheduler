STATUS = {
    'NEW': 0,
    'SCANNING': 1,
    'EXPORTING': 2,
    'MOVING': 3,
    'SCORING': 4,
    'SORTING': 5,
    'FINISHED': 6
}

# sqlite3
db_name = 'scheduler.db'

# lister
LIST_CHECK_INTERVAL = 30 # sec

# worker
WORKER_CHECK_INTERVAL = 10 # sec

# mover
MOVE_CHECK_INTERVAL = 10 # sec

# scorer
SCORE_CHECK_INTERVAL = 10 # sec

# sorter
SORT_CHECK_INTERVAL = 10 # sec
SORT_SIMULATION = True # VERY IMPORTANT! SET TO FALSE AFTER DEBUGGING!

# global config
src_path = '/media/msd'
dest_path = '/media/cs'
export_path = '/media/export'
tmp_path = './tmp'

SRC_EXT = 'mmi' # must consider case
DEST_EXT = 'JPG'
