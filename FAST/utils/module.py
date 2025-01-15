import numpy as np
import torch
import torchvision.transforms as transforms
from FAST.fast_dataset.utils import get_img, scale_aligned_short
from FAST.models import build_model
from FAST.models.utils import fuse_module, rep_model_convert
from mmcv import Config
from PIL import Image


def load_fast_model(
    model_cfg_path="../FAST/FAST/config/fast/tt/fast_base_tt_800_finetune_ic17mlt.py",
    ckpt_path="../FAST/FAST/download/fast_base_tt_800_finetune_ic17mlt.pth",
    override_for_rect_inference=True,
):
    cfg = Config.fromfile(model_cfg_path)
    model = build_model(cfg.model)
    model = model.cuda()

    ckpt = torch.load(ckpt_path)

    d = dict()
    state_dict = ckpt.get("ema", False)
    if not state_dict:
        state_dict = ckpt.get("state_dict", ckpt)

    for key, value in state_dict.items():
        tmp = key.replace("module.", "")
        d[tmp] = value

    model.load_state_dict(d)
    model = rep_model_convert(model)
    model = fuse_module(model)

    if override_for_rect_inference:
        cfg.test_cfg.bbox_type = "rect"
        cfg.test_cfg.min_score = 0.85
        cfg.min_area = 250

    return model, cfg


def process_image(img, model_short_size=640):
    img_meta = dict(org_img_size=[np.array(img.shape[:2])])

    img = scale_aligned_short(img, model_short_size)
    img_meta.update(dict(img_size=[np.array(img.shape[:2])]))

    img = Image.fromarray(img)
    img = img.convert("RGB")
    img = transforms.ToTensor()(img)
    img = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(
        img
    )

    data = dict(imgs=img.cuda(non_blocking=True).unsqueeze(0), img_metas=img_meta)
    return data
