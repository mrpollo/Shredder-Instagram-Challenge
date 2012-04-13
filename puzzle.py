#!/usr/local/bin/python
from pprint import pprint
from PIL import Image, ImageChops, ImageStat

''' props '''

image             = Image.open('file.png')
data              = image.getdata()
NUMBER_OF_COLUMNS = 20
unshredded        = Image.new("RGBA", image.size)
shred_width       = unshredded.size[0] / NUMBER_OF_COLUMNS
height            = image.size[1]
pairs             = {}
check             = -1

''' functions '''

def get_pixel_value(x, y, img = image):
	'''
	Access an arbitrary pixel. Data is stored as a 2d array where rows are
	sequential. Each element in the array is a RGBA tuple (red, green, blue,
	alpha).
	'''
	width, height = img.size
	# y -= 1
	pixel = img.getdata()[y * width + x]
	return pixel

def get_shred(sn):
	'''
	Get shred by index defined by total width / shred width starting in 0
	from given image
	'''
	x1, y1 = shred_width * sn, 0
	x2, y2 = x1 + shred_width, height
	crop   = image.crop((x1, y1, x2, y2))
	shred  = Image.new("RGBA", (shred_width, height))
	shred.paste(crop, (0,0))
	return shred

def diff_rows(right, left):
	'''
	compare pixel rows
	'''
	r, g, b = 0, 0, 0
	diff = 0
	for i in range(height):
		r = abs(right[i][0] - left[i][0])
		g = abs(right[i][1] - left[i][1])
		b = abs(right[i][2] - left[i][2])
		diff += r + g + b
	# print diff
	return diff

''' playground '''

# fill the dict with checked values so we can compare
# if its new data
for i in range(NUMBER_OF_COLUMNS):
	pairs[i] = {0: -1, 1: 0}

# check the delta sensation "Delta E"
# delta = difference && E = sensation
for o in range(NUMBER_OF_COLUMNS):
	lowestShred, lowestCount = -1, -1
	
	for i in range(NUMBER_OF_COLUMNS):
		shred_a, shred_b, right, left = get_shred(o), get_shred(i), [], []
		
		for y in range(height):
			right.append( get_pixel_value(shred_width -1, y, shred_a) )
			left.append( get_pixel_value(0, y, shred_b) )
			
		delta = diff_rows(right, left)
		
		if	(lowestCount == -1 or delta < lowestCount):
			lowestShred = i
			lowestCount = delta
			
	if (pairs[lowestShred][0] == -1 or pairs[lowestShred][1] > lowestCount):
		pairs[lowestShred][0] = o
		pairs[lowestShred][1] = lowestCount

# check for the shred with no difference to the left
# then start pasting next to it
for o in range(NUMBER_OF_COLUMNS):
	for i in range(NUMBER_OF_COLUMNS):
		if ( pairs[i][0] == check ):
			check = i
			unshredded.paste(get_shred(i), (shred_width * o, 0))
			break
			
unshredded.save("final.png", "PNG")