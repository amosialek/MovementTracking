To run this program type:

python3 offside.py

python3 with python opencv installed is required.
This project has been developed under python 3.6.3 and opencv-python in 4.1.0.25 although it should be also compatible with newer versions.

Configuration
The project has configuration file 'config.json' with following configurtion:
{
    "debug":"False"
    "filepath":"path/to/football/video",
    "teams":
    [        
        {"h":[lower_bound_of_hue,upper_bound_of_hue],"s":[lower_bound_of_saturation,upper_bound_of_saturation],"v":[lower_bound_of_value,upper_bound_of_value]},
        {"h":[0,20],"s":[74,255],"v":[134,255]}
        
    ],
    "grass":{"h":[40,50],"s":[0,255],"v":[0,255]},
    "grass_min_area":100000,
    "min_player_area": 50,
    "frame_delay":15
}

teams should consist of 2 elements with bounds for hsv values of team shirts colors
grass contains bounds for grass color (it is needed to get boundary of the pitch)
grass min area - minimal area of grass to be taken as pitch
min_player_area - the same as above for players - it prevents small blobs like faces to be recognized as player
frame_delay - delay between frame to prevent playing the video too fast

This program searches for all blobs of team colors specified in config inside the biggest green blob in the current frame (score and tv logo are usually outside). In each frame program compares positions of players and checks if they are in offside position (simply by checking if their x coordinates on the image is lower/higher than all of the opponent team players). If they are, program will mark them with either white or black dot.

Program also contains also two debug windows which helps with finding color of players. One of them consists of 6 trackbars which may be used to set boundaries and second window shows mask filtered by these boundaries. To show these windows change "debug" value in config to True.
