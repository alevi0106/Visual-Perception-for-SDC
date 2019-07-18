
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import imutils
import cv2
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect(image):
	present = False
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), scale=1.9)

	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	#pick = non_max_suppression(rects, probs=None, overlapThresh=)
	pick = rects


	for (xA, yA, xB, yB) in pick:
		present = True
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

	return (image, present)

