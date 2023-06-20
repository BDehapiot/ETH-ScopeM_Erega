setBatchMode(true);

run("3D Manager");

/// --- Initialize --- ///
list = getList("image.titles");
if (list.length==0) {print("Abort: no image open"); exit();}
if (list.length==1) {print("Abort: only one image open"); exit();}
if (list.length>2) {print("Abort: more than two images open"); exit();}
for (i=0; i<list.length; i++){
	selectWindow(list[i]);
	rename("Mask-" + d2s(i+1, 0));
}
getPixelSize(unit, pixelWidth, pixelHeight, pixelDepth);

/// --- Create Masks and Labels --- ///
imageCalculator("Min create stack", "Mask-1","Mask-2");
rename("Mask-inter");
imageCalculator("Add create stack", "Mask-1","Mask-2");
rename("Mask-union");
Ext.Manager3D_Segment(1, 255);
rename("ID-union");
run("glasbey inverted");

/// --- Get maxID --- ///
run("Z Project...", "projection=[Max Intensity]");
run("Set Measurements...", "min max redirect=None decimal=3");
run("Measure");
maxID = getResult("Max", 0);
close("MAX_ID-union");
run("Clear Results");

/// --- Get results --- ///
run("Set Measurements...", "integrated redirect=None decimal=3");
sumChn1 = newArray(maxID);
sumChn2 = newArray(maxID);
sumInter = newArray(maxID);
sumUnion = newArray(maxID);
IoU = newArray(maxID);

for (i=0; i<maxID; i++){
	
	// Get Mask-ID 
	selectWindow("ID-union");
	run("Duplicate...", "duplicate");
	rename("Mask-ID");
	setThreshold(i+1, i+1, "raw");
	run("Convert to Mask", "method=Default background=Dark black");
	
	// chn-1
	imageCalculator("AND create stack", "Mask-ID","Mask-1");
	rename("Mask-ID-1");
	run("Z Project...", "projection=[Sum Slices]");
	run("Measure");
	sumChn1[i] = getResult("RawIntDen", 0);
	run("Clear Results");
	
	// chn-2
	imageCalculator("AND create stack", "Mask-ID","Mask-2");
	rename("Mask-ID-2");
	run("Z Project...", "projection=[Sum Slices]");
	run("Measure");
	sumChn2[i] = getResult("RawIntDen", 0);
	run("Clear Results");
	
	// Union
	imageCalculator("AND create stack", "Mask-ID","Mask-union");
	rename("Mask-ID-union");
	run("Z Project...", "projection=[Sum Slices]");
	run("Measure");
	sumUnion[i] = getResult("RawIntDen", 0);
	run("Clear Results");
	
	// Intersection
	imageCalculator("AND create stack", "Mask-ID","Mask-inter");
	rename("Mask-ID-inter");
	run("Z Project...", "projection=[Sum Slices]");
	run("Measure");
	sumInter[i] = getResult("RawIntDen", 0);
	run("Clear Results");
	
	// IoU
	IoU[i] = sumInter[i] / sumUnion[i];
	
	close("Mask-ID");
	close("Mask-ID-1");
	close("SUM_Mask-ID-1");
	close("Mask-ID-2");
	close("SUM_Mask-ID-2");
	close("Mask-ID-inter");
	close("SUM_Mask-ID-inter");
	close("Mask-ID-union");
	close("SUM_Mask-ID-union");
}

for(i=0; i<maxID; i++){
	setResult("chn1", i, sumChn1[i] / 255 * pixelWidth * pixelHeight * pixelDepth);
	setResult("chn2", i, sumChn2[i] / 255  * pixelWidth * pixelHeight * pixelDepth);
	setResult("union", i, sumUnion[i] / 255  * pixelWidth * pixelHeight * pixelDepth);
	setResult("inter", i, sumInter[i] / 255  * pixelWidth * pixelHeight * pixelDepth);
	setResult("iou", i, IoU[i]);
}

run("Merge Channels...", "c2=Mask-1 c6=Mask-2 create");
rename("chn1(green)_chn2(magenta)_both(white)");
close("Mask-inter");
close("Mask-union");
//close("ID-union");

setBatchMode("exit and display");


