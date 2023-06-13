open("D:/local_Erega/data/raw/zStack_01_dead-live_chn-1_mask.tif");
open("D:/local_Erega/data/raw/zStack_01_dead-live_chn-2_mask.tif");

run("3D Manager");

list = getList("image.titles");
if (list.length==0) {print("Abort: no image open"); exit();}
if (list.length==1) {print("Abort: only one image open"); exit();}
if (list.length>2) {print("Abort: more than two images open"); exit();}

for (i=0; i<list.length; i++){
	selectWindow(list[i]);
	rename("mask-" + d2s(i, 0));
	Ext.Manager3D_Segment(1, 255);
	rename("labels-" + d2s(i, 0));
	run("glasbey inverted");
}

imageCalculator("Add create stack", "mask-0","mask-1");
rename("mask-union");
Ext.Manager3D_Segment(1, 255);
rename("labels-union");
run("glasbey inverted");

imageCalculator("Min create stack", "mask-0","mask-1");
rename("mask-inter");

run("Tile");
