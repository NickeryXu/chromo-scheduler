# on 1080Ti: total: 35.42738127708435s, avg: 0.03542738127708435s, fps: 28.22675467257396

import time

from core_handler import *
from core_config import *

# consts
test_path = './test'
filename = 'test.jpg'

test_round = 1000

# ai core
handler = CoreHandler(use_core)

image_path = os.path.join(test_path, filename)

tik = time.time()

for i in range(test_round):
    with open(image_path, 'rb') as img:
        score = handler.get_score(img)

tok = time.time()

total_time = tok - tik
avg_time = total_time / test_round
fps = test_round / total_time

print('total: {}s, avg: {}s, fps: {}'.format(total_time, avg_time, fps))
