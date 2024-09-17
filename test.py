from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
import torch
from PIL import Image
import numpy as np
#from visualizer_depthmap import 
import matplotlib.pyplot as plt
from depthmap_visualization import depth_visualization

"""This small script outputs a """
# Depth maps in sea-thru dataset contains zero values when it is far away from the camera

depth_map, colored_depth_map = depth_visualization('docs/depthT_S04879.tif', save=True)

# Load controlnet from pretrained sdv-1.5 depth-based model
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-depth", torch_dtype=torch.float16
)

# Load stable diffusion v1.4 
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "sd-legacy/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16,
)

# Load lora specialized in underwater scenes
pipe.load_lora_weights('Ivan5d/lora_deep_sea', weight_name='UNDERWATER_SCENE_v2.safetensors', adapter_name="underwater")

positive_prompt = "UNDERWATER_SCENE, aqua, corals"

pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_xformers_memory_efficient_attention()
pipe.enable_model_cpu_offload()

lora_scale = 0.9
image = pipe(positive_prompt, depth_map, num_inference_steps=20, cross_attention_kwargs={"scale": lora_scale}).images[0]

image.save("controlnet_depthmap.png")