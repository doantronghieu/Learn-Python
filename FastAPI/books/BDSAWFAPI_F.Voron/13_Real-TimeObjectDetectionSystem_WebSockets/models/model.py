import add_packages
import torch
from PIL import Image
from typing import Union
import loguru
from pydantic import BaseModel
from transformers import YolosForObjectDetection, YolosImageProcessor

logger = loguru.logger

class Object(BaseModel):
  # The model for a single detected object
  box: tuple[float, float, float, float] # coordinates of the bounding box
  label: str # type of detected object
  
class Objects(BaseModel):
  objects: list[Object]
  
class ObjectDetection:
  image_processor: Union[YolosImageProcessor, None] = None
  model: Union[YolosForObjectDetection, None] = None
  
  def load_model(self) -> None:
    """Loads the model"""
    logger.info("Loading model ...")
    self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
    self.model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")
    logger.info("Model loaded.")
    
  def predict(self, image: Image.Image) -> Objects:
    """Runs a prediction"""
    if not self.image_processor or not self.model:
      raise RuntimeError("Model is not loaded.")
    
    inputs = self.image_processor(images=image, return_tensors="pt")
    outputs = self.model(**inputs)
    
    target_sizes = torch.tensor([image.size[::-1]])
    results = self.image_processor.post_process_object_detection(
      outputs=outputs, target_sizes=target_sizes
    )[0]

    objects: list[Object] = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
      if score > 0.7:
        box_values = box.tolist()
        label = self.model.config.id2label[label.item()]
        objects.append(Object(box=box_values, label=label))
    
    return Objects(objects=objects)

