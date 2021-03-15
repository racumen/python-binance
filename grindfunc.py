# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 22:49:00 2021

@author: f.romano
"""


# from datetime import datetime
from binance.client import Client
import pandas as pd
import statistics 
import matplotlib.pyplot as plt
import sklearn
from joblib import dump,load
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def calculate_values(samples, variables, values):
    #samples_mean=statistics.mean(samples)
    #samples_mean=0
    
    for v in variables:
        for i in range(v["n_values"]):
            values[v["offset_values"]+i]=twodec(1000*(statistics.mean(samples[v["offset_samples"]+v["n_samples"]*i:v["offset_samples"]+v["n_samples"]*(i+1)])-samples[0])/samples[0])
    #print(values)


def get_target(samples, target_definition):
    lissamp= [row[1] for row in samples[-target_definition["samples_to"]:-target_definition["samples_from"]]]
    maxval=quarterdec(100*(max(lissamp)-samples[-1][1])/samples[-1][1])
    return maxval

def import_samples(file,datefrom="2021-01-01", dateto="9999"):
    df=pd.read_csv(file,usecols=[1, 3],parse_dates=[1],skiprows=1)
    #print(df.head())
    df=df[df["date"]>datefrom]  
    df=df[df["date"]<dateto]
    df["open"] = pd.to_numeric(df["open"], downcast="float")
    #df["date"] = pd.to_datetime(df["date"])
    return df

def twodec(x):
    return round(x*100)/100
def onedec(x):
    return round(x*10)/10
def quarterdec(x):
    return round(x*4)/4

def preparetrain(df,datefrom,dateto,variables,target):
    df2=df[df["date"]>datefrom]  
    df2=df2[df2["date"]<dateto]
    n_samples=0
    n_values=0
    for v in variables:
        n_samples=n_samples+v["n_samples"]*v["n_values"]
        n_values=n_values+v["n_values"]
    X = np.empty((0,n_values), dtype='float')
    y = np.empty((0,1), dtype='float')
    
    values=list(range(n_values))

    h_samples=df2.values.tolist()
    samples=[]
    count=0
    for i in range(n_samples):
        #print("preshift",h_samples[-1])
        samples.insert(0,h_samples[-1][1])
        h_samples.pop(-1)
    while(len(h_samples)>target["samples_to"]):
        if not count%1:
            calculate_values(samples, variables,values)
            y=np.append(y,get_target(h_samples, target))
            X=np.append(X,[values], axis=0)
        samples.pop(-1)
        samples.insert(0,h_samples[-1][1]) 
        h_samples.pop(-1)
        count=count+1
        if not count%100:
            print(count,"shift ",h_samples[-1],y[-1])
    return X,y