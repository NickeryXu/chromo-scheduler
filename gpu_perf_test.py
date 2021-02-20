# on 1080Ti: total: 35.42738127708435s, avg: 0.03542738127708435s, fps: 28.22675467257396
# on 1080Ti bathsize=8: total: 25.644643783569336s, avg: 0.03205580472946167s, fps: 31.195598065299095
import time

from core_handler import *
from core_config import *

# consts
test_path = './test'
filename = 'test-{}.jpg'

test_round = 100
test_file = 8

# ai core
handler = CoreHandler(use_core)

image_path = os.path.join(test_path, filename)

tik = time.time()

for i in range(test_round):
    # with open(image_path, 'rb') as img:
    if test_file == 1:
        score = handler.get_score(image_path.format(0))
    else:
        scores = handler.get_all_scores([image_path.format(i) for i in range(test_file)])
        print(scores)

tok = time.time()

total_time = tok - tik
avg_time = total_time / (test_round * test_file)
fps = (test_round * test_file) / total_time

print('total: {}s, avg: {}s, fps: {}'.format(total_time, avg_time, fps))
