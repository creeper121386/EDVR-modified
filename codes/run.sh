python -m torch.distributed.launch --nproc_per_node 1 --master_port 4323 train.py -opt options/train/train_EDVR_ours.yml --launcher pytorch
