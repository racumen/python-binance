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
import grindfunc




client = Client("4y2FAri1QZdyNWjO6BLp1FSiO0sXmQcEVKTKZwjfRpaklSbfX3wcLWd5Ikx8M6nw","sgwdst1CBgUDj9HHz74i9O5eJ0Zx2ATuMJUCMCiezC8EaD6xuO8mUyTs10krefXt")




symbol1="BTC"
symbol2="BUSD"
string1 = client.get_asset_balance(symbol1)
string2 = client.get_asset_balance(symbol2)
print(symbol1+"\t"+string1["free"]+"\t"+symbol2+"\t"+string2["free"])

#order = client.order_market_buy(symbol=symbol1+symbol2,quantity=1)

#order = client.order_market_buy(symbol=symbol1+symbol2,quantity=0.001)

klines = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
 print(klines)

string1 = client.get_asset_balance(symbol1)
string2 = client.get_asset_balance(symbol2)
print(symbol1+"\t"+string1["free"]+"\t"+symbol2+"\t"+string2["free"])

cwdcw

























           
variables_definition=[
    {"name":"minutes","n_samples":1,"n_values":60},
    {"name":"15minutes","n_samples":15,"n_values":28},
    {"name":"hours","n_samples":60,"n_values":0},
    {"name":"6hours","n_samples":360,"n_values":0},
    ]

target_definition={"samples_from":5, "samples_to":120, "n_samples":10}

n_samples=0
n_values=0
for v in variables_definition:
    v["offset_values"]=n_values
    v["offset_samples"]=n_samples
    n_samples=n_samples+v["n_samples"]*v["n_values"]
    n_values=n_values+v["n_values"]
    
values=list(range(n_values))
df=grindfunc.import_samples("Binance_BTCUSDT_minute3.csv","2021-01-01")

h_samples=df.values.tolist()
print("Importati ",len(h_samples),"valori da",h_samples[-1],"a",h_samples[0])
print("Variabili",n_values)
print("Giorni",grindfunc.twodec(n_samples/60/24))
print("Vampioni",n_samples)

inpt=1
#inpt=input("Prepare to train model? y/n")
if 1 or inpt =="y":
    datefrom="2021-01-01"
    dateto="2021-03-01"
    train_X, train_y = grindfunc.preparetrain(df,datefrom,dateto,variables_definition,target_definition)
    np.savetxt("train_y4.csv", train_y, delimiter=",")
    np.savetxt("train_X4.csv", train_X, delimiter=",")
    

#inpt=input("Train model? y/n")
if 1 or inpt =="y":
    # Instantiate model with 1000 decision trees
    rf = RandomForestRegressor(n_estimators = 50, random_state = 42)
    # Train the model on training data
    rf.fit(train_X, train_y);
    dump(rf,"rf4.joblib")
    

