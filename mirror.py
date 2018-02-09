import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while(cap.isOpened()):
	ret, frame = cap.read()
	if ret == False:
		break
	frame = cv2.flip(frame,1) #flip(frame,x): if x = 0 then flip around x-axis, if x > 0 then flip around y-axis, and if x < 0 then flip around both axis
	cv2.imshow('frame',frame)

	if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
