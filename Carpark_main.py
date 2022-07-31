import cv2
import numpy as np
import pickle
import cvzone


cap = cv2.VideoCapture("image/car_parking.mp4")

with open('CarParkPos','rb') as f:
    posList = pickle.load(f)

width, height = 53, 25

def checkParkingSpace(imgProcess):

    spaceCounter = 0

    for pos in posList:
        x, y = pos
        # cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height),(255,0,255),2)
        imgCrop = imgProcess[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        
        if count < 300:
            color = (0,255,0)
            thickness = 3
            spaceCounter += 1

        else: 
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height), color, thickness)
        cvzone.putTextRect(frame,str(count),(x,y+height-3),scale=1, thickness=1, offset=0, colorR=color)



    cvzone.putTextRect(frame,f'Free : {spaceCounter}/{len(posList)}',(50, 60),scale=4, thickness=5, offset=15, colorR=(0,255,0))



while True:
   
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, frame = cap.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray, (3,3),1)
    frameThreshold = cv2.adaptiveThreshold(frameBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    frameMedian = cv2.medianBlur(frameThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    frameDilate = cv2.dilate(frameMedian,kernel,iterations=1)
    checkParkingSpace(frameDilate)

    # for pos in posList:
    #     cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height),(255,0,255),2)

    cv2.imshow("Image", frame)
    # cv2.imshow("ImageThres", frameMedian)
    if cv2.waitKey(30) & 0xFF == ord("e"):
        break 

cap.release()
cv2.destroyAllWindows()