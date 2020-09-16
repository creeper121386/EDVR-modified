import os.path as osp
import os
import sys
from PIL import Image
import numpy as np
from utils.util import ssim, calculate_psnr
import shutil

## test comment

maps = {
    'MVI_0549': [113, 1313],
    'MVI_0550': [100, 1300],

    'MVI_0551': [160, 760],
    'MVI_0552': [200, 800],

    'MVI_0553': [126, 926],
    'MVI_0554': [200, 1000],

    'MVI_0555': [187, 1187],
    'MVI_0556': [200, 1200],

    'MVI_0557': [215, 1015],
    'MVI_0558': [200, 1000]

    # generate eval data:
    # 'MVI_0457': [300, 600],
    # 'MVI_0458': [303, 603],
}


def align(folder):
    print('process', folder)
    xs = os.listdir(folder)
    xs.sort(key=lambda x: int(x.split('.')[0][5:]))

    last = None
    sum = []
    total = 0
    for i, x in enumerate(xs):
        x = osp.join(folder, x)
        # print(x)
        img = Image.open(x)
        h, w = img.size
        scale = 10
        h //= scale
        w //= scale
        img = img.resize((h, w))

        # img.save('./tmp.jpg')
        # import ipdb; ipdb.set_trace()

        img = np.array(img)
        if i == 0:
            last = img
            continue

        # check diff:
        # PSNR = calculate_psnr(img, last)
        PSNR = None
        SSIM = ssim(img, last)
        sum.append(SSIM)
        total += SSIM
        if total / i - SSIM > 0.008:
            print(f'{folder} - res: frame-{i}, SSIM: {SSIM}, mean-SSIM: {total/i}')
            break
        # print(f'{i}, {i-1}: SSIM: {SSIM}, mean-SSIM: {total/i}, PSNR: {PSNR}')
        # last = img
    return i


def mv(start, src, dst):
    assert type(start) == int

    begin = False
    i = 0
    xs = os.listdir(src)
    xs.sort(key=lambda x: int(x.split('.')[0][5:]))
    for x in xs:
        # print(f'mv: {x}')
        if f'frame{start}' not in x and not begin:
            continue
        elif f'frame{start}' in x:
            begin = True

        old_path = osp.join(src, x)

        new_name = f'frame{i}.jpg'
        new_path = osp.join(dst, new_name)
        shutil.copy(old_path, new_path)
        # print(f'mv: {old_path} -> {new_path}')
        i += 1


def mv_new(src, dst):
    folder = src.split('/')[-1]
    try:
        start, end = maps[folder]
    except:
        print('Err in access:', folder)
        return

    print(f'process: {src}, start: {start}, end: {end}')
    if start is None and end is None:
        return

    begin = False
    i = 0
    xs = os.listdir(src)
    xs.sort(key=lambda x: int(x.split('.')[0][14:]))
    for x in xs:
        if f'frame{end}.' in x:
            break

        if f'frame{start}.' not in x and not begin:
            continue
        elif f'frame{start}.' in x:
            begin = True

        old_path = osp.join(src, x)

        new_name = f'frame{i}.jpg'
        new_path = osp.join(dst, new_name)
        shutil.copy(old_path, new_path)
        # print(f'mv: {old_path} -> {new_path}')
        i += 1

# root = sys.argv[1]
# target = sys.argv[2]
# for folder in os.listdir(root):
#     src = osp.join(root, folder)
#     dst = osp.join(target, folder)
#     start = align(src)
#     print('get res:', start)
#     if not osp.exists(dst):
#         os.makedirs(dst)
#     mv(res, src, dst)


root = sys.argv[1]
target = sys.argv[2]
for folder in os.listdir(root):
    src = osp.join(root, folder)
    dst = osp.join(target, folder)
    if not osp.exists(dst):
        os.makedirs(dst)
    mv_new(src, dst)
