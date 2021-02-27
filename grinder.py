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

columns=['SYMBOL','TIME','PRICE']


old_instant=0
dt=1
symbol="BTCBUSD"
savesize=3600


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
        
        for p in prices:
            if p['symbol']==symbol:
                prezzo=float(p['price'])
                prezzo=floor(prezzo*0.996)
                now = datetime.now()
                current_time = now.strftime("%Y_%m_%d__%H_%M_%S")    
                instant=int(current_time[-2:])
                if (instant-old_instant>=dt or (instant-old_instant<0 and instant-old_instant+60>=dt )):
                    print(symbol,'\t', current_time,'\t',prezzo)
                    old_instant=instant
                    data.append([symbol,current_time,prezzo])
                    count+=1
                    
    df = pd.DataFrame (data,columns = columns)
    print("SAVING FILE: DATA"+current_time+".csv")
    df.to_csv("DATA"+current_time+".csv", index = False)