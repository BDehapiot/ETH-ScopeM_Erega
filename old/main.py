#%% Imports -------------------------------------------------------------------

import numpy as np
from skimage import io 
from pathlib import Path
from skimage.filters import gaussian
from skimage.morphology import binary_erosion

#%% Parameters ----------------------------------------------------------------

pixSize = 2.1526
voxSize = 2.9793
treshC1 = 0.1
treshC2 = 0.1

#%% Initialize ----------------------------------------------------------------

stack_name = 'expl_01.tif'
stack_path = Path('data') / stack_name
stack = io.imread(stack_path)
stackC1 = stack[:,0,...]
stackC2 = stack[:,1,...]
scaleFactors = [voxSize, pixSize, pixSize]

#%% Process -------------------------------------------------------------------

# Segment (blur + threshold)
maskC1 = gaussian(stackC1, sigma=2) > treshC1
maskC2 = gaussian(stackC2, sigma=2) > treshC2

# Get results
onlyC1 = maskC1.copy()
onlyC1[maskC2==True] = False
onlyC2 = maskC2.copy()
onlyC2[maskC1==True] = False
intersect = np.logical_and(maskC1, maskC2)

# Show results
print(       
      f'allC1 =     {np.sum(maskC1)}\n'
      f'onlyC1 =    {np.sum(onlyC1)}\n'
      f'allC2 =     {np.sum(maskC2)}\n'
      f'onlyC2 =    {np.sum(onlyC2)}\n'
      f'interC1C2 = {np.sum(intersect)}\n'
      )

# Displays
empty = np.zeros_like(stackC1)
outlineC1 = ((binary_erosion(maskC1) ^ maskC1).astype('uint8'))*255
outlineC2 = ((binary_erosion(maskC2) ^ maskC2).astype('uint8'))*255
displayC1 = np.maximum(stackC1, outlineC1)
displayC2 = np.maximum(stackC2, outlineC2)

#%% Napari displays -----------------------------------------------------------

import napari
viewer = napari.Viewer()

# -----------------------------------------------------------------------------

# # Raw data
# viewer.add_image(stackC1, scale=scaleFactors)
# viewer.add_image(stackC2, scale=scaleFactors)

# -----------------------------------------------------------------------------

# # Masks
# viewer.add_image(maskC1, scale=scaleFactors)
# viewer.add_image(maskC2, scale=scaleFactors)

# -----------------------------------------------------------------------------

# Results
viewer.add_image(
    onlyC1, colormap='green', blending='additive', scale=scaleFactors)
viewer.add_image(
    onlyC2, colormap='magenta', blending='additive', scale=scaleFactors)
viewer.add_image(
    intersect, colormap='gray', blending='additive', scale=scaleFactors)

# -----------------------------------------------------------------------------

# # Displays
# viewer.add_image(displayC1, scale=scaleFactors)
# viewer.add_image(displayC2, scale=scaleFactors)