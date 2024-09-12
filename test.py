from diffusers import DDPMPipeline
from PIL import Image
import numpy as np

ddpm = DDPMPipeline.from_pretrained("google/ddpm-cat-256", use_safetensors=True).to("cuda")

image = ddpm(num_inference_steps=25).images[0]

image.save("test.png")