#########################################################################################################
#   @Description: This Dockerfile takes the image from pytorch: 2.4.0-cuda11.8-cudnn9-devel. 
#   Given that cuda 12.2 was selected, the drivers should match it, i.e., ubuntu drivers 535. 
#
#   @Author: Ivan Diaz
#   @Email:  ivan.d557d@hotmail.com
#   @Date:   12.09.24
#   @Brief:  Outputs a container with Ubuntu 22.04, PyTorch 2.4.0
#
#########################################################################################################

FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

# Install useful packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    python3-pip \
    git \
    nano \
    terminator \
    curl \
    build-essential \
    dbus-x11 \
    python3.10-venv \
    python3-tk \
    wget \
    software-properties-common -y \
    && rm -r /var/lib/apt/lists/*

RUN pip install flax

RUN pip install accelerate

RUN pip install git+https://github.com/huggingface/diffusers

RUN pip install pft

RUN pip install -q diffusers transformers accelerate invisible-watermark>=0.2.0

RUN pip install xformers

RUN pip install matplotlib

RUN mkdir -p /ws/vanttec_synth/

# Blender and Blenderproc
