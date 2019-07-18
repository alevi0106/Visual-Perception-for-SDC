
import numpy as np
import cv2
import math

import car_dist_detect
#import zebra_crossing
#import pedestrian1


width, height = 640, 480
center = (width//2-65, height - height//3)

turn = 0
msg = "pw"

def drawlines(m1,c1,m2,c2, img):
    # print("drawlines")
    x,y = center
    y1 = 200
    y2 = height
    x1 = int((y1 - c1)/m1)
    x2 = int((y2 - c1)/m1)
    dl = ((abs(y - m1*x - c1))/math.sqrt(1 + m1**2))

    y3 = 200
    y4 = height
    x3 = int((y3 - c2)/m2)
    x4 = int((y4 - c2)/m2)
    dr = ((abs(y - m2*x - c2))/math.sqrt(1 + m2**2))

    # print(dl,dr)

    global turn
    global msg
    diff = dl - dr
    if diff > 155:
        turn = -1
        msg = 'lw'
    elif diff < -155:
        turn = 1
        msg = 'rw'
    else:
        turn = 0
        msg = 'ffw'

    points = np.array([[x1,y1],[x2,y2],[x4,y4],[x3,y3]], dtype = np.int32)
    # cv2.fillConvexPoly(img, points, (225,200,135))
    cv2.line(img, (x1,y1),(x2,y2), (0,0,255), 5)
    cv2.line(img, (x3,y3),(x4,y4), (0,0,255), 5)
    cv2.circle(img, center, 3, (0,255,255))
    # cv2.putText(img, f"turn = {turn}", (width//3,height//3), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,255), thickness = 2)
    #print(msg)
    return img
    

def drawcars(img, cars):
    for (x,y,w,h) in cars: 
        cv2.rectangle(img,(x,y),(x + w, y + h),(0,0,255),2)
    return img

def roi(img):
    vertices = np.array([[0,height],[0,height//2],[200,0],[450,0],[650,400],[800,600]], np.int32)
    mask = np.zeros_like(img)
    # print(mask)
    cv2.fillConvexPoly(mask, vertices, (255,255,255))
    # return mask
    masked = cv2.bitwise_and(img,mask)
    return masked


def detect(img):
    # print("detect")
    global msg
    lintercept, rintercept = [], []
    lslope, rslope = [], []
    img = cv2.resize(img, (width, height))
    #return (roi(img),msg)
    cars, dist = car_dist_detect.detect(roi(img))

    grey_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask_white = cv2.inRange(grey_image, 200, 255)
    tmp = cv2.bitwise_and(img, img, mask = mask_white)
    edges = cv2.Canny(tmp, 500, 500)
    #return (edges,msg)

    lines = cv2.HoughLinesP(edges,rho = 1,theta = 1*np.pi/180,threshold = 50,minLineLength = 5,maxLineGap = 50)

    if lines is None:
        msg = "pw"
        # print("no lines")s
        return (img, msg)
    for l in lines:
        line = l[0]
        x1,y1 = line[0],line[1]
        x2,y2 = line[2],line[3]
        if x2-x1 == 0:
            continue
        slope = (y1-y2)/(x1-x2)
        if 1<=abs(slope)<=5.7:
            # cv2.line(img, (x1,y1),(x2,y2), (255,0,0), 2)
            intercept = y1 - slope * x1
            if slope > 0:       #right
                rintercept.append(intercept)
                rslope.append(slope)
            else:               #left
                lintercept.append(intercept)
                lslope.append(slope)

    try:
        lintercept = list(filter(lambda v: v==v, lintercept))
        rintercept = list(filter(lambda v: v==v, rintercept))
        m1 = np.mean(lslope)
        c1 = int(np.mean(lintercept))
        m2 = np.mean(rslope)
        c2 = int(np.mean(rintercept))
        img = drawlines(m1,c1,m2,c2, img)
        threshold = 8000
        for x,y,area in dist:
            #print (area)
            if area > threshold:
                msg = 'pw'
            if area > 25000:
                msg = 'bw'
    except Exception as e:
        msg = 'pw'
        #print(e)
        pass

    img = drawcars(img, cars)
    #if zebra_crossing.speed_detect(img):
        #msg = 'fw'
        #print("crosswalk ahead")
    #img, pedspre = pedestrian1.detect(img)
    #if pedspre:
        #msg = 'pw'
    return (img, msg)

if __name__ == '__main__':
    img = cv2.imread("fwd/Left2.jpg")
    img,m = detect(img)

    # cap = cv2.VideoCapture('video1.mp4') 
    while True:
        # ret,img = cap.read()
        # if not ret:
        #   break
        # img = cv2.flip(img, -1)
        # img = detect(img)
        cv2.imshow("winname", img)
        # print(turn)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
