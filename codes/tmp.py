def mv(src, target):
    '''
    folder: folder containing images
    target: destnation containing many sub-folders with `nframes` images.
    '''
    for sub_folder in os.listdir(folder):
        if not osp.isdir(sub_folder):
            continue

        src = osp.join(folder, sub_folder)
        files = [x for x in os.listdir(src)]
        files.sort()
        packet_num = len(files) // nframes

        for i in tqdm(range(packet_num)):
            packet = files[i*nframes:(i+1)*nframes]
            target_folder = f'{i*nframes}-{(i+1)*nframes}'
            target_folder = osp.join(target, target_folder)

            if not osp.exists(target_folder):
                os.makedirs(target_folder)

            for f in'src' packet:
                f = sub_folder + '.' + f
                fpath = osp.join(src, f)
                dst = osp.join(target_folder, f)

                shutil.copy(fpath, dst)
