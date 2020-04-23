python -m torch.distributed.launch --nproc_per_node=2 --master_port=4321 train.py -opt options/train/train_EDVR_ours.yml --launcher pytorch
