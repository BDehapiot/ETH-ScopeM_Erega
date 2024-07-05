## Usage
### `getMask.ijm` 
1 - Drag and drop the ijm file to Fiji interface.  
2 - Open image hyperstack in Fiji and run the script. 

Parameters:
- `select channel`  
- `sigma for Gaussian blur`  
- `threshold for binarization`  
- `minimum object size` 

Output:  
Save a single binary mask tif file.  
Repeat for another channel.

### `analyseMask.ijm`  
1 - Drag and drop the ijm file to Fiji interface.   
2 - Open two masks (chn1 & chn2) obtain using `getMask.ijm`. 

Outputs:  
Result table with volume (µm3) of:
 - chn1
 - chn2
 - union (chn1 or chn2)
 - intersection (chn1 and chn2)
 - intersection/union (IoU)  