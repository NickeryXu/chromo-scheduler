import os
import sys
import time
import shutil
from pathlib import Path

from consts import *
from utils import *

# configs
l_cases = 5
l_samples_per_case = 10
g_cases = 10
g_samples_per_case = 10

# consts
test_pic_path = './test/pic'
test_pic_ext = 'jpg'

def create_mmi(mmi_path, type, case, samples_per_case, ext):
    for sample in range(samples_per_case):
        Path(os.path.join(mmi_path, '{}{:03d}.{:03d}.{}'.format(type, case+1, sample+1, ext))).touch()

    return

def create_export(export_path, type, case, samples_per_case, ext):
    for sample in range(samples_per_case):
        sample_file = os.path.join(export_path, '{}{:03d}.{:03d}.{}'.format(type, case+1, sample+1, ext))
        test_pic = os.path.join(test_pic_path, 'test-0.jpg')

        shutil.copy(test_pic, sample_file)

    return

def clean_mmi(mmi_path, type, case, samples_per_case, ext):
    for sample in range(samples_per_case):
        os.remove(os.path.join(mmi_path, '{}{:03d}.{:03d}.{}'.format(type, case+1, sample+1, ext)))

    return

def clean_export(export_path, type, case, samples_per_case, ext):
    for sample in range(samples_per_case):
        sample_file = os.path.join(export_path, '{}{:03d}.{:03d}.{}'.format(type, case+1, sample+1, ext))
        os.remove(sample_file)

    return

if __name__ == '__main__':
    argv = sys.argv

    if 'clean' in argv:
        print('clean mmi files')
        mmi_path = os.path.join(src_path, month_path())

        for case in range(l_cases):
            clean_mmi(mmi_path, 'L', case, l_samples_per_case, SRC_EXT)

        for case in range(g_cases):
            clean_mmi(mmi_path, 'G', case, g_samples_per_case, SRC_EXT)

        print('clean export files')
        for case in range(l_cases):
            clean_mmi(export_path, 'L', case, l_samples_per_case, test_pic_ext)

        for case in range(g_cases):
            clean_mmi(export_path, 'G', case, g_samples_per_case, test_pic_ext)
    else:
        print('create mmi files')
        mmi_path = os.path.join(src_path, month_path())

        if not os.path.exists(mmi_path):
            os.makedirs(mmi_path)

        for case in range(l_cases):
            create_mmi(mmi_path, 'L', case, l_samples_per_case, SRC_EXT)

        for case in range(g_cases):
            create_mmi(mmi_path, 'G', case, g_samples_per_case, SRC_EXT)

        time.sleep(3) # NEW status error workaround

        print('create export files')
        for case in range(l_cases):
            create_export(export_path, 'L', case, l_samples_per_case, test_pic_ext)

        for case in range(g_cases):
            create_export(export_path, 'G', case, g_samples_per_case, test_pic_ext)
