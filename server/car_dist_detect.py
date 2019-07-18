import cv2

car_cascade = cv2.CascadeClassifier('cars.xml') 

def detect(img):

	# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	dist = []
	cars = car_cascade.detectMultiScale(img, scaleFactor = 1.2, minNeighbors = 4, minSize = (80, 80))
	
	for (x,y,w,h) in cars: 
		# cv2.rectangle(img,(x,y),(x + w, y + h),(0,0,255),2)
		dist.append([x + (w//2), y + (h//2), w * h])
		# cv2.putText(img, f"{dist[-1][2]}", (dist[-1][0], dist[-1][1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), thickness = 2)

	return cars, dist

if __name__ == '__main__':
    img = cv2.imread("toycar4.jpg")
    cars, dist = detect(img)
    print(cars, dist)
    
