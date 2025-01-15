import FAST.fast_dataset as fast_dataset


def build_data_loader(cfg):
    param = dict()
    for key in cfg:
        if key == "type":
            continue
        param[key] = cfg[key]

    data_loader = fast_dataset.__dict__[cfg.type](**param)

    return data_loader
