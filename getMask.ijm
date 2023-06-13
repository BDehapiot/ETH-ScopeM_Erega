name = File.nameWithoutExtension;
dir = File.directory;

setBatchMode(true);

saveData = false;
while (saveData == false) {
	
	// --- Clear Data --- ///
	if (isOpen("Raw")) {selectWindow("Raw"); run("Close");} 
	if (isOpen("GBlur")) {selectWindow("GBlur"); run("Close");} 
	if (isOpen("tmpMask")) {selectWindow("tmpMask"); run("Close");}
	if (isOpen("Mask")) {selectWindow("Mask"); run("Close");}
	if (isOpen("Mask")) {selectWindow("Mask"); run("Close");}	
    if (isOpen("Display")) {selectWindow("Display"); run("Close");}	
    
    // --- Dialog Box --- ///
	Dialog.create("Options");
	channel = Dialog.addNumber("select channel", 1.0000);
	sigma = Dialog.addNumber("sigma for Gaussian blur", 3.0000);
	thresh = Dialog.addNumber("threshold for binarization", 15.0000);
	minSize = Dialog.addNumber("minimum object size", 250.0000);
	Dialog.show();
	channel = Dialog.getNumber();
	sigma = Dialog.getNumber();
	thresh = Dialog.getNumber();
	minSize = Dialog.getNumber();
	
	/// --- Get Mask --- ///
	run("Duplicate...", "duplicate channels=" + channel);
	rename("Raw");
	run("Duplicate...", "duplicate");
	run("Gaussian Blur...", "sigma="+sigma+" stack");
	rename("GBlur");
	setThreshold(thresh, 65535, "raw");
	run("Convert to Mask", "method=Default background=Dark black");
	rename("tmpMask");
	run("Analyze Particles...", "size="+minSize+"-Infinity show=Masks stack");
	run("Invert LUT");
	rename("Mask");
	
	/// --- Make Display --- ///
	run("Duplicate...", "duplicate");
	run("Outline", "stack");
	rename("Outline");
	selectWindow("Raw");
	run("Fire");
	run("Merge Channels...", "c1=Outline c4=Raw create");
	run("RGB Color", "slices");
	rename("Display");
	setBatchMode("show");
	
	/// --- Dialog Box --- ///
	waitForUser( "","Inspect data and click");
	saveData = getBoolean("Save data?", "Yes", "Retry");
	
}

selectWindow("Mask");
saveAs("tiff", dir + name + "_chn-" + d2s(channel, 0) + "_mask.tif");

// --- Clear Data --- ///
if (isOpen("Raw")) {selectWindow("Raw"); run("Close");} 
if (isOpen("GBlur")) {selectWindow("GBlur"); run("Close");} 
if (isOpen("tmpMask")) {selectWindow("tmpMask"); run("Close");}
if (isOpen("Mask")) {selectWindow("Mask"); run("Close");}
if (isOpen("Mask")) {selectWindow("Mask"); run("Close");}	
if (isOpen("Display")) {selectWindow("Display"); run("Close");}	