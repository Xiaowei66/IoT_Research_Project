
# evaluate the coordinate that we calculate,
def evaluate_edge(level_v,label_v,lan_v,lat_v):

    # Currently, I only 
    # in the Lowground floor
    if (level_v == "lg"):

        if (label_v <= 14):
            # evaluate level 1 left column
            lan_v = lan_v + 0.000021
            lat_v = lat_v + 0.000006

            # evaluate level 1 top row
        if (label_v in [15,32,49,66,83,100,117,134,151,168,185,202,219]):
            lan_v = lan_v + 0.000008
            lat_v = lat_v - 0.000020
    

    if (level_v == "b1"):
        if (label_v <= 14):
            # evaluate level 1 left column
            lan_v = lan_v + 0.000021
            lat_v = lat_v + 0.000006

            # evaluate level 1 top row
        if (label_v in [15,32,49,66,83,100,117,134,151,168,185,202,219]):
            lan_v = lan_v + 0.000008
            lat_v = lat_v - 0.000020
            
    return [lan_v,lat_v]
