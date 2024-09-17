<p align="center">
  <img src="docs/vanttec.png" width="320" height="180"/>
</p>

# VantTec's Synthetic Data Repository

This is the Vanttec's repository used for synthetic data generation used to feed image segmentation and object detection models. It runs with docker containers and a GPU, but a simplified version can be run without GPU.

<!-- TABLE OF CONTENTS -->
<summary>Table of Contents</summary>
<ol>
  <li>
    <a href="#installation">Installation</a>
  </li>
  <li>
    <a href="#usage">Usage</a>
    <ul>
      <li><a href="#LoRAs">LoRAs</a></li>
    </ul>
  </li>
</ol>


## Installation
```Shell
cd
git clone --recurse-submodules https://github.com/vanttec/vanttec_synthdata.git
```

Inside the /vanttec_uuv/dockerfiles/ directory you would two options to select: 
* ubuntu2204
* ubuntu2204_gpu

Each option contains a Dockerfile (image) and their respective create_container.bash, so please select the one that suits you the most and continue:

```Shell
cd ~/vanttec_uuv/dockerfiles/{selected_option}
docker build -t uuv_synth .
./create_container.bash
docker exec -it uuv_synth /bin/bash
```

## Usage

### LoRA

Underwater scenary: https://huggingface.co/Ivan5d/lora_deep_sea. Trigger words: UNDERWATER_SCENE, aqua

Terrestrial scenary: 

Aerial scenary:

This is a example image obtained from the test.py script using a custom lora, stable diffusion v-1.5 and controlnet.
<div align="center">
  <a href="">
    <img src="controlnet_depthmap.png" alt="test" width="1080" height="720">
  </a>
