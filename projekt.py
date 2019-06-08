import numpy as np
import cv2 as cv

filePath = 'here goes your movie path'
cap = cv.VideoCapture(filePath)
h1=s1=v1=h2=s2=v2=0
def on_trackbar_h1(val):
    global h1
    h1=val
    print('h1=',h1)
def on_trackbar_s1(val):
    global s1
    s1=val
    print('s1=',s1)
def on_trackbar_v1(val):
    global v1
    v1=val
    print('v1=',v1)
def on_trackbar_h2(val):
    global h2
    h2=val
    print('h2=',h2)
def on_trackbar_s2(val):
    global s2
    s2=val
    print('s2=',s2)
def on_trackbar_v2(val):
    global v2
    v2=val
    print('v2=',v2)
cv.namedWindow("test", cv.WINDOW_AUTOSIZE);
cv.createTrackbar("h1", "test" , 0, 255, on_trackbar_h1)
cv.createTrackbar("s1", "test" , 0, 255, on_trackbar_s1)
cv.createTrackbar("v1", "test" , 0, 255, on_trackbar_v1)
cv.createTrackbar("h2", "test" , 0, 255, on_trackbar_h2)
cv.createTrackbar("s2", "test" , 0, 255, on_trackbar_s2)
cv.createTrackbar("v2", "test" , 0, 255, on_trackbar_v2)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    canvas = frame.copy()
    

    lower = (h1,s1,v1)  #120,150,80
    upper = (h2,s2,v2) #150,250,120
    print(lower)
    print(upper)
    mask = cv.inRange(hsv, lower, upper)
    # try:
    # NB: using _ as the variable name for two of the outputs, as they're not used
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    for c in contours:
        M = cv.moments(c)
        #print(M)
        if(M["m00"]!=0):
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv.circle(frame, center, 2, (0,0,255), 10)

    # except (ValueError, ZeroDivisionError):
    #     pass
    
    cv.imshow('frame',frame)
    #cv.imshow('canvas',canvas)
    cv.imshow('mask',mask)
    # Our opythonperations on the frame come here
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    if cv.waitKey(30) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()