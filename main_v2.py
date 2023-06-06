#%% Imports -------------------------------------------------------------------

import re
import numpy as np
from skimage import io 
from pathlib import Path
from tifffile import TiffFile
from joblib import Parallel, delayed
from skimage.filters import gaussian
from skimage.morphology import binary_erosion

#%% Parameters ----------------------------------------------------------------

deadThresh = 0.1
liveThresh = 0.1
bflmThresh = 0.1

#%% Initialize ----------------------------------------------------------------

data_path = 'D:\local_Erega\data'
chn_data = []
hstack_data = {
    'metadata': [],
    'hstackName': [],
    'chnNames': [],
    'voxSize': [],
    'hstack': [],
    'mask':[],
    }

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
        
        # Extract metadata
        with TiffFile(hstack_path) as tif:
            metadata = tif.imagej_metadata
            
        # Voxel info
        info = metadata['Info']
        xi = info.find('dblVoxelX')
        yi = info.find('dblVoxelY')
        zi = info.find('dblVoxelZ')
        xf = info.find('\n', xi)
        yf = info.find('\n', yi)
        zf = info.find('\n', zi)           
        voxX = float(re.findall('\d+\.\d+', info[xi:xf])[0])
        voxY = float(re.findall('\d+\.\d+', info[yi:yf])[0])
        voxZ = float(re.findall('\d+\.\d+', info[zi:zf])[0])
        voxSize = tuple((voxX, voxY, voxZ))
        
        # Extract channels
        try:
            chn_data.append((
                hstackName, 'dead',
                hstack[:, chnNames.index('dead'), ...],
                ))
        except:
            pass
        try:
            chn_data.append((
                hstackName, 'live',
                hstack[:, chnNames.index('live'), ...],
                ))  
        except:
            pass    
        try:
            chn_data.append((
                hstackName, 'bflm',
                hstack[:, chnNames.index('bflm'), ...],
                )) 
        except:
            pass
            
        # Append hstack dict
        hstack_data['metadata'].append(metadata)
        hstack_data['hstackName'].append(hstackName)
        hstack_data['chnNames'].append(chnNames)
        hstack_data['voxSize'].append(voxSize)
        hstack_data['hstack'].append(hstack)

#%% Process -------------------------------------------------------------------   

def process(chn):
    return gaussian(chn, 2) > 0.1

outputs = Parallel(n_jobs=-1)(
    delayed(process)(data[2]) 
    for data in chn_data
    ) 

chn_data = [
    (data[0], data[1], data[2], output) 
    for data, output in zip(chn_data, outputs)
    ]

#%%

hstackNames = sorted(set(hstack_data['hstackName']))
for hstackName in hstackNames:
    data = [data for data in chn_data if data[0] == hstackName]
    mask = np.stack([data[3] for data in data], axis=1)
    hstack_data['mask'].append(mask)



#%% Display -------------------------------------------------------------------
    
# import napari
# viewer = napari.Viewer()
# viewer.add_image(mask)
    