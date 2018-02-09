# Apply opticalflow to live movie from camera on your laptop
import sys
import cv2
import numpy as np

movie = 0 # live movie from the front camera of the laptop

def draw_flow(im,flow,step=16):
	h,w = im.shape[:2]
	y,x = np.mgrid[step/2:h:step,step/2:w:step].reshape(2,-1).astype(int)
	fx,fy = flow[y,x].T

	lines = np.vstack([x,y,x+fx,y+fy]).T.reshape(-1,2,2)
	lines = np.int32(lines + 0.5)

	vis = cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
	#cv2.polylines(vis, lines, 0, (0,255, 0))
	for (x1,y1),(x2,y2) in lines:
		cv2.line(vis,(x1,y1),(x2,y2),(0,255,0),1)
		cv2.circle(vis,(x1,y1),1,(0,255,0),-1)
	return vis

cap = cv2.VideoCapture(movie)
#cap.set(3,640) # change the width of the window
#cap.set(4,480) # change the height of the window

ret,im = cap.read()
prev_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

#while cap.isOpened():
while True:
	ret,im = cap.read()
	if ret == False:
		break
	im = cv2.flip(im,1)
	gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	#print(prev_gray.shape)
	#print(gray.shape)
	flow = cv2.calcOpticalFlowFarneback(prev_gray,gray,None,0.5,3,15,3,5,1.5,cv2.OPTFLOW_USE_INITIAL_FLOW)
	prev_gray = gray

	cv2.imshow('Optical flow',draw_flow(gray,flow))
	#cv2.imshow('test',flow)
	#cv2.imshow('test2',prev_gray)
	if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27: #press 'q' or 'ESC' then break
		break

cap.release()
cv2.destroyAllWindows()
