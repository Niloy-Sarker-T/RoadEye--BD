import numpy as np
from ultralytics import RTDETR
from ensemble_boxes import weighted_boxes_fusion
from .utils import get_boxes

# Load models once (adjust paths to your local models)
model1 = RTDETR("models/best.pt")
model2 = RTDETR("models/last.pt")

def run_inference(image_path):
    """
    Run inference on a single image and return bounding boxes, scores, classes.
    """
    boxes_list, scores_list, classes_list = [], [], []

    # Model 1
    r1 = model1.predict(source=image_path, conf=0.5, verbose=False)
    boxes_list.append(get_boxes(r1[0].boxes.xywhn.cpu().numpy()))
    scores_list.append(r1[0].boxes.conf.cpu().numpy())
    classes_list.append(r1[0].boxes.cls.cpu().numpy())

    # Model 2
    r2 = model2.predict(source=image_path, conf=0.5, verbose=False)
    boxes_list.append(get_boxes(r2[0].boxes.xywhn.cpu().numpy()))
    scores_list.append(r2[0].boxes.conf.cpu().numpy())
    classes_list.append(r2[0].boxes.cls.cpu().numpy())

    # Weighted Boxes Fusion
    if boxes_list and any(len(b) > 0 for b in boxes_list):
        boxes, scores, classes = weighted_boxes_fusion(
            boxes_list, scores_list, classes_list,
            weights=[1,1], iou_thr=0.4, skip_box_thr=0.001
        )
    else:
        boxes, scores, classes = [], [], []

    return boxes, scores, classes
