import sys
import cv2
from numpy import *

argv = sys.argv #arguments list
argc = len(argv) #length of arguments

if argc != 2:
	print'Usage: $python %s arg1(moviefile)' %argv[0]
	quit()
movie = argv[1]

def draw_flow(im,flow,step=16):
	h,w = im.shape[:2]
	y,x = mgrid[step/2:h:step,step/2:w:step].reshape(2,-1)
	fx,fy = flow[y,x].T

	lines = vstack([x,y,x+fx,y+fy]).T.reshape(-1,2,2)
	lines = int32(lines)

	vis = cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
	for (x1,y1),(x2,y2) in lines:
		cv2.line(vis,(x1,y1),(x2,y2),(0,255,0),1)
		cv2.circle(vis,(x1,y1),1,(0,255,0),-1)
	return vis

cap = cv2.VideoCapture(movie)

ret,im = cap.read()
prev_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

while cap.isOpened():
	ret,im = cap.read()
	gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

	flow = cv2.calcOpticalFlowFarneback(prev_gray,gray,0.5,1,3,15,3,5,1)
	prev_gray = gray

	cv2.imshow('Optical flow',draw_flow(gray,flow))
	if cv2.waitKey(1) == 27: #press 'ESC' then break
		break

cap.release()
cv2.desetroyAllWindows()
