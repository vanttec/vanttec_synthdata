import argparse
import torch
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt

def depth_visualization(path_depth_map, save):
    '''This module is used for visualizing a raw depth map.'''
    depth_map = Image.open(path_depth_map)   
    cmap = plt.cm.viridis
    d_min = np.min(depth_map)
    d_max = np.max(depth_map)
    depth_relative = (depth_map - d_min) / (d_max - d_min) # Normalization to [0,1]
    colored_depth_map = 255 * cmap(depth_relative)[:,:,:3] # cmap returns a fourth channel (alpha)
    if save == True: 
        plt.imshow(colored_depth_map.astype("uint8")) # JPEG/PNG stores only uint8 or uint16. 
        plt.axis("off")
        plt.savefig("visualization_depthmap.png")
    
    return depth_map, colored_depth_map

if __name__=="__main__":
    depth_map, colored_depth_map = depth_visualization(path_depth_map, save)