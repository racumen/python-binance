    # -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:56:09 2021

@author: f.romano
"""
from datetime import datetime
from math import floor
from binance.client import Client
import pandas as pd
import statistics 


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


variables=[
    ["seconds",1,30],
    ["minutes",60,10],
    ["15minutes",900,20],
    ["hours",3600,48],
    ["6hours",21600,12]
    ]

values=[]



n_minutes=0
sampls=0
for v in variables:
    n_minutes=n_minutes+v[1]*v[2]
    sampls=sampls+v[2]
    val=[]
    values.append(val)
    
n_minutes=10
values_seconds=[]
n_seconds=60
values_minutes=[]

for i in range(n_seconds+n_minutes*60):
    values_seconds.append(0)
for i in range(n_minutes):
    values_minutes.append(0)


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
            
            values_seconds.pop(-1)
            values_seconds.insert(0,record[1])
            
            
            for v in variables:
                if v[0]=="minutes":
                    for i in range(v[2]):
                        #print(i,n_seconds+60*i,n_seconds+60*(i+1))
                        #print(values_seconds[n_seconds+60*i:n_seconds+60*(i+1)])
                        values_minutes[i]=floor(statistics.mean(values_seconds[n_seconds+v[1]*i:n_seconds+v[1]*(i+1)]))
                    print("minutes",values_minutes)
               else: 
                    for i in range(v[2]):
                        #print(i,n_seconds+60*i,n_seconds+60*(i+1))
                        #print(values_seconds[n_seconds+60*i:n_seconds+60*(i+1)])
                        values_minutes[i]=floor(statistics.mean(values_seconds[n_seconds+v[1]*i:n_seconds+v[1]*(i+1)]))
                    print("minutes",values_minutes)
               e
            
            
            
            
            
            
            
    columns=["TIME"]
    columns.extend(symbols)
    df = pd.DataFrame (data,columns = columns)
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")    
    print("SAVING FILE: DATA"+current_time+".csv")
    df.to_csv("DATA_"+current_time+".csv", index = False)