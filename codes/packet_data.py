import os
import os.path as osp
from tqdm import tqdm
import shutil
from PIL import Image


nframes = 50
def mv(src, target):
    '''
    src: folder containing images
    target: destnation containing many sub-folders with `nframes` images.
    '''
    files = [x for x in os.listdir(src)]
    files.sort()
    packet_num = len(files) // nframes

    for i in tqdm(range(packet_num)):
        packet = files[i*nframes:(i+1)*nframes]
        target_folder = f'{i*nframes}-{(i+1)*nframes}'
        target_folder = osp.join(target, target_folder)

        if not osp.exists(target_folder):
            os.makedirs(target_folder)

        for f in packet:
            fpath = osp.join(src, f)
            dst = osp.join(target_folder, f)

            shutil.copy(fpath, dst)
        

mv('/data1/why/EDVR/datasets/low_light_enhancement/input/', '/data1/why/EDVR/datasets/LLE005/input')        
mv('/data1/why/EDVR/datasets/low_light_enhancement/GT/', '/data1/why/EDVR/datasets/LLE005/GT')        
