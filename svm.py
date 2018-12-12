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
from get_prices import make_map, fun
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential


def lstm():
    features = pd.read_csv('data.csv')
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
    Y = pd.get_dummies(features['AVG_TRIPS'])
    features = pd.get_dummies(features)
    print(features.head())
    labels = np.array(features['AVG_TRIPS'])
    # features= features.drop('AVG_TRIPS', axis = 1)
    feature_list = list(features.columns)
    features = np.array(features)

    embed_dim = 256
    lstm_out = 250
    batch_size = 128

    model = Sequential()
    model.add(Embedding(3500, embed_dim,input_length = features.shape[1], dropout = 0.4))
    model.add(LSTM(lstm_out, dropout_U = 0.4, dropout_W = 0.4))
    model.add(Dense(32,activation='softmax'))
    model.compile(loss = 'mean_squared_error', optimizer='adam',metrics = ['accuracy'])
    print(model.summary())
    
    train_features, test_features, train_labels, test_labels = train_test_split(features, Y, test_size = 0.25, random_state = 42)
    # # X_train, X_valid, Y_train, Y_valid = train_test_split(X,Y, test_size = 0.20, random_state = 36)

    # #Here we train the Network.

    model.fit(train_features, train_labels, batch_size =batch_size, nb_epoch = 5, verbose = 10)
    score,acc = model.evaluate(test_features, test_labels, verbose = 2, batch_size = batch_size)
    print("Logloss score: %.2f" % (score))
    print("Validation set Accuracy: %.2f" % (acc))




# Categorizes the ridership according to the congestion level of 1-3
#Reads modded.csv and stores result in categorized.csv
def categorize_ridership():
    # print(csvFile.head(0))
    # our current categories are as follows: <10=1 <20=2 >20=3
    csvFile = pd.read_csv('modded.csv')
    for i,row in csvFile.iterrows():
        val=0
        if row['AVG_TRIPS'] <10:
            val=1
        elif row['AVG_TRIPS'] <20:
            val=2
        elif row['AVG_TRIPS'] > 20:
            val=3
        csvFile.set_value(i, 'congestion_level', val)
    csvFile.to_csv("categorized.csv", index=False)


# Uses the congestion level to compute on the prices
# reads categorized.csv and stores result in final.csv
def compute_final_prices():
    csvFile = pd.read_csv('categorized.csv')
    before_discount = 0
    after_discount = float(0)
    station_and_codes = make_map()
    stations = {}
    print("station names from csv given as follow\n")
    sno = 0
    for i,row in csvFile.iterrows():
        val=0
        #we call the api here to get the cost 
        #TODO: replace old_cost with api response 
        # print(row['ENTSTATION'],row['EXTSTATION'])
        ent_station = row['ENTSTATION']
        ext_station = row['EXTSTATION']
        if(ent_station == ext_station):
            continue
        # old_cost = 100
        stations[row['ENTSTATION']] = 1
        old_cost = fun(station_and_codes[ent_station], station_and_codes[ext_station])
        # print(type(before_discount))
        # print(str(sno) + ". " + ent_station + " " + ext_station)
        # sno = sno + 1
        before_discount = before_discount + old_cost
        discount = row['congestion_level']/(10*1.0)
        new_cost = old_cost - old_cost * discount
        after_discount = after_discount + new_cost
        csvFile.set_value(i, 'old_cost', old_cost)
        csvFile.set_value(i, 'new_cost', new_cost)
    # print(length(stations))
    print("Cost before discount: ")
    print(before_discount)
    print("Cost after discount: ")
    print(after_discount)
    csvFile.to_csv("final.csv", index=False)


# Makes the file ready for business logic 
# reads data.csv and the ready file is in modded.csv
def create_extra_columns():
    csvFile = pd.read_csv('data.csv')
    csvFile['congestion_level'] = ''
    csvFile['old_cost'] = ''
    csvFile['new_cost'] = ''
    csvFile.to_csv('modded.csv',index=False)


def read_csv():
    features = pd.read_csv('data.csv')
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
    create_extra_columns()
    categorize_ridership()
    compute_final_prices()
    return features

# read_csv()
lstm()

