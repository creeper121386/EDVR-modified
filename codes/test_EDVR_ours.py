import os
import os.path as osp
import glob
import logging
import numpy as np
import cv2
import torch
from PIL import Image

import utils.util as util
import data.util as data_util
from models import create_model
import models.archs.EDVR_arch as EDVR_arch

import os.path as osp
import logging
import time
import argparse
from collections import OrderedDict

import options.options as option
import utils.util as util
from data.util import bgr2ycbcr
from data import create_dataset, create_dataloader
from models import create_model

#### options
parser = argparse.ArgumentParser()
parser.add_argument('-opt', type=str, required=True, help='Path to options YMAL file.')
opt = option.parse(parser.parse_args().opt, is_train=False)
opt = option.dict_to_nonedict(opt)


def main():
    #################
    # configurations
    #################
    # device = torch.device('cuda')
    # os.environ['CUDA_VISIBLE_DEVICES'] = '0, 1'
    save_imgs = True

    print('before')

    model = create_model(opt)
    print('after')

    save_folder = '../results/{}'.format(opt['name'])
    GT_folder = osp.join(save_folder, 'images/GT')
    output_folder = osp.join(save_folder, 'images/output')
    input_folder = osp.join(save_folder, 'images/input')
    util.mkdirs(save_folder)
    util.mkdirs(GT_folder)
    util.mkdirs(output_folder)
    util.mkdirs(input_folder)

    print('mkdir finish')

    util.setup_logger('base', save_folder, 'test', level=logging.INFO, screen=True, tofile=True)
    logger = logging.getLogger('base')

    #### set up the models
    # model.load_state_dict(torch.load(model_path), strict=True)
    # model.eval()
    # model = model.to(device)
    
    for phase, dataset_opt in opt['datasets'].items():
        val_set = create_dataset(dataset_opt)
        val_loader = create_dataloader(val_set, dataset_opt, opt, None)

        pbar = util.ProgressBar(len(val_loader))
        psnr_rlt = {}  # with border and center frames
        psnr_rlt_avg = {}
        psnr_total_avg = 0.
        for val_data in val_loader:
            folder = val_data['folder'][0]

            # import ipdb; ipdb.set_trace()

            idx_d = val_data['idx']
            # border = val_data['border'].item()
            if psnr_rlt.get(folder, None) is None:
                psnr_rlt[folder] = []

            model.feed_data(val_data)
            model.test()
            visuals = model.get_current_visuals()
            rlt_img = util.tensor2img(visuals['rlt'])  # uint8
            gt_img = util.tensor2img(visuals['GT'])  # uint8
            
            mid_ix = dataset_opt['N_frames'] // 2
            input_img = util.tensor2img(visuals['LQ'][mid_ix])

            
            # Image.fromarray(rlt_img).save(os.path.join(save_folder, f'res/{}.jpg'))
            if save_imgs:
                try:
                    print(osp.join(output_folder, '{}.png'.format(idx_d[0].replace('/', '-'))))
                    cv2.imwrite(osp.join(output_folder, '{}.png'.format(idx_d[0].replace('/', '-'))), rlt_img)
                    cv2.imwrite(osp.join(GT_folder, '{}.png'.format(idx_d[0].replace('/', '-'))), gt_img)

                    cv2.imwrite(osp.join(input_folder, '{}.png'.format(idx_d[0].replace('/', '-'))), input_img)
                    # import ipdb; ipdb.set_trace()

                except Exception as e:
                    print(e)
                    import ipdb; ipdb.set_trace()

            # calculate PSNR
            psnr = util.calculate_psnr(rlt_img, gt_img)
            psnr_rlt[folder].append(psnr)
            pbar.update('Test {} - {}'.format(folder, idx_d))
        for k, v in psnr_rlt.items():
            psnr_rlt_avg[k] = sum(v) / len(v)
            psnr_total_avg += psnr_rlt_avg[k]
        psnr_total_avg /= len(psnr_rlt)
        log_s = '# Validation # PSNR: {:.4e}:'.format(psnr_total_avg)
        for k, v in psnr_rlt_avg.items():
            log_s += ' {}: {:.4e}'.format(k, v)
        logger.info(log_s)


if __name__ == '__main__':
    main()
