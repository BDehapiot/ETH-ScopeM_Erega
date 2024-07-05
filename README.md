 ![IJ Badge](https://img.shields.io/badge/ImageJ-1.54f-rgb(101%2C164%2C227)?logo=imageJ&logoColor=rgb(149%2C157%2C165)&labelColor=rgb(50%2C60%2C65))  
![Author Badge](https://img.shields.io/badge/Author-Benoit%20Dehapiot-blue?labelColor=rgb(50%2C60%2C65)&color=rgb(149%2C157%2C165))
![Date Badge](https://img.shields.io/badge/Created-2023--05--12-blue?labelColor=rgb(50%2C60%2C65)&color=rgb(149%2C157%2C165))
![License Badge](https://img.shields.io/badge/Licence-GNU%20General%20Public%20License%20v3.0-blue?labelColor=rgb(50%2C60%2C65)&color=rgb(149%2C157%2C165))    

# ETH-ScopeM_Erega  
3D segmentation of bacterial colony habitats

## Index
- [Installation](#installation)
- [Usage](#usage)
- [Comments](#comments)

## Installation

</details> 

<details> <summary>Click to expand</summary>  

### Step 1: Download this GitHub Repository 
- Click on the green `<> Code` button and download `ZIP` 
- Unzip the downloaded folder to a desired location

### Step 2: Install/Update Fiji
#### Fiji <ins>is not</ins> installed on your system:
- Download [Fiji](https://imagej.net/software/fiji) for your operating system
- Unzip the downloaded Fiji folder to a desired location
- Start Fiji by running the executable contained in the folder  

#### Fiji <ins>is already</ins> installed on your system:
- Option 1:
    - Update ImageJ by clicking > `Help` > `Update ImageJ...`
    - Update Fiji by clicking > `Help` > `Update...`

- Option 2:
    - Install a new Fiji instance (folder) to avoid modifying your own

### Step 3: Run the Macro
- Drag and drop the `IJM` file(s) to you Fiji interface
- Click `run` in the new IDE window to execute the macro

</details>

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

## Comments