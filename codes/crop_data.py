import numpy as np
# from patchify import patchify, unpatchify
import PIL.Image as Image
import os
import glob

'''
a video folder -> many cropped-video folders
'''

## 这里的俩路径末尾不能有 `/`
root = '/data1/why/EDVR/datasets/low_light_enhancement'
target = '/data1/why/EDVR/datasets/small'

def crop(path):
    name = os.path.basename(path).split('.')[0]
    dirname = os.path.dirname(path)
    img = np.array(Image.open(path))

    dirname = os.path.join(target, dirname.replace(root, '')[1:], name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    print('save to:', dirname)
    h, w, _ = img.shape

    sz = (256, 256)
    n1 = h//sz[0]
    n2 = w//sz[1]

    # res = patchify(img, (256, 256), step=1)
    for i in range(n1):
        for j in range(n2):
            # print(f'now: {i}, {j} - {n1*i} -> {n1*i+sz[0]} & {n2*j} -> {n2*j+sz[1]}')
            x = img[sz[0]*i : sz[0]*i+sz[0], sz[1]*j : sz[1]*j+sz[1], :]
            Image.fromarray(x).save(os.path.join(dirname, name + f'_{i}-{j}.jpg'))


if __name__ == "__main__":
    for x in glob.glob(root + r'/*/*/*.jpg'):
        print('crop file:', x)
        crop(x)
        # break;