from sklearn.preprocessing import MultiLabelBinarizer
import csv
import numpy as np
from sklearn.svm import SVR
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from sklearn.preprocessing import OneHotEncoder

def read_csv():
    features = pd.read_csv('data.csv')
    #hot encoder
    features = pd.get_dummies(features, columns=['ENTDATEDAYOFWEEK', 'ENTQUARTHOUR',])
    print features.head(5)


#binarizer
mlb = MultiLabelBinarizer()
a = mlb.fit_transform([set(['Navy Yard','Takoma']), set(['Anacostia','U Street-Cardozo']), set(['Crystal City','Metro Center'])])
days = ['Wed', 'Thu', 'Fri']
density = [3,3,2]
read_csv()
# encode = pd.get_dummies(days)
# print encode
# print days
svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)
svr_rbf.fit(a, density)
# print svr_rbf.predict([[0,1,1,0,0,0]])[0]
# print a
# print list(mlb.classes_)