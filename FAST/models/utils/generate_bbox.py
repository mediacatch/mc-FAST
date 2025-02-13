import numpy as np
import cv2
import math


def generate_bbox(keys, label, score, scales, cfg):
    if cfg is None:
        min_score = 0.85
        min_area = 250
        bbox_type = "rect"

    else:
        min_score = cfg.test_cfg.min_score
        min_area = cfg.test_cfg.min_area
        bbox_type = cfg.test_cfg.bbox_type

    label_num = len(keys)
    bboxes = []
    scores = []
    for index in range(1, label_num):
        i = keys[index]
        ind = label == i
        ind_np = ind.data.cpu().numpy()
        points = np.array(np.where(ind_np)).transpose((1, 0))
        if points.shape[0] < min_area:
            label[ind] = 0
            continue
        score_i = score[ind].mean().item()
        if score_i < min_score:
            label[ind] = 0
            continue

        if bbox_type == "rect":
            rect = cv2.minAreaRect(points[:, ::-1])
            alpha = math.sqrt(math.sqrt(points.shape[0] / (rect[1][0] * rect[1][1])))
            rect = (rect[0], (rect[1][0] * alpha, rect[1][1] * alpha), rect[2])
            bbox = cv2.boxPoints(rect) * scales

        elif bbox_type == "poly":
            binary = np.zeros(label.shape, dtype="uint8")
            binary[ind_np] = 1
            contours, _ = cv2.findContours(
                binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            bbox = contours[0] * scales
        bbox = bbox.astype("int32")
        bboxes.append(bbox.reshape(-1).tolist())
        scores.append(score_i)
    return bboxes, scores
