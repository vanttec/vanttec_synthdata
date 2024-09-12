#########################################################################################################
#   @Description:
#
#   @Author: 
#   @Email:  
#   @Date:   
#   @Brief:  Outputs a container with Ubuntu 22.04
#
#########################################################################################################
FROM ubuntu/ubuntu:22.04

# Install useful packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    python3-pip \
    git \
    nano \
    terminator \
    curl \
    build-essential \
    dbus-x11 \
    software-properties-common -y \
    && rm -r /var/lib/apt/lists/*

RUN mkdir -p /ws/vanttec_synth/

# Blender and Blenderproc
