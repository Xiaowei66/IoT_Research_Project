import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def train_knn_path(path):
    
    data_path = path
    df=pd.read_csv(data_path, delimiter=',')

    data = df.drop('Unnamed: 0',1)

    features = data.drop('Label',axis=1).values
    label = data['Label'].values

    X_train,X_test,y_train,y_test = train_test_split(features,label,test_size=0.3,random_state=42)

    #Setup a knn classifier with k neighbors
    knn = KNeighborsClassifier(n_neighbors=1)
    #Fit the model
    knn.fit(X_train,y_train)

    print("Training Done")

    return knn

def predict_label(model_knn,data):
    #let us get the predictions using the classifier we had fit above
    label_p = model_knn.predict(data)

    return label_p

    






    