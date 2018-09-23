import os
def dfree():
	bits = os.statvfs('/flash')
	blksize = bits[0] # 4096
	blkfree = bits[3] # 12
	freesize = blksize * blkfree # 49152
	mbcalc = 1024*1024 # 1048576 
	mbfree = freesize / mbcalc # 0.046875
	return mbfree