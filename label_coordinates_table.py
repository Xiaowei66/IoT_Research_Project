
# import the function that we design in convert.py file
from convert import output_current_coordiantes

# import the function that we design in convert_b1.py file
from convert_b1 import b1_output_current_coordiantes

import csv

import os

# the label of underfround floor
# label from -2 to 235
def transfer():
    label_list = list(range(-2,236,1))
    #print(label_list)
    #rmove
    if os.path.exists('templates/label_coor.csv'):
        os.remove('templates/label_coor.csv')

    with open('templates/label_coor.csv','w',newline="") as label_coor:

        writer = csv.writer(label_coor)

        writer.writerow(["Label","Lantitude","Longtitude"])

        for label_v in label_list:

            coo = output_current_coordiantes(-2,label_v)

            label_str = str(label_v)
            lan_v = str(round(float(coo[1]),6))
            lat_v = str(round(float(coo[0]),6))

            writer.writerow([label_str, lan_v, lat_v])




