import time
import sys
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle

DURATION = 1.0

argv = sys.argv #arguments list
argc = len(argv) #length of arguments

if argc != 3:
	print'Usage: $python %s arg1(moviefile) arg2(outputfile)' %argv[0] 
	sys.exit()
movie = argv[1]

# cv2.namedWindow(movie)

src = cv2.VideoCapture(movie)
if not src.isOpened():
	print 'cannot read the file'
	sys.exit()

retval, frame = src.read()
height, width, channels = frame.shape
hist_32 = np.zeros((height, width), np.float32)
frame_pre = frame.copy()

array_angle = []

while True:
	retval, frame = src.read()

	if frame is None:
		break

	diff = cv2.absdiff(frame, frame_pre)
	diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	retval, diff = cv2.threshold(diff, 30, 1, cv2.THRESH_BINARY)
	time_s = time.clock()
	cv2.updateMotionHistory(diff, hist_32, time_s, DURATION)

	hist = np.array(np.clip((hist_32-(time_s-DURATION))/DURATION, 0, 1) * 255, np.uint8)
	hist = cv2.cvtColor(hist, cv2.COLOR_GRAY2BGR)

	hist_8, direction = cv2.calcMotionGradient(hist_32, 0.25, 0.05, apertureSize=5)

	angle = cv2.calcGlobalOrientation(direction, hist_8, hist_32, time_s, DURATION)

	angle = angle * np.pi/180
	array_angle.append(angle)
	
	#cv2.circle(hist, (width/2, height/2), 3, (255, 0, 0), 3, cv2.CV_AA, 0)
	#cv2.line(hist, (width/2, height/2), \
	#		(int( width/2 + math.cos(angle) * height/3), \
	#		 int(height/2 + math.sin(angle) * height/3)), \
	#		(255, 0, 0), 3, cv2.CV_AA, 0)

	#cv2.imshow(movie, hist)

	frame_pre = frame.copy()

	#key = cv2.waitKey(1)
	#if key == 27:
	#	break

with open(argv[2],'wb') as output:
	pickle.dump(array_angle, output)

#print array_angle
#plt.plot(array_angle)
#plt.show()

cv2.destroyAllWindows()
src.release()
