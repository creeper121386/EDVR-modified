import os
import os.path as osp
from tqdm import tqdm
import shutil
from PIL import Image
import sys

new_size = (960, 512)
# root = '/data1/why/EDVR/datasets/LLE-005-littleNum'
root = sys.argv[1]
if root[-1] == '/':
    root = root[:-1]
target = root + '.resize{}x{}'.format(*new_size)

def access(folder):
    print('access', folder)
    for x in os.listdir(folder):
        xpath = osp.join(folder, x)

        if osp.isdir(xpath):
            access(xpath)
        elif '.jpg' in xpath or '.png' in x:
            img = Image.open(xpath)
            # h, w = img.size
            # h //= scale
            # w //= scale
            # img = img.resize((h, w))
            img = img.resize(new_size)
            img.save(xpath)
        else:
            # other file types, remove it.
            os.remove(xpath)
            

if osp.exists(target):
    shutil.rmtree(target)
shutil.copytree(root, target)
access(target)