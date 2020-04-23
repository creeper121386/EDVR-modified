import cv2
import os
from tqdm import tqdm
import sys

## usage: python split.py src-dir target-dir


path = sys.argv[1]
res_path = sys.argv[2]


def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def split(file, save_dir):
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()
    count = 0
    
    print(file, success)
    while success:
        p = os.path.join(res_path, fname, f"frame{count}.jpg")
        if 'mov' == file.split('.')[-1].lower():
            image = cv2.flip(image, 0)

        cv2.imwrite(p, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1


if __name__ == "__main__":
    if not os.path.exists(res_path):
        os.makedirs(res_path)

    for f in tqdm(os.listdir(path)):
        fname = os.path.basename(f).split('.')[0]
        save_dir = os.path.join(res_path, fname)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        split(os.path.join(path, f), save_dir)

    