## EDVR for lowlight-enhancement

### code comments:

- how to select a model? : 

```
train.py -> models.create_model -> models.networks.define_G -> models.archs.EDVR_arch
```

- how to select a dataset? :

```
train.py -> data.create_dataset -> xxx_dataset.py
```