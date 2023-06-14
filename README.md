# ETH-ScopeM_Erega
3D segmentation of bacteria colony

## Installation  
1 - Download Fiji    
https://imagej.net/software/fiji/  

2 - Install 3D ImageJ Suite  
https://sites.imagej.net/Tboudier/  
- Help > Update > Manage update sites  
- Check "3D ImageJ Suite"  
- Close and Apply changes  

3 - Download this GitHub repository  

## Usage
### `getMask.ijm` 
Drag and drop the ijm file to Fiji interface.  
Open image hyperstack in Fiji and run the script. 

Parameters:
- `select channel`  
- `sigma for Gaussian blur`  
- `threshold for binarization`  
- `minimum object size` 

Output:  
Save a single binary mask tif file.  
Repeat for another channel.

### `analyseMask.ijm`  
Drag and drop the ijm file to Fiji interface.   
Open two masks (chn1 & chn2) obtain using `getMask.ijm`. 

Outputs:  
Result table with volume (µm3) of:
 - chn1
 - chn2
 - union (chn1 or chn2)
 - intersection (chn1 and chn2)
 - intersection/union (IoU)  

