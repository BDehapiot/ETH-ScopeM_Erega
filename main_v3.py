#%% Imports -------------------------------------------------------------------

import re
import numpy as np
import pandas as pd
from skimage import io 
from pathlib import Path
from tifffile import TiffFile
from joblib import Parallel, delayed
from skimage.filters import gaussian
from skimage.morphology import binary_erosion

#%% Initialize ----------------------------------------------------------------


data_path = 'D:\local_Erega\data'
for hstack_path in sorted(Path(data_path).iterdir()): 
    if hstack_path.suffix == '.tif':
        
        # hstack & channel info
        hstackName = hstack_path.stem[:9]
        chnNames = tuple(hstack_path.stem[10:].split('-'))
               
        # Extract image hstack    
        hstack = io.imread(hstack_path)
        
        # Transpose hstack to ztyx (will not work in any situations)
        hstackDims = hstack.shape
        chnDim = hstackDims.index(len(chnNames))
        if chnDim == 3:
            hstack = np.transpose(hstack, (0,3,1,2))
            
        # create saving directory
        dir_path = Path(data_path, hstackName)
        dir_path.mkdir(parents=True, exist_ok=True)


        

        

