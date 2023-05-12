#%% Imports -------------------------------------------------------------------

import numpy as np
from skimage import io 
from pathlib import Path

#%% Parameters ----------------------------------------------------------------

treshC1 = 0.1
treshC2 = 0.1

#%% Initialize ----------------------------------------------------------------

stack_name = 'expl_01.tif'
stack = io.imread(Path('data') / stack_name)
stackC1 = stack[:,0,...]
stackC2 = stack[:,1,...]

#%%

from skimage.filters import gaussian
from skimage.morphology import binary_erosion

# segment (blur + threshold)
maskC1 = gaussian(stackC1, sigma=2) > treshC1
maskC2 = gaussian(stackC2, sigma=2) > treshC2

# get results
onlyC1 = maskC1.copy()
onlyC1[maskC2==True] = False
onlyC2 = maskC2.copy()
onlyC2[maskC1==True] = False
overlap = np.logical_and(maskC1, maskC2)

# display
outlineC1 = ((binary_erosion(maskC1) ^ maskC1).astype('uint8'))*255
outlineC2 = ((binary_erosion(maskC2) ^ maskC2).astype('uint8'))*255
outlineC1 = np.stack((
    np.zeros_like(outlineC1),
    outlineC1,
    np.zeros_like(outlineC1),
    ), axis=-1)
outlineC2 = np.stack((
    outlineC2,
    np.zeros_like(outlineC2),
    outlineC2,
    ), axis=-1)

stackHrz = np.concatenate((stackC1, stackC2), axis=2)
outlineHrz = np.concatenate((outlineC1, outlineC2), axis=2)

# displayC1 = np.stack((stackC1, stackC1, stackC1), axis=-1)


# displayC1 = stackC1.copy()
# displayC1[outlineC1==True] = np.max(displayC1) 
# displayC2 = stackC2.copy()
# displayC2[outlineC2==True] = np.max(displayC2) 



#%%

import napari
viewer = napari.Viewer()

# viewer.add_image(stackC1)
# viewer.add_image(stackC2)
# viewer.add_image(maskC1)
# viewer.add_image(maskC2)

# viewer.add_image(outlineC1)
# viewer.add_image(outlineC2)

viewer.add_image(stackHrz)
viewer.add_image(outlineHrz)

# viewer.add_image(displayC1)
# viewer.add_image(displayC2)

# viewer.add_image(onlyC1, colormap='green', blending='additive')
# viewer.add_image(onlyC2, colormap='magenta', blending='additive')
# viewer.add_image(overlap, colormap='gray', blending='additive')
# viewer.ndims.ndisplay = 3