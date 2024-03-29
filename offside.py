import numpy as np
import cv2 as cv
import json
from time import sleep

config = {}
with open('config.json',"r+") as config_file:
    config = json.loads(''.join(config_file.readlines()))
filePath = config['filepath']

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
if config['debug']=='True':
    cv.namedWindow("test", cv.WINDOW_AUTOSIZE);
    cv.createTrackbar("h1", "test" , 0, 179, on_trackbar_h1)
    cv.createTrackbar("s1", "test" , 0, 255, on_trackbar_s1)
    cv.createTrackbar("v1", "test" , 0, 255, on_trackbar_v1)
    cv.createTrackbar("h2", "test" , 0, 179, on_trackbar_h2)
    cv.createTrackbar("s2", "test" , 0, 255, on_trackbar_s2)
    cv.createTrackbar("v2", "test" , 0, 255, on_trackbar_v2)
lower1 = (config['teams'][0]['h'][0],config['teams'][0]['s'][0],config['teams'][0]['v'][0])  
upper1 = (config['teams'][0]['h'][1],config['teams'][0]['s'][1],config['teams'][0]['v'][1]) 
lower2 = (config['teams'][1]['h'][0],config['teams'][1]['s'][0],config['teams'][1]['v'][0])  
upper2 = (config['teams'][1]['h'][1],config['teams'][1]['s'][1],config['teams'][1]['v'][1]) 
grass_lower = (config['grass']['h'][0],config['grass']['s'][0],config['grass']['v'][0])  
grass_upper = (config['grass']['h'][1],config['grass']['s'][1],config['grass']['v'][1]) 


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

def get_more_left(team_pos, selected_value):
    return [pos for pos in team_pos if pos[0]<selected_value]

def get_more_right(team_pos, selected_value):
    return [pos for pos in team_pos if pos[0]>selected_value]

while True:
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    canvas = frame.copy()
    if config['debug']=='True':
        lower = (h1,s1,v1)  
        upper = (h2,s2,v2) 
        mask = cv.inRange(hsv, lower, upper)
    mask1 = cv.inRange(hsv, lower1, upper1)
    mask2 = cv.inRange(hsv, lower2, upper2)
    grass_mask = cv.inRange(hsv, grass_lower, grass_upper)
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
                if(M["m00"]!=0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if(cv.pointPolygonTest(grass_contour,center,False)>0):
                        cv.circle(frame, center, 2, (0,0,255), 10)
                        left_team_pos.append(center)
        right_team_pos = []
        for c in contours2:
            if(cv.contourArea(c)>config["min_player_area"]):
                M = cv.moments(c)
                if(M["m00"]!=0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if(cv.pointPolygonTest(grass_contour,center,False)>0):
                        cv.circle(frame, center, 2, (255,0,0), 10)
                        right_team_pos.append(center)

        most_right_def = get_most_right(right_team_pos)
        more_right_atk = get_more_right(left_team_pos, most_right_def[0])
        most_left_def = get_most_left(left_team_pos)
        more_left_atk = get_more_left(right_team_pos, most_left_def[0])
        
       
        for more_right_attacker in  more_right_atk:
            if most_right_def[0] < more_right_attacker[0]:
                cv.circle(frame, more_right_attacker, 2, (0, 0, 0), 20)      # black
        for more_left_attacker in  more_left_atk:
            if most_left_def[0] > more_left_attacker[0]:
                cv.circle(frame, more_left_attacker, 2, (255, 255, 255), 20) # grey
    if config['debug']=='True':           
        cv.imshow('mask',mask)
    cv.imshow('frame',frame)
    if cv.waitKey(config["frame_delay"]) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()