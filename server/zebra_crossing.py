import cv2
import numpy as np
import math

def speed_detect(img):
	img = cv2.resize(img, (800,600))
	grey_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	mask_white = cv2.inRange(grey_image, 200, 255)
	tmp = cv2.bitwise_and(img, img, mask = mask_white)

	edges = cv2.Canny(tmp, 500, 500)
	# return edges
	lines = cv2.HoughLinesP(edges,rho = 1,theta = 1*np.pi/180,threshold = 50,minLineLength = 50,maxLineGap = 10)
	# print(len(lines))
	if lines is None:
		# return (img, False)
		return False

	lines2 = []
	for l in lines:
		line = l[0]
		x1,y1 = line[0],line[1]
		x2,y2 = line[2],line[3]
		# cv2.line(img, (x1,y1),(x2,y2), (255,0,0), 2)

		if x1 - x2 == 0:
			lines2.append([x1,y1,x2,y2])
			continue

		slope = (y1-y2)/(x1-x2)
		# print(slope)

		if not 0<=abs(slope)<=1:
			lines2.append([x1,y1,x2,y2])

	max_y, min_y = 500,200
	max_x, min_x = 700,200
	parallel_lines = 0
	for x1,y1,x2,y2 in lines2:
		if min_x < x1 < max_x and min_x < x2 < max_x and min_y < y1 < max_y and min_y < y2 < max_y:
			# cv2.line(img, (x1,y1),(x2,y2), (0,0,255), 2)
			parallel_lines += 1

	# print(parallel_lines)
	if parallel_lines >= 11:
		# print("zebra crossing present")
		# return (img, True)
		return True
	else:
		# print("zebra crossing not present")
		# return (img, False)
		return False

	# return img


if __name__ == '__main__':	
	img = cv2.imread('cross4.jpg')
	img = cv2.resize(img, (800,600))

	img = sliding_window(img)
	while  True:
		cv2.imshow('winname', img)
		if cv2.waitKey(3) == ord('q'):
			cv2.destroyAllWindows()
			break
