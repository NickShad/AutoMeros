# backend/segmentation.py
import numpy as np
import cv2
from PIL import Image
import os
from ultralytics import YOLO
from typing import Tuple, List, Dict
from pathlib import Path
from collections import namedtuple


MODEL_PATH = Path(__file__).parent.parent / "backend" / "20_ep_ishak.pt"
IMAGE_SIZE = 640
CONFIDENCE_THRESHOLD = 0.25
IOU = 0.45
CLASSES_LIST = [0, 3, 6, 8, 11, 14, 16, 22]

OUTPUT_DIR = Path(__file__).parent.parent / "frontend" / "runs" / "segment" / "predict" / "crops_by_mask"
CLASSNAMES_PATH = Path(__file__).parent.parent / "frontend" / "runs" / "segment" / "predict" / "labels" / "classes_names.txt"

ImageTuple = namedtuple("NamedTuple", ("class_idx", "conf", "path"))

# os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_class_names(path):
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f.readlines() if line.strip() != ""]
        return names
    return None


def parse_yolo_segmentation_line(line, img_w, img_h):
    """
    Ожидает строку вида:
    class_id x1 y1 x2 y2 x3 y3 ... conf
    где x,y нормализованы (0..1), последнее значение - confidence score.
    Возвращает dict {class_id, conf, polygon: [(x_px,y_px), ...]}
    """
    parts = line.strip().split()
    if len(parts) < 4:
        raise ValueError("Label line слишком короткая: " + line)
    try:
        class_id = int(float(parts[0]))
    except:
        raise ValueError("Не удалось распарсить class_id в строке: " + line)

    try:
        conf = float(parts[-1])
    except:
        raise ValueError("Не удалось распарсить confidence в строке: " + line)

    coord_strs = parts[1:-1]
    if len(coord_strs) % 2 != 0:
        coord_strs = coord_strs[:-1]

    coords = []
    for i in range(0, len(coord_strs), 2):
        try:
            x = float(coord_strs[i])
            y = float(coord_strs[i+1])
        except:
            continue
        px = int(round(x * img_w))
        py = int(round(y * img_h))
        coords.append((px, py))

    if len(coords) < 3:
        raise ValueError("Мало точек для полигона: " + line)

    return {"class_id": class_id, "conf": conf, "polygon": coords}

def read_labels_file(labels_path, img_w, img_h):
    items = []
    with open(labels_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                item = parse_yolo_segmentation_line(line, img_w, img_h)
                items.append(item)
            except Exception as e:
                print(f"[warning] пропускаю строку {i}: {e}")
    return items


def create_masked_crops(image_path, labels, output_dir, class_names=None, pad=2) -> List[ImageTuple]:
    """
    Для каждого элемента labels:
      - создаёт маску (0/255)
      - применяет её как alpha канал к исходному изображению
      - кадрирует по bounding box маски (+pad пикселей)
      - сохраняет PNG в output_dir
    """

    bgr = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if bgr is None:
        raise FileNotFoundError(f"Не удалось открыть изображение: {image_path}")
    img_h, img_w = bgr.shape[:2]
    bgr_rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    mask_images = []
    for idx, item in enumerate(labels):
        pts = np.array(item["polygon"], dtype=np.int32)
        pts[:,0] = np.clip(pts[:,0], 0, img_w-1)
        pts[:,1] = np.clip(pts[:,1], 0, img_h-1)

        mask = np.zeros((img_h, img_w), dtype=np.uint8)
        cv2.fillPoly(mask, [pts], 255)

        x, y, w, h = cv2.boundingRect(pts)
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(img_w, x + w + pad)
        y1 = min(img_h, y + h + pad)

        alpha = mask
        rgba = np.dstack([bgr_rgb, alpha])
        crop_rgba = rgba[y0:y1, x0:x1, :].copy()


        # Для мягких краёв можно применить blur к alpha (раскомментировать при необходимости)
        alpha_crop = crop_rgba[:,:,3]
        alpha_blur = cv2.GaussianBlur(alpha_crop, (5,5), 0)
        crop_rgba[:,:,3] = alpha_blur



        pil_img = Image.fromarray(crop_rgba)  # mode RGBA
        class_id = item["class_id"]
        conf = item["conf"]
        class_name = str(class_id)
        if class_names and 0 <= class_id < len(class_names):
            class_name = class_names[class_id].replace(" ", "_")
        out_name = f"{idx:03d}_class{class_id}_{class_name}_conf{conf:.3f}.png"
        out_path = os.path.join(output_dir, out_name)
        pil_img.save(out_path, format="PNG")
        mask_images.append(ImageTuple(class_idx=class_id, conf=conf, path=out_path))
        print(f"Saved: {out_path}  bbox=({x0},{y0})-({x1},{y1}) points={len(pts)}")

    return mask_images


def segment_image(image_path: str) -> Tuple[str, List[ImageTuple]]:
    """
    Сегментирует переданное изображение и возвращает сегментированное изображение,
    а также список изображений сегментов.
    """

    if not os.path.exists(image_path):      # если файл не существует
        raise FileNotFoundError(f"Не существует картинки по пути {image_path}")

    model = YOLO(MODEL_PATH)

    prediction = model.predict(
        source=image_path,  # загруженное изображение
        imgsz=IMAGE_SIZE,  # меньше размер -> меньше точность, но больше скорость
        conf=CONFIDENCE_THRESHOLD,  # confidence threshold
        iou=IOU,  # NMS IoU threshold
        save=True,  # save results to runs/predict/
        save_txt=True,  # disable saving labels as txt
        save_conf=True,  # включает информацию о confidence score в файл
        save_crop=False,  # сохраняет обрезки картинки - почти бесполезно
        show_boxes=False,
        classes=CLASSES_LIST
    )

    predict_dirs = [f for f in os.listdir("./runs/segment") if f.startswith('predict')]
    predict_dir = max(predict_dirs, key=lambda d: int(d[7:]) if len(d) > 7 else 0)
    segmented_image_path = Path(__file__).parent.parent / "frontend"  / "runs" / "segment" / predict_dir / Path(image_path).name
    OUTPUT_DIR = Path(__file__).parent.parent / "frontend"  / "runs" / "segment" / predict_dir / "crops_by_mask"
    CLASSNAMES_PATH = Path(__file__).parent.parent / "frontend"  / "runs" / "segment" / predict_dir / "labels" / "classes_names.txt"
    labels_path = Path(__file__).parent.parent / "frontend"  / "runs" / "segment" / predict_dir /"labels" / f"{Path(image_path).stem}.txt"

    print(__file__)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img = cv2.imread(image_path)
    H, W = img.shape[:2]

    class_names = load_class_names(CLASSNAMES_PATH)
    labels = read_labels_file(labels_path, W, H)

    mask_images_paths = create_masked_crops(image_path, labels, OUTPUT_DIR, class_names)
    return segmented_image_path, mask_images_paths

