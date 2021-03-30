import os
import shutil

# case_name = 'L2103123132'
mmi_path = '\\\\Think-pc\\MSD\\2103'
target_file = '\\\\Think-pc\\cs\\fix_target.txt'
fix_path = 'fix'

def read_filename(case_name, sample_id_str, mmi_path):
    with open(os.path.join(mmi_path, '{}.{}.MMI'.format(case_name, sample_id_str)), 'rb') as file:
        s = file.read(500)
        
        start = s.find(case_name.encode())
        end = start + len(case_name) + 8
        
        file_s = s[start:end]
        
        return file_s.decode()

if __name__ == '__main__':
    if not os.path.exists(fix_path):
        os.makedirs(fix_path)
        
    # filenames = [filename for filename in os.listdir(mmi_path) if (case_name in filename) and ('MMI' in filename)]
    # filenames = os.listdir(mmi_path)
    
    with open(target_file, 'r') as target:
        targets = target.readlines()
        targets = [t.strip() for t in targets]
    
    for filename in targets:
        case_name, sample_id_str, _ = filename.split('.')
        real_filename = read_filename(case_name, sample_id_str, mmi_path)
        print('{} -> {}'.format(filename, real_filename))
        
        ori_file = os.path.join(mmi_path, filename)
        fix_file = os.path.join(fix_path, real_filename)
        
        if not os.path.exists(fix_file):
            shutil.copy(ori_file, fix_file)
        