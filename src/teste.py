
# Author: Gabriel Dinse
# File: teste
# Date: 11/1/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
cap2 = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
i = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    i += 1
    print(i)
    if not ret and not ret2:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    # cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
