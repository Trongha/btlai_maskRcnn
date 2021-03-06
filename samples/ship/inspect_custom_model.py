#!/usr/bin/env python
# coding: utf-8

# # Mask R-CNN - Inspect Custom Trained Model
# 
# Code and visualizations to test, debug, and evaluate the Mask R-CNN model.

# In[32]:


import os
#import cv2
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage
import glob

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

from samples.ship import ship
from scipy.misc import imsave

# get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

SHIP_WEIGHTS_PATH = "mask_rcnn_ship_0010.h5"  # TODO: update this path


# ## Configurations

# In[33]:


config = ship.ShipConfig()
SHIP_DIR = os.path.join(ROOT_DIR, "datasets/ship")


# In[34]:


# Override the training configurations with a few
# changes for inferencing.
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()


# ## Notebook Preferences

# In[35]:


# Device to load the neural network on.
# Useful if you're training a model on the same 
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"


# In[36]:


def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax


# ## Load Validation Dataset

# In[37]:


# Load validation dataset
dataset = ship.ShipDataset()
dataset.load_ship(SHIP_DIR, "val")

# Must call before using the dataset
dataset.prepare()

print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))


# ## Load Model

# In[38]:


# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                              config=config)


# In[39]:


# load the last model you trained
# weights_path = model.find_last()[1]

weights_path = "../../logs/ship20181209T0231/mask_rcnn_ship_0010.h5"

# Load weights
print("Loading weights ", SHIP_WEIGHTS_PATH)
model.load_weights(weights_path, by_name=True)


# In[40]:


from importlib import reload # was constantly changin the visualization, so I decided to reload it instead of notebook
reload(visualize)


# # Run Detection on Images

# In[41]:


# image_id = random.choice(dataset.image_ids)
for image_id in dataset.image_ids:
    image, image_meta, gt_class_id, gt_bbox, gt_mask =    modellib.load_image_gt(dataset, config, image_id, use_mini_mask=False)
    info = dataset.image_info[image_id]
    print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], image_id, 
                                           dataset.image_reference(image_id)))

    # Run object detection
    results = model.detect([image], verbose=1)

    # Display results
    ax = get_ax(1)
    # 
    r = results[0]

    title = "Pre_" + info["id"] + "_2"
    visualize.display_instances(image , r['rois'], r['masks'], r['class_ids'], 
                                dataset.class_names, r['scores'],
                                title=title, ax=ax, show_mask=False, pathSave = "imgSave/")

    log("gt_class_id", gt_class_id)
    log("gt_bbox", gt_bbox)
    log("gt_mask", gt_mask)



