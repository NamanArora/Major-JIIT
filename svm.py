from sklearn.preprocessing import LabelEncoder
import csv
import numpy as np
from sklearn.svm import SVR
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def categorize_ridership(csvFile):
    for i,row in csvFile.iterrows():
        val=1
        if condition:
            val=2;
        else if condition:
            val=3;

        csvFile.set_value(i, 'congestion_level', val)

def read_csv():
    features = pd.read_csv('data.csv')
    categorize_ridership(features)
    print(features.head())
    print(features.shape)
    binarizer1=LabelEncoder()
    binarizer2=LabelEncoder()
    print('Binarizing the station names...')
    features.iloc[:,1:2]=binarizer1.fit_transform(features.iloc[:,1:2])
    features.iloc[:,2:3]=binarizer2.fit_transform(features.iloc[:,2:3])
    # print(features.head())
    #hot encoder
    print('Hot encoding the features...')
    features = pd.get_dummies(features)
    print(features.head())
    labels = np.array(features['AVG_TRIPS'])
    features= features.drop('AVG_TRIPS', axis = 1)
    feature_list = list(features.columns)
    features = np.array(features)
    svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
    print('Training Features Shape:', train_features.shape)
    print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    print('Testing Labels Shape:', test_labels.shape)
    print('Training data in progress...')
    svr_rbf.fit(train_features, train_labels)
    predictions = svr_rbf.predict(test_features)
    errors = abs(predictions - test_labels)
    print('Mean Absolute Error:', round(np.mean(errors), 2), '.')
    return features


#binarizer
# mlb = MultiLabelBinarizer()
# a = mlb.fit_transform([set(['Navy Yard','Takoma']), set(['Anacostia','U Street-Cardozo']), set(['Crystal City','Metro Center'])])

read_csv()
# encode = pd.get_dummies(days)
# print encode
# print day
# print svr_rbf.predict([[0,1,1,0,0,0]])[0]
# print a
# print list(mlb.classes_)



