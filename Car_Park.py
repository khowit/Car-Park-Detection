import cv2
import pickle


try:
    with open('CarParkPos','rb') as f:
        posList = pickle.load(f)
except:
        posList = []

# frame = cv2.resize(frame,(1000,450))
width, height = 53, 25

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open('CarParkPos','wb') as f:
        pickle.dump(posList, f)


while True:
    # success, frame = cap.read()
    frame = cv2.imread('image/park2.png')
    for pos in posList:
        cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height),(255,0,255),2)
         
    cv2.imshow("Image", frame)
    cv2.setMouseCallback("Image",mouseClick)
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break 

# cap.release()
# cv2.destroyAllWindows()