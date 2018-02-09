import sys
import cv2

argv = sys.argv #arguments list
argc = len(argv) #length of arguments

if argc != 2:
        print'Usage: $python %s arg1(moviefile)' %argv[0]
        quit()
movie = argv[1]

cap = cv2.VideoCapture(movie)

while cap.isOpened(): 
	ret,im = cap.read()
	blur = cv2.GaussianBlur(im,(0,0),5)
	cv2.imshow('GaussianBlur',blur)
	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
