import os

from lister import *

# consts
count_path = '/media/msd/2103'
count_ext = 'MMI'

filenames = [filename for filename in os.listdir(count_path) if count_ext in filename]
print('total files: {}'.format(len(filenames)))

new_l_files, _ = filter_file(filenames, 'L', '')
new_g_files, _ = filter_file(filenames, 'G', '')

new_l_cases, _ = get_cases(new_l_files)
new_g_cases, _ = get_cases(new_g_files)

print('l files: {}, l cases: {}'.format(len(new_l_files), len(new_l_cases)))
print('g files: {}, g cases: {}'.format(len(new_g_files), len(new_g_cases)))
