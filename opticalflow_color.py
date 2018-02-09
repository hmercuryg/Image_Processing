# opticalflow with color
import cv2
import numpy as np
import sys

argv = sys.argv #arguments list
argc = len(argv) #length of arguments

if argc != 2:
        print'Usage: $python %s arg1(moviefile)' %argv[0]
        quit()
movie = argv[1]

cap = cv2.VideoCapture(movie)

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while True:
	ret, frame2 = cap.read()
	next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

	flow = cv2.calcOpticalFlowFarneback(prvs,next,0.5,1,3,15,3,5,1)

	mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
	hsv[...,0] = ang*180/np.pi/2
	hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
	rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

	cv2.imshow('frame2', rgb)
	k = cv2.waitKey(30)
	if k == 27:
		break
	elif k == ord('s'):
		cv2.imwrite('opticalfb.png',frame2)
		cv2.imwrite('opticalhsv.png',rgb)
	prvs = next

cap.release()
cv2.destroyAllWindows()
