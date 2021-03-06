""" This color tracking program is made by _. 0___4 @ _1__1 __1_ """
import numpy as np
import cv2
import sys
import time

start = time.time()

argv = sys.argv #arguments list
argc = len(argv) #length of arguments

if argc != 2:
	print'Usage: $python %s arg1(moviefile)' %argv[0]
	sys.exit()
movie = argv[1]

src = cv2.VideoCapture(argv[1])

""" Take first frame of the video """
retval, frame = src.read()
height, width, channels = frame.shape

"""  Set up initial location of window """
# r,h,c,w - region of image
#           simply hardcoded the values
# (x,y) = (c,r), h = height, w = width
x_green,y_green,w,h = 0,0,50,50
track_window_green = (x_green,y_green,w,h)

""" Set up the several ROI for tracking """
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

""" Set up the termination criteria, either 10 iteration or move by at least 1 pt """
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

""" Set up the colorfilter. which color do you want to track? """
#colorRange( HSV format )
#pink: 150<Hue<170
#red: 0<Hue<20
#yellow: 20<Hue<30
#lightgreen: 35<Hue<45

lower_line_green = np.array([35,60,60])
upper_line_green = np.array([55,255,255])

""" Algorithm of searching for the best initial position of ROI """
# 1. source -> color_filter
# 2. masking the colored area(colored pixels -> 0, the other pixels -> 255)
# 3. counting the number of 0 pixel 
# 4. defining the center of colored area, (x, y), where the count is over the half number of 0 pixel

#green
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask_green = cv2.inRange(hsv, lower_line_green, upper_line_green)
mask_green = cv2.bitwise_not(mask_green)
count_0 = 0 
for i in range(0, height):
	for j in range(0, width):
		if mask_green[i,j] == 0:
			count_0 += 1
center = count_0 / 2
count_0 = 0
for i in range(0, height):
	for j in range(0, width):
		if mask_green[i,j] == 0:
			count_0 += 1
		if count_0 > center:
			break
	if count_0 > center:
		break

print 'green: %d %d' % (j, i)
track_window_green = (j,i,w,h)


while(1):
    retval ,frame = src.read()

    if retval == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask_green = cv2.inRange(hsv, lower_line_green, upper_line_green)
	mask_green = cv2.bitwise_not(mask_green)
	dst_green = cv2.calcBackProject([mask_green],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
	retval_green, track_window_green = cv2.meanShift(dst_green, track_window_green, term_crit)

        # Draw it on image
	x_green,y_green,w,h = track_window_green
	cv2.rectangle(frame, (x_green,y_green), (x_green+w,y_green+h), 100,2)
        cv2.imshow('img',frame)
	cv2.imshow('mask_green',mask_green)
        k = cv2.waitKey(60)# & 0xff
        if k == 27:
            break

    else:
        break

cv2.destroyAllWindows()
src.release()

elapse = time.time() - start
print elapse/60.0, "[min]"
