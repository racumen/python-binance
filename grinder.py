    # -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:56:09 2021

@author: f.romano
"""
from datetime import datetime
from math import floor
from binance.client import Client
import pandas as pd

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
    ["seconds",1,300],
    ["minutes",60,300],
    ["15minutes",900,20],
    ["hours",3600,48],
    ["6hours",21600,12]
    ]

values=[]



secs=0
sampls=0
for v in variables:
    secs=secs+v[1]*v[2]
    sampls=sampls+v[2]
    val=[]
    values.append(val)



print(secs/3600/24,sampls)

dedede
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
            average
            count+=1
            
            val[0].pop(0)
            
            
            
    columns=["TIME"]
    columns.extend(symbols)
    df = pd.DataFrame (data,columns = columns)
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")    
    print("SAVING FILE: DATA"+current_time+".csv")
    df.to_csv("DATA_"+current_time+".csv", index = False)