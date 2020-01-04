#!/usr/bin/env python
import time
# función utilizada desde "encriptar.py" para escribir el tiempo en el .srt
# indica el tiempo actual y un segundo posterior
def min_seg(minu, seg, minu2, seg2):
	# se indica el tiempo actual (seg comienza en 0)
	if seg == 59:
		minu = minu+1
		seg = 0
	else:
		seg = seg+1
	#print("Min: %s, Seg: %s" % (minu, seg))
	if seg < 10:
		seg_str = '0'+str(seg)
	else:
		seg_str = str(seg)
	if minu < 10:
		min_str = '0'+str(minu)+':'
	else:
		min_str = str(minu)+':'
	##########################################
	# se indica 1 segundo después (seg2 comienza en 1)
	if seg2 == 59:
		minu2 = minu2+1
		seg2 = 0
	else:
		seg2 = seg2+1
	#print("Min: %s, Seg: %s" % (minu2, seg2))
	if seg2 < 10:
		seg_str2 = '0'+str(seg2)
	else:
		seg_str2 = str(seg2)
	if minu2 < 10:
		min_str2 = '0'+str(minu2)+':'
	else:
		min_str2 = str(minu2)+':'

	return minu, seg, seg_str, min_str, minu2, seg2, min_str2, seg_str2