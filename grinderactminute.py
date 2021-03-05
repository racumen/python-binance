    # -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:56:09 2021

@author: f.romano
"""
from datetime import datetime
from binance.client import Client
import pandas as pd
import statistics 
import sklearn
import numpy as np

def calculate_values(samples, variables, values):
    #samples_mean=statistics.mean(samples)
    samples_mean=0
    
    for v in variables:
        for i in range(v["n_values"]):
            values[v["offset_values"]+i]=statistics.mean(samples[v["offset_samples"]+v["n_samples"]*i:v["offset_samples"]+v["n_samples"]*(i+1)])-samples_mean
    #print(values)


def get_target(samples, target_definition):
    target_samples=samples[target_definition["samples_from"]:target_definition["samples_to"]]
    target_samples.sort(reverse=True)
    print(target_samples[:target_definition["n_samples"]])
    return 100*((statistics.mean(target_samples[:5])-samples[0])/samples[0])

def import_samples():
    df=pd.read_csv("Binance_BTCUSDT_minute.csv",usecols=[1, 3],parse_dates=[1],skiprows=1)
    #print(df.head())
    df["open"] = pd.to_numeric(df["open"], downcast="float")
    df["date"] = pd.to_datetime(df["date"])
    return df["open"].tolist()


h_samples= import_samples()
print(h_samples[:10])


variables_definition=[
    {"name":"minutes","n_samples":1,"n_values":5},
    {"name":"15minutes","n_samples":15,"n_values":1},
    {"name":"hours","n_samples":60,"n_values":1},
    {"name":"6hours","n_samples":360,"n_values":1},
    ]

target_definition={"samples_from":10, "samples_to":20, "n_samples":5}



n_samples=0
n_values=0

for v in variables_definition:
    v["offset_values"]=n_values
    v["offset_samples"]=n_samples
    n_samples=n_samples+v["n_samples"]*v["n_values"]
    n_values=n_values+v["n_values"]


samples=[]
for i in range(n_samples):
    #samples.append(h_samples[0])
    samples.append(0)
    h_samples.pop(0)
    
print(samples[:10])
print(n_samples)

values=list(range(n_values))

h_samples=list(range(1000))
count=0


size=1000


np_array = np.empty((0,4), dtype='float')

X=np.array()
y=np.array()

cs

while(len(h_samples)>target_definition["samples_to"]):
    samples.pop(-1)
    #samples.insert(0,h_samples[0]) 
    samples.insert(0,1) 
    h_samples.pop(0)
    calculate_values(samples, variables_definition,values)
    target=get_target(h_samples, target_definition)
    count+=1

    

    print(count,target,h_samples[:20])
    z=input("cazus ")
    if z != '':
        qwwq
    
    


dwcwd

values=[]





dede


client = Client("4y2FAri1QZdyNWjO6BLp1FSiO0sXmQcEVKTKZwjfRpaklSbfX3wcLWd5Ikx8M6nw","sgwdst1CBgUDj9HHz74i9O5eJ0Zx2ATuMJUCMCiezC8EaD6xuO8mUyTs10krefXt")

old_instant=0
dt=1
symbols=["BTCBUSD"]
savesize=3600


stats=[['minute']]


time_res = client.get_server_time()
info = client.get_exchange_info()
prices = client.get_all_tickers()

datatot=[]





#n_seconds=0















while(1):
    data=[]
    count=0
    while(count<savesize):
        try:
            prices = client.get_all_tickers()    
        except Exception as e: 
            print(e)
            break        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")    
        instant=int(current_time[-2:])
        if (instant-old_instant>=dt or (instant-old_instant<0 and instant-old_instant+60>=dt )):
            record=[current_time]
            for p in prices:
                if p['symbol'] in symbols:
                    record.append(float(p['price']))
            print(record)
            old_instant=instant
            data.append(record)
            datatot.append(record)
            count+=1
            
            
            
            
            
            
            
            
    columns=["TIME"]
    columns.extend(symbols)
    df = pd.DataFrame (data,columns = columns)
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")    
    print("SAVING FILE: DATA"+current_time+".csv")
    df.to_csv("DATA_"+current_time+".csv", index = False)