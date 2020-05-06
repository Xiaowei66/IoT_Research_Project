# import python flask lbrary
from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response

# import timestamp library
from datetime import datetime

# import the function that we design in convert.py file
from convert import output_current_coordiantes

# import the function that we design in convert_b1.py file
from convert_b1 import b1_output_current_coordiantes

# import the function that we design in evaluate.py file
from evaluate import evaluate_edge

# import the function from label_coordinates_table.py
from label_coordinates_table import transfer

# import the model prediction
from knn_train import predict_knn

import pandas as pd
import numpy as np
import random

from knn_train_csv import train_knn_path
from knn_train_csv import predict_label

import time
# test set path
test_data_path = '6733_processed_data.csv'
test_df=pd.read_csv(test_data_path, delimiter=',')
test_data = test_df.drop('Unnamed: 0',1)

# initalize the modal
knn_modal = 0
knn_circle = 0

# I refer the video instruction form Julian Nash in YouTube (https://www.youtube.com/watch?v=QKcVjdLEX_s&t=204s)
# If you have any doubts about Python Flask, please refer the video
app = Flask(__name__)
# test message
@app.route("/display")
def output():
    return render_template("display.html")

@app.route("/path")
def path():
    return render_template("path.html")

@app.route("/display/data.csv")
def data():
    return render_template("label_coor.csv")

# define the root page of the server, link it to the index.html
@app.route("/")
def index():
    return render_template("index.html")



@app.route("/training", methods = ['POST'])
def training():

    global knn_circle
    global knn_modal

    train_data = request.get_json()
    print(train_data)

    csv_path = train_data["csv_path"]
    pre_path = train_data["pre_path"]
    csv_level = train_data["level"]

    if (knn_circle == 0):

        knn_modal = train_knn_path(csv_path)
        knn_circle = knn_circle +1


    # get the data from pre_path

    pre_data_df=pd.read_csv(pre_path, delimiter=',')
    p_data = pre_data_df.drop('Unnamed: 0',1)

    print("the predict data length:")
    print(len(p_data))

    p_length = len(p_data)

    lan_list = []
    lat_list = []
    label_list = []

    for i in range(p_length):

        row_data = [p_data.iloc[i][1:]]

        p_label = predict_label(knn_modal,row_data )
        p_label = int(p_label[0])

        p_coo = output_current_coordiantes(-2,p_label)

        lan_v = (round(float(p_coo[1]),6))
        lat_v = (round(float(p_coo[0]),6))

        evaluate_v = evaluate_edge(csv_level,p_label,lan_v,lat_v)
        lan_v = str(round(evaluate_v[0],6))
        lat_v = str(round(evaluate_v[1],6))

        lan_list.append(lan_v)
        lat_list.append(lat_v)
        label_list.append(str(p_label))

        lan_str_list = ','.join(lan_list)
        lat_str_list = ','.join(lat_list)
        lab_str_list = ','.join(label_list)

    res_3 = make_response(jsonify({"lan":lan_str_list,"lat":lat_str_list,"label":lab_str_list}),200)

        #res_3 = make_response(jsonify({"lan":lan_v,"lat":lat_v,"label":p_label}),200)

        #time.sleep(2)

    # #number_pool = list(range(300))
    # #s_row = random.choice(number_pool)
    # print(p_data.iloc[0])
    # test_row = [p_data.iloc[0][1:]]
    # print(test_row)

    # p_label = predict_label(knn_modal,test_row)
    # p_label = int(p_label[0])
    # print(type(p_label))

    # p_coo = output_current_coordiantes(-2,p_label)

    # # modify the lantitude and langitude to correct style
    # lan_v = (round(float(p_coo[1]),6))
    # lat_v = (round(float(p_coo[0]),6))

    # evaluate_v = evaluate_edge(csv_level,p_label,lan_v,lat_v)
    # lan_v = str(round(evaluate_v[0],6))
    # lat_v = str(round(evaluate_v[1],6))

    # print("TTTTTTTTTTTTT")
    # print(lan_v)
    # print(lat_v)
    # print(int(p_label))

    # res_3 = make_response(jsonify({"lan":lan_v,"lat":lat_v,"label":p_label}),200)   

    return res_3







#define the backend train model logic
@app.route("/train_model", methods = ['POST'])
def trainer():

    tm_data = request.get_json()
    print(tm_data)

    train_mark = int(tm_data["train"])

    print("Message from Train Model")
    print(train_mark)

    if (train_mark == 1):

        number_pool = list(range(300))
        s_row = random.choice(number_pool)
        test_row = [test_data.iloc[s_row][1:]]
        predicted_label = int(predict_knn(test_row))

        # after we get the predicted label, we can get the corresponding coordinates

        p_coo = output_current_coordiantes(-2,predicted_label)

    # set a default level lg
    level_v = "lg"
    
    str_test_row = str(test_row)
    # modify the lantitude and langitude to correct style
    lan_v = (round(float(p_coo[1]),6))
    lat_v = (round(float(p_coo[0]),6))

    print("This is the Predicted (LAN, LAT)")
    print(lan_v,lat_v)

    # evaluate the localization
    # without the evaluation, the 
    evaluate_v = evaluate_edge(level_v,predicted_label,lan_v,lat_v)
    lan_v = str(round(evaluate_v[0],6))
    lat_v = str(round(evaluate_v[1],6))
    print("After Evaluation")
    print(lan_v,lat_v)

    # summarize the label and coordinates table
    

    # send the data back to frontend
    res_2 = make_response(jsonify({"lan":lan_v,"lat":lat_v,"label":predicted_label,"raw_message":str_test_row}),200)   

    return res_2


# define the backend logic
@app.route("/receiver", methods = ['POST'])
def worker():

    # receive the data from frontend
    data = request.get_json()
    
    print(data)

    # convert string to int
    label_v = int(data["label"])
    level_v = str(data["level"])
    print(label_v)
    print(level_v)

    # Here  1 means Lowerground Floor
    #       2 means Upperground Floor
    #      -1 means Basement 1
    #      -2 means Basement 2
    # you can adjust by yourself here
    if ( level_v == "lg"):
        print("YYYYYYYYY")
        # due the the grid designing error (did't follow the same to logic and standard to design Lowerground and Basement 1)
        # we need to divide into different coordiantes converting logic
        coo = output_current_coordiantes(-2,label_v)
        
    else:
        coo = b1_output_current_coordiantes(415,label_v)
    #coo = output_current_coordiantes(-2,label_v)
    
    print(coo)
    # modify the lantitude and langitude to correct style
    lan_v = (round(float(coo[1]),6))
    lat_v = (round(float(coo[0]),6))

    print("This is the Predicted (LAN, LAT)")
    print(lan_v,lat_v)

    # evaluate the localization
    # without the evaluation, the 
    evaluate_v = evaluate_edge(level_v,label_v,lan_v,lat_v)
    lan_v = str(round(evaluate_v[0],6))
    lat_v = str(round(evaluate_v[1],6))
    print("After Evaluation")
    print(lan_v,lat_v)

    # summarize the label and coordinates table
    

    # send the data back to frontend
    res = make_response(jsonify({"lan":lan_v,"lat":lat_v}),200)   
    return res

transfer()

if __name__ == "__main__":

    # define the demo IP, and the port
    # please bbe aware of the port restriction
    # sometimes, if you want to restart the server, remember to kill the port!
    app.run()