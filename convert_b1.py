
# import the Python geopy library
import geopy as g 
import geopy.distance as gp 
from geopy.units import radians
import math

#################################################################
# This part, i refer the programming from https://blog.csdn.net/weixin_42649077/article/details/92560687
from sympy import *
from math import radians, cos, sin, asin, sqrt

class Get_new_gps():
    def __init__(self):
        # define the radius of earth (6371 * 1000m)
        self.R = 6371 * 1000
        pass

    # with the original (lat, lng), the distance and angle, figure out the destination (lat, lng)
    def get_new_lng_angle(self, lng1, lat1, dist=500, angle=30):

        lat2 = 180 * dist*sin(radians(angle)) / (self.R * pi) + lat1
        lng2 = 180 * dist*cos(radians(angle)) / (self.R * pi * cos(radians(lat1))) + lng1
        return (lng2, lat2)
################################################################

# Define is the structure of basement
# the length of each square we define
lable_meter = 3

# the total number of rows
number_of_rows = 23

# the total number of columns
number_of_columns = 18

# The reference coordinates that we marked, we get the figure through google map
# the conversed coordinates (compared with google map)
coordiantes_of_start_point = [151.181655, -33.794509]

# define a function that output the coordinates with the input of distance and angle
def get_coordinates(start_ponit, dist, angle):
    # original coordinates
    lng1,lat1 = start_ponit

    # define the function from class
    functions = Get_new_gps()
    
    # get the predicted coordinates
    lng4, lat4 = functions.get_new_lng_angle(lng1, lat1, dist, angle)
    print("Current coordinates:%f,%f"%(lat4, lng4))
    ans = [lat4, lng4]
    
    # return the list
    return ans

# define a function to get the disctance from current point to label -2
def get_distance(start_label,current_label):
    # calculate the horizontal length
    horizontal_len = lable_meter*((current_label-start_label)//number_of_rows)
    # calculate the vertical length
    vertical_len = lable_meter*((current_label-start_label)%number_of_rows)
    
    # calculate the distance through pythagorean theorem
    distance = math.sqrt(horizontal_len*horizontal_len + vertical_len*vertical_len)
    print("The distance to the reference point:",distance)
    return distance

# define a function to calculate the angle between two coordinates
def get_angle(start_label,current_label):

    horizontal_len = (current_label-start_label)//number_of_rows
    vertical_len = (current_label-start_label)%number_of_rows
    distance = math.sqrt(horizontal_len*horizontal_len + vertical_len*vertical_len)
    
    
    if (horizontal_len == distance):

        # the original angle between our building and map horizontal 
        # we calculate this angle manually, please refer the 
        angle = 21.5
    else:
        # calculate the angle between two coordinates (anti-clock)
        
        A=math.degrees(math.acos((horizontal_len*horizontal_len-vertical_len*vertical_len-distance*distance)/(-2*vertical_len*distance)))
        A = round(A)
        B = 90-A
        
        if (B <= 21.5):
            angle = 21.5-B
        else:
            angle = 360-(B-21.5)
    
    print("The angle of this point:",angle)
    return angle

# define a function that will be called in the backend file
def b1_output_current_coordiantes(start_label,current_label):
    
    dist = get_distance(start_label,current_label)

    angle = get_angle(start_label,current_label)
    # calculate the coordinates
    current_coordinates = get_coordinates(coordiantes_of_start_point, dist, angle)
    
    return current_coordinates

# (-2 means: the label that you used to refer, 232: means the label that you want to get coordinates)
# in this project we refer label -2 and it's coordinates is coordiantes_of_start_point = [-33.794508, 151.181634]
