from pathlib import Path
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import YolosForObjectDetection, YolosImageProcessor

path_picture = "../assets/coffee-shop.jpg"
path_font = "../assets/OpenSans-ExtraBold.ttf"

image = Image.open(path_picture)

image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(
  outputs=outputs, target_sizes=target_sizes
)[0]

