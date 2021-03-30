from datetime import datetime


def check_ext(filename, ext='mmi'):
    if ext.upper() in filename.upper():
        return True

    return False


def split_filename(filename):
    arr = filename.split('.')
    case_name = arr[0]
    sample_id = arr[1]

    return case_name, sample_id


def month_path():
    now = datetime.now()
    path = now.strftime('%y%m')

    return path
