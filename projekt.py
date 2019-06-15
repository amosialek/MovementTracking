import numpy as np
import cv2 as cv
import json
from time import sleep

config = {}
with open('config.json',"r+") as config_file:
    config = json.loads(''.join(config_file.readlines()))
filePath = '/home/albert/Downloads/3fa4626e80d48bb7984d2dd5c19731ac14406429-720p__66006.mp4'

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
lower1 = (config['teams'][0]['h'][0],config['teams'][0]['s'][0],config['teams'][0]['v'][0])  #120,150,80
upper1 = (config['teams'][0]['h'][1],config['teams'][0]['s'][1],config['teams'][0]['v'][1]) #150,250,120
lower2 = (config['teams'][1]['h'][0],config['teams'][1]['s'][0],config['teams'][1]['v'][0])  #120,150,80
upper2 = (config['teams'][1]['h'][1],config['teams'][1]['s'][1],config['teams'][1]['v'][1]) #150,250,120
grass_lower = (config['grass']['h'][0],config['grass']['s'][0],config['grass']['v'][0])  #120,150,80
grass_upper = (config['grass']['h'][1],config['grass']['s'][1],config['grass']['v'][1]) #150,250,120


def get_most_right(team_pos):
    most_right = (0, 0)
    for pos in team_pos:
        if pos[0] > most_right[0]:
            most_right = pos
    return most_right


def get_most_left(team_pos):
    most_left = (10000000, 0)
    for pos in team_pos:
        if pos[0] < most_left[0]:
            most_left = pos
    return most_left


while True:
    # print(config["filepath"])
    # print(config['teams'])
    # Capture frame-by-frame
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    canvas = frame.copy()

    lower = (h1,s1,v1)  #120,150,80
    upper = (h2,s2,v2) #150,250,120
    # print(lower)
    # print(upper)
    mask1 = cv.inRange(hsv, lower1, upper1)
    mask2 = cv.inRange(hsv, lower2, upper2)
    grass_mask = cv.inRange(hsv, grass_lower, grass_upper)
    # try:
    # NB: using _ as the variable name for two of the outputs, as they're not used
    contours1, _ = cv.findContours(mask1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours2, _ = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    grass_contour = max(cv.findContours(grass_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[0], key = cv.contourArea)
    if(cv.contourArea(grass_contour)>config["grass_min_area"]):
        M = cv.moments(grass_contour)
        grass_center = (0, 0)
        if(M["m00"]!=0):
            grass_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv.circle(frame, grass_center, 2, (0,255,0), 10)
        left_team_pos = []
        for c in contours1:
            if(cv.contourArea(c)>config["min_player_area"]):
                M = cv.moments(c)
                #print(M)
                if(M["m00"]!=0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if(cv.pointPolygonTest(grass_contour,center,False)>0):
                        cv.circle(frame, center, 2, (0,0,255), 10)
                        left_team_pos.append(center)
                # print(cv.contourArea(c))
        right_team_pos = []
        for c in contours2:
            if(cv.contourArea(c)>config["min_player_area"]):
                M = cv.moments(c)
                #print(M)
                if(M["m00"]!=0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if(cv.pointPolygonTest(grass_contour,center,False)>0):
                        cv.circle(frame, center, 2, (255,0,0), 10)
                #print(cv.contourArea(c))

        most_right_def = get_most_right(right_team_pos)
        most_right_atk = get_most_right(left_team_pos)
        most_left_def = get_most_left(left_team_pos)
        most_left_atk = get_most_left(right_team_pos)
        # cv.circle(frame, most_right_atk, 2, (255, 255, 0), 10)  # yellow
        # cv.circle(frame, most_right_def, 2, (0, 255, 255), 10)  # cyan
        # cv.circle(frame, most_left_atk, 2, (255, 0, 255), 10)   # magenta
        # cv.circle(frame, most_left_def, 2, (127, 127, 127), 10) # grey
        if most_right_def[0] < most_right_atk[0]:
            cv.circle(frame, most_right_atk, 2, (0, 0, 0), 10)      # black
        if most_left_def[0] > most_left_atk[0]:
            cv.circle(frame, most_left_atk, 2, (127, 127, 127), 10) # grey
    # except (ValueError, ZeroDivisionError):
    #     pass
    
    cv.imshow('frame',frame)
    #cv.imshow('canvas',canvas)
    cv.imshow('mask',grass_mask)
    # Our opythonperations on the frame come here
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    if cv.waitKey(30) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()