import cv2
import numpy as np
frame_width = 640
frame_height = 480
cap = cv2.VideoCapture(0)
cap.set(3,frame_width)
cap.set(4,frame_height)
cap.set(10,100)

myColors = [[28,129,94,120,255,255]]

myPoints = []   #[x,y]


def findColor(img,myColors):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    newpoints = []
    lower = np.array(myColors[0][0:3])
    upper = np.array(myColors[0][3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    x,y = getContours(mask)
    cv2.circle(imgResult,(x,y),10,(255,255,0),cv2.FILLED)
    #cv2.imshow("mask",mask)
    if x!=0 and y!=0:
        newpoints.append([x,y])
    return newpoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y


def drawOnCanvas(mypoints):
    for point in mypoints:
            cv2.circle(imgResult,(point[0],point[1]),10,(255,255,0),cv2.FILLED)




while True:
    success,img = cap.read()
    imgResult = img.copy()
    newpoints = findColor(img,myColors)
    if len(newpoints)!=0:
        for newP in newpoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints)
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == 'q':
        break
