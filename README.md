## EDVR for lowlight-enhancement

### code comments:

- how to select a model? : 

```
train.py -> models.create_model -> models.Video_base_model -> models.networks.define_G -> models.archs.EDVR_arch
```

- how to select a dataset? :

```
train.py -> data.create_dataset -> xxx_dataset.py
```

- in dataset creation: pipline: 
    - `read_img_seq`
    - select each N frames as a group
    - do the transformation: resize, random-crop, etc.

## 4.21

- 试图添加crop。发现REDS中，`__getitem__`输出的图片都是numpy浮点格式，[H, W, C].
- 两个办法：
    - 我们的数据集也用numpy：需要修改`data.util.read_img_seq`，去掉变为pytorch的部分
    - 还是使用`torch.Tensor`格式：修改crop部分和rotate部分(`data.util.augment`)

## 4.22

- 多卡训练：`yml`文件中设置可见卡，并在训练的命令行参数中传递`--nproc_per_node=卡数`

## 4.24

- 训练使用的图片大小有限制。尽量使用2^n的长宽的图片，肯定不会出错。如果不行的话也尽量是16，8，4的倍数之类的。