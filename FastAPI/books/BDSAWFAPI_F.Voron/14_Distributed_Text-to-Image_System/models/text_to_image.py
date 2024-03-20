from loguru import logger
from collections.abc import Callable
import transformers
from typing import Union
import torch
from PIL import Image
from diffusers import (
  StableDiffusionPipeline, UNet2DConditionModel, EulerDiscreteScheduler
)
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

transformers.utils.move_cache()

model_lst = [
  "runwayml/stable-diffusion-v1-5",
  "CompVis/stable-diffusion-v1-4",
  "segmind/tiny-sd",
]

class TextToImage:
  def __init__(
    self, 
    model_path="runwayml/stable-diffusion-v1-5"
  ) -> None:
    self.pipe: Union[StableDiffusionPipeline, None] = None
    self.model_path: str = model_lst[1]
    self.device: str = ""
  
  def load_model(self) -> None:
    if torch.cuda.is_available():
      self.device = "cuda"
      logger.info("Device: cuda.")
    elif torch.backends.mps.is_available():
      self.device = "mps"
      logger.info("Device: mps.")
    else:
      self.device = "cpu"
      logger.info("Device: cpu.")

    logger.info("Loading model.")
    pipe = StableDiffusionPipeline.from_pretrained(
      self.model_path, torch_dtype=torch.float16,
    )
    pipe.to(self.device)
    self.pipe = pipe
    logger.info("Model loaded.")

  def generate(
    self,
    prompt: str, 
    *,
    negative_prompt: Union[str, None] = None,
    num_steps: int = 1, # 50
    callback: Union[Callable[[int, int, torch.FloatTensor], None], None] = None,
  ) -> Image.Image:
    if not self.pipe:
      raise RuntimeError("Pipeline is not loaded.")
    # result is list of Pillow images, default is one image
    return self.pipe(
      prompt=prompt,
      negative_prompt=negative_prompt,
      num_inference_steps=num_steps,
      guidance_scale=9.0,
      callback=callback
    ).images[0]

if __name__ == "__main__":
  text_to_image = TextToImage()
  text_to_image.load_model()
  
  # def callback(step: int, _timestep, _tensor):
  #   print(f"Step: {step}")
  
  prompt = "A Renaissance castle in the Loire Valley"
  negative_prompt = "low quality, ugly"
  image = text_to_image.generate(
    prompt=prompt, negative_prompt=negative_prompt, 
    # callback=callback,
  )
  image.save("../assets/output.png")
  
text_to_image = TextToImage()
text_to_image.load_model()

# def callback(step: int, _timestep, _tensor):
#   print(f"Step: {step}")

prompt = "A Renaissance castle in the Loire Valley"
negative_prompt = "low quality, ugly"
image = text_to_image.generate(
  prompt=prompt, negative_prompt=negative_prompt, 
  # callback=callback,
)
image.save("../assets/output.png")