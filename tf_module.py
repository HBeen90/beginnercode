#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:10:07 2026

@author: hyobeen
"""


import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.datasets import fashion_mnist, mnist

from sklearn.metrics import pairwise_distances, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Flatten
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.models import Sequential

from datetime import datetime
from IPython.display import display, Image

import urllib.request
import PIL.Image as PIL_image

import yfinance as yf
import warnings

from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import RandomizedSearchCV

from scipy.stats import loguniform, randint

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import plot_tree
from sklearn.metrics import mean_absolute_error as MSE

from xgboost import XGBRegressor, XGBClassifier
import xgboost as xgb

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

from sklearn.pipeline import Pipeline

def train_sec():
    tf.keras.utils.set_random_seed(42)
    tf.config.experimental.enable_op_determinism()
    (train_input, train_target), (test_input, test_target) = keras.datasets.fashion_mnist.load_data()
    a=train_input.shape
    b=train_target.shape
    c=test_input.shape
    d=test_target.shape
    #print(a,b,c,d)

    fig, axs = plt.subplots(1,10, figsize = (10,10))
    for i in range(10):
        axs[i].imshow(train_input[i], cmap='gray_r')
        axs[i].axis('off')
    #plt.show()
    
    train_scaled = train_input /255.0
    train_scaled = train_scaled.reshape(-1, 28*28)
    #print(train_scaled.shape)
    
    train_scaled, val_scaled, train_target, val_target = train_test_split(train_scaled, train_target,
                                                                          test_size = 0.2, random_state =42)
      
    a1 = train_scaled.shape
    b1 = train_target.shape
    c1 = val_scaled.shape
    d1 = val_target.shape
    #print(a1, b1, c1, d1)
    
    #print(train_scaled[0].shape)
    '''
    dense =keras.layers.Dense(10,activation = 'softmax', input_shape = train_scaled[0].shape)
    model = keras.Sequential([dense])
    model.compile(loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
    model.fit(train_scaled, train_target, epochs =5)
    model.evaluate(val_scaled, val_target)
    '''

    train_cat = to_categorical(train_target)
    val_cat = to_categorical(val_target)
    a2 = train_cat.shape
    b2 = val_cat.shape
    print(a2, b2)
    
    model = keras.Sequential()
    model.add(keras.layers.Dense(10, activation = 'softmax', input_shape =train_scaled[0].shape))
    model.compile(loss='categorical_crossentropy', metrics = ['accuracy'])
    model.fit(train_scaled, train_cat, epochs =5)
    model.evaluate(val_scaled, val_cat)    
    
def Conv2D():
    tf.keras.utils.set_random_seed(42)
    tf.config.experimental.enable_op_determinism()
    (train_input, train_target), (test_input, test_target)=fashion_mnist.load_data()
    a = train_input.shape
    b = train_target.shape
    c = test_input.shape
    d = test_target.shape
    
    #print(a,b,c,d)
    
    train_scaled = train_input.reshape(-1,28,28,1)/255.0
    
    #print(train_scaled.shape)
    
    train_scaled, val_scaled, train_target, val_target = train_test_split(train_scaled,
                                                                          train_target, test_size =0.2, random_state =42)
    
    a1 = train_scaled.shape 
    b1 = train_target.shape 
    c1 = val_scaled.shape 
    d1 = val_target.shape  
    
    #print(a1, b1, c1, d1)
    
    model = keras.Sequential()
    model.add(tf.keras.layers.Conv2D(32, kernel_size =(3,3), activation = 'relu',
                     padding = 'same', input_shape =(28,28,1)))
    model.add(MaxPooling2D(2))
    model.add(tf.keras.layers.Conv2D(64, kernel_size =(3,3), activation ='relu', 
                     padding = 'same'))
    model.add(MaxPooling2D(2))
    model.add(Flatten())
    model.add(Dense(100, activation = 'relu'))
    model.add(keras.layers.Dropout(0.4))
    model.add(Dense(10, activation = 'softmax'))    
    
    model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
    checkpoint_cb = keras.callbacks.ModelCheckpoint('best.model.h5',save_best_only =True)
    early_stopping_cb = keras.callbacks.EarlyStopping(patience=2, restore_best_weights = True)
    history = model.fit(train_scaled, train_target, epochs=20, validation_data = (val_scaled, val_target),
                        callbacks= [checkpoint_cb, early_stopping_cb])

    history.history.keys()
    #plt.plot(history.history['loss'])
    #plt.plot(history.history['val_loss'])
    #model.evaluate(val_scaled, val_target)
    
    test_scaled =test_input.reshape(-1,28,28,1)/255.0
    a2 =test_scaled.shape
    b2 =test_target.shape
    #print(a2,b2)
    
    conv = model.layer[0]
    fig, axs = plt.subplots(2,16, figsize =(15,2))
    for i in range(2):
        for j in range(16):
            axs[i,j].imshow(conv_weight[:,:,0, i*16+j], vmin=-0.5, vmax =0.5)
            axs[i,j].axis('off')
    plt.show()
     
    
def fashion():
    df = pd.read_csv('./data/fashion.csv')
    a=df[df.Gender =='Women'].Category.value_counts()
    #print(a)    
    df_Women_Footwear = df[df.Gender =='Women']
    url = df_Women_Footwear[df_Women_Footwear.ProductId == 54118].ImageURL.values[0]
    image = PIL_image.open(urllib.request.urlopen(url))
    image = image.resize((224,224))
    plt.imshow(image)
    #plt.show()    
    img_width, img_height =224,224
    train_data_dir = './data/data_3/Images/images_with_product_ids'

def seq2dataset(seq,window,horizon):
    X = []; Y =[]
    for i in range(len(seq)-(window+horizon)+1):
        x =  seq[i:(i+window)]
        y=(seq[i+window+horizon -1])
        X.append(x); Y.append(y)
        
    return np.array(X), np.array(Y)

    
def BTC(): 
    # 과거 7일 데이터, 다음날 1일 예측, LSTM
    df = pd.read_csv('./data/BTC_USD_2019-02-28_2020-02-27-CoinDesk.csv')
    seq = df[['Closing Price (USD)']].to_numpy()
    a = print(seq.shape)
    print(a)
    w =7
    h=1
    X, Y =seq2dataset(seq, w, h)
    #print(X[0], Y[0]); print(X[1])    
    
    split = int(len(X)*0.7)
    x_train = X[0:split]; y_train = Y[0:split]
    x_test = X[split:]; y_test = Y[split:]
    
    a1 = x_train.shape
    b1 = y_train.shape
    c1 = x_test.shape
    d1 = y_test.shape
    #print(a1, b1, c1, d1)    
    model = keras.Sequential()
    model.add(keras.layers.LSTM(128, activation='relu', input_shape = x_train[0].shape))
    model.add(keras.layers.Dense(1))
    model.compile(loss='mse', optimizer = 'adam', metrics =['mae'])
    hist = model.fit(x_train, y_train, epochs =100, validation_data = (x_test, y_test),verbose =2 )
    ev = model.evaluate(x_test, y_test)
    pred = model.predict(x_test)

    a2 = x_test.shape
    b2 = y_test.shape
    c2 = pred.shape
    print(a2,b2,c2)    
    
    
def BTC1():
    # 과거 7일 데이터, 다음날 1일 예측, Conv1D + LSTM
    df = pd.read_csv('./data/BTC_USD_2019-02-28_2020-02-27-CoinDesk.csv')
    seq = df[['Closing Price (USD)']].to_numpy()
    a = print(seq.shape)
    #print(a)
    w =7
    h=1
    X, Y =seq2dataset(seq, w, h)
    #print(X[0], Y[0]); print(X[1])    
    
    split = int(len(X)*0.7)
    x_train = X[0:split]; y_train = Y[0:split]
    x_test = X[split:]; y_test = Y[split:]
    
    a1 = x_train.shape
    b1 = y_train.shape
    c1 = x_test.shape
    d1 = y_test.shape
    #print(a1, b1, c1, d1)    
    model = keras.Sequential()
    model.add(keras.layers.Conv1D(filters =32, kernel_size =(3,), activation ='relu',input_shape = x_train[0].shape))
    model.add(keras.layers.LSTM(128, activation='relu'))
    model.add(keras.layers.Dense(1))
    model.compile(loss='mse', optimizer = 'adam', metrics =['mae'])
    hist = model.fit(x_train, y_train, epochs =100, validation_data = (x_test, y_test),verbose =2 )
    ev = model.evaluate(x_test, y_test)
    print(ev[0], ev[1])
    pred = model.predict(x_test)
    print('평균절대값백분율오차율(MAPE)', sum(abs(y_test-pred)/y_test)/len(x_test)*100)

    a2 = x_test.shape
    b2 = y_test.shape
    c2 = pred.shape
    print(a2,b2,c2)
    
    model.summary()    
    
import inspect
print(inspect.getfile(KFold))      
    
def kfold():
    iris = load_iris()
    features = iris.data
    label = iris.target
    
    X_train, X_test, y_train, y_test = train_test_split(iris_data.data, iris_data,target, test_size =0.2)
    
    a = features.shape
    b = label.shape 
    #print(a, b)
    
    kfold = KFold(n_splits=5)
    for train_index, val_index in kfold.split(features):
        #print('train: ', train_index)
        #print('val:', val_index)
        #print('--'*50)
        
        X_train = features[train_index]
        y_train = label[train_index]
        X_test = features[val_index]
        y_test = label[val_index]
    
    
        a1=X_train.shape
        b1=y_train.shape
        c1=X_test.shape
        d1=y_train.shape
        
        print(a1, b1, c1, d1)
    
        cv_acc= []
        dt_clf = DecisionTreeClassifier()
        for train_index, val_index in kfold.split(features):
            dt_clf.fit(features[train_index],label[train_index])
            dt_pred = dt_clf.predict(features[test_index])
            acc = accuracy_score(label[test_index], dt_pred)
            cv_acc.append(acc)
    
    iris_df = pd.DataFrame(data=iris.data, columns = iris.feature_names)
    
    print(iris.target)

    
def random_search_clf(params, runs =20,clf = DecisionTreeClassifier(random_state=2)):
    
    df = pd.read_csv('./data/census_cleaned.csv')
        
    X= df.iloc[:,:-1]
    y= df.iloc[:,-1]
    
    X_train, X_test, y_train, y_test = train_test_split(X,y, stratify =y, random_state =2)
    
    rand_clf = RandomizedSearchCV(clf, params, n_iter = runs, cv =5, n_jobs =-1, random_state =2)
    rand_clf.fit(X_train, y_train)
       
    best_model = rand_clf.best_estimator_
    best_score = rand_clf.best_score_
    print(np.round(best_score,3))
    print(rand_clf.best_params_)
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(np.round(acc,3))
    return best_model   



def learning_rate():
    df_bikes = pd.read_csv('./data/bike_rentals_cleaned.csv')
    X_bikes = df_bikes.iloc[:,:-1]
    y_bikes = df_bikes.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X_bikes, y_bikes, test_size =0.2, random_state =2)
   
  
    learning_rate_values = [0.001,0.01,0.05,0.1,0.15,0.2,0.3,0.5,1.0]
    rmse_list =[]
    for value in learning_rate_values:
        gbr = GradientBoostingRegressor(max_depth =2, n_estimators=30, random_state =2, learning_rate =value)
        gbr.fit(X_train,y_train)
        y_pred = gbr.predict(X_test)
        rmse = MSE(y_test, y_pred)**0.5
        rmse_list.append(rmse)
    print(rmse_list)
    return rmse_list

def plot_gbm_rmse(rmse_list=learning_rate(), x =None):
    values = [0.001,0.01,0.05,0.1,0.15,0.2,0.3,0.5,1.0]
    if x is None:
        x = range(len(rmse_list))
    plt.plot(x, rmse_list)
    plt.xlabel(values)
    plt.ylabel('RMSE')
    plt.grid()
    plt.show()
    
def subsmp():
    samples = [1,0.9,0.8,0.7,0.6,0.5]
    for sample in samples:
        gbr = GradientBoostingRegressor(max_depth=3, n_estimators =300, random_state =2,leanring_rate =0.1)
        gbr.fit(X_train, y_train)
        y_pred = gbr.predict(X_test)
        rmse = MSE(y_test, y_pred)**0.5
        print(sample, rmse)

def poly():
    X = np.arange(4).reshape(2,2)
    poly_ftr = PolynomialFeatures(degree=3).fit_transform(X)
    y = 1 + 2*poly_ftr[:,0] + 3*poly_ftr[:,0]**2 + 4*poly_ftr[:,1]**3
    model = Pipeline([('poly', PolynomialFeatures(degree=3)), ('linear', LinearRegression())])
    model.fit(X,y)
    
    A=np.round(model.named_steps['linear'].coef_,2)
    print(A)

            
    
    
    
    
    
    
    
    
    
    
    
    
    