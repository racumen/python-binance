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
symbols=["BTCBUSD","ETHBUSD","ADABUSD","IOTABUSD","LTCBUSD","ZECBUSD","BCHBUSD"]
savesize=3600


stats=[['minute']]


time_res = client.get_server_time()
info = client.get_exchange_info()
prices = client.get_all_tickers()
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
                    record.append(p['price'])
            print(record)
            old_instant=instant
            data.append(record)
            count+=1
            
    columns=["TIME"]
    columns.extend(symbols)
    df = pd.DataFrame (data,columns = columns)
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")    
    print("SAVING FILE: DATA"+current_time+".csv")
    df.to_csv("DATA_"+current_time+".csv", index = False)