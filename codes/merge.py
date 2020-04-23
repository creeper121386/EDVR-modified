# 参数和crop.py保持一致

import PIL.Image as Image
import os
import glob

origin_sample = '/data1/why/EDVR/datasets/low_light_enhancement'
target = '/data1/why/EDVR/datasets/small'

h, w,  = 2026, 3840
sz = (256, 256)
n1 = h//sz[0]
n2 = w//sz[1]

for x in 