open("D:/local_Erega/data/raw/zStack_01_dead-live_chn-1_mask_lite.tif");
selectWindow("zStack_01_dead-live_chn-1_mask_lite.tif");
rename("Mask");

setBatchMode(true);

/// --- Initialize --- ///
getDimensions(width,height,channels,slices,frames);
newImage("HyperStack", "16-bit grayscale-mode", width, height, 1, slices, 1);
rename("Labels");

run("Set Measurements...", "modal min redirect=None decimal=3");
run("ROI Manager...");
roiManager("Show All without labels");
roiManager("Show None");

/// --- Process --- ///
maxLabel = 1;
for (i=0; i<slices; i++) {
	
	selectWindow("Mask");
	setSlice(i+1);
	run("Duplicate...", " ");
	run("Analyze Particles...", "add");
	rename("tmpMask");

	if (i+1>1) {
		
		selectWindow("Labels");
		setSlice(i);
		run("Duplicate...", " ");
		rename("tmpLabels");
		
	} else {
		
		selectWindow("Labels");
		setSlice(1);
		run("Duplicate...", " ");
		rename("tmpLabels");
		
	}
	
	for (j=0; j < roiManager("count"); j++) {
		
		selectWindow("tmpLabels");	
		roiManager("Select", j);
		run("Measure");
		modal = getResult("Mode", 0);
		max = getResult("Max", 0);
		run("Clear Results");
		
		if (modal==0 && max==0) {
			color = maxLabel; 
			maxLabel = maxLabel + 1; 
			print("#1");
			}
		if (modal==0 && max!=0) {
			color = max;
			print("#2");
			}
		if (modal!=0) {
			color = modal;
			print("#3");
			}

//		print(color);
		
		setForegroundColor(color, color, color);
		selectWindow("Labels");
		setSlice(i+1);
	    roiManager("Select", j);
	    run("Set...", "value=100");
    	run("Fill", "slice");
		
	}
	
	roiManager("reset");	
	close("tmpMask");
	close("tmpLabels");
		
}
selectWindow("Labels");
setBatchMode("show");
