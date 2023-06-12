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
        
        # create saving directory
        dir_path = Path(data_path, hstackName)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Extract channels
        try:
            chn_data.append((
                hstackName, 'dead',
                hstack[:, chnNames.index('dead'), ...],
                ))
        except: pass
        try:
            chn_data.append((
                hstackName, 'live',
                hstack[:, chnNames.index('live'), ...],
                ))  
        except: pass    
        try:
            chn_data.append((
                hstackName, 'bflm',
                hstack[:, chnNames.index('bflm'), ...],
                )) 
        except: pass
            
        # Append hstack dict
        hstack_data['metadata'].append(metadata)
        hstack_data['hstackName'].append(hstackName)
        hstack_data['chnNames'].append(chnNames)
        hstack_data['voxSize'].append(voxSize)
        
#%% Get mask ------------------------------------------------------------------   

def get_mask(chn):
    mask = (gaussian(chn, 2) > 0.1).astype('uint8') * 255
    outline = mask - binary_erosion(mask)
    display = np.maximum(chn, outline)
    return mask, outline, display

outputs = Parallel(n_jobs=-1)(
    delayed(get_mask)(data[2]) 
    for data in chn_data
    ) 

chn_data = [
    (data[0], data[1], data[2], output[0], output[1], output[2]) 
    for data, output in zip(chn_data, outputs)
    ]

#%%

for i in range(len(chn_data)):
    
    hstackName = chn_data[i][0]
    chnName = chn_data[i][1]
    mask = chn_data[i][3]
    outline = chn_data[i][4]
    display = chn_data[i][5]
    
    io.imsave(
        Path(data_path, hstackName + '_mask_' + chnName + '.tif'),
        mask,
        check_contrast=False, 
        imagej=True,
        ) 
    
    io.imsave(
        Path(data_path, hstackName + '_display_' + chnName + '.tif'),
        display,
        check_contrast=False, 
        imagej=True,
        )    
        
        
    
#%%

# results = []
# for i, mask in enumerate(hstack_data['mask']):
    
#     hstackName = hstack_data['hstackName'][i]
#     chnNames = hstack_data['chnNames'][i]
    
#     try: 
#         dead = mask[:, chnNames.index('dead'), ...]
#         live = mask[:, chnNames.index('live'), ...]
#         inter_dl = np.sum(np.logical_and(dead, live))
#         union_dl = np.sum(np.logical_or(dead, live))
#         iou_dl = np.sum(inter_dl)/np.sum(union_dl)
#     except:
#         inter_dl, union_dl, iou_dl = np.nan, np.nan, np.nan

#     try: 
#         dead = mask[:, chnNames.index('dead'), ...]
#         bflm = mask[:, chnNames.index('bflm'), ...]
#         inter_db = np.sum(np.logical_and(dead, bflm))
#         union_db = np.sum(np.logical_or(dead, bflm))
#         iou_db = np.sum(inter_db)/np.sum(union_db)
#     except:
#         inter_db, union_db, iou_db = np.nan, np.nan, np.nan

#     try: 
#         live = mask[:, chnNames.index('live'), ...]
#         bflm = mask[:, chnNames.index('bflm'), ...]
#         inter_lb = np.sum(np.logical_and(live, bflm))
#         union_lb = np.sum(np.logical_or(live, bflm))
#         iou_lb = np.sum(inter_lb)/np.sum(union_lb)
#     except: 
#         inter_lb, union_lb, iou_lb = np.nan, np.nan, np.nan
        
#     results.append((hstackName, 'dead/live', inter_dl, union_dl, iou_dl))
#     results.append((hstackName, 'dead/bflm', inter_db, union_db, iou_db))
#     results.append((hstackName, 'live/bflm', inter_lb, union_lb, iou_lb))
    
# results = pd.DataFrame(results, columns=['name', 'comp.', 'inter.', 'union', 'iou'])


#%% outline -------------------------------------------------------------------
    
# import napari
# viewer = napari.Viewer()
# viewer.add_image(mask)
    