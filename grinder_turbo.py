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
import sklearn
import numpy as np
from joblib import dump,load
from sklearn.ensemble import RandomForestRegressor
import grindfunc
import telegram

my_token = '1749392805:AAEq09tlCLSKMsTTdIAJx_fasgZ7iFfVPAA'
def send(msg, chat_id, token=my_token):
	"""
	Send a mensage to a telegram user specified on chatId
	chat_id must be a number!
	"""
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)


client = Client("4y2FAri1QZdyNWjO6BLp1FSiO0sXmQcEVKTKZwjfRpaklSbfX3wcLWd5Ikx8M6nw","sgwdst1CBgUDj9HHz74i9O5eJ0Zx2ATuMJUCMCiezC8EaD6xuO8mUyTs10krefXt")
numeri=[876572799]

old_instant=""
savesize=20


symbol1="BTC"
symbol2="BUSD"
         
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
 


klines = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
samples=[float(row[4]) for row in klines[-1:-n_samples-1:-1]]
print(samples[:3])
print(len(samples))

#df=pd.read_csv("GRINDER_SAMPLES.csv")
#df["VALUE"] = pd.to_numeric(df["VALUE"], downcast="float")
#samples=df["VALUE"].values.tolist()
#samples=[]

#values=list(range(n_values))


print("Variabili",n_values)
print("Giorni",grindfunc.twodec(n_samples/60/24))
print("Campioni da caricare",n_samples)
print("Campioni caricati",len(samples))

flag_start=False
minute_val=[]
old_avg=0
predu=[]
valu=[]





model='rf4.joblib'
rf = load(model) 
print("Caricato modello ",model)

capital=100000
invested=0
capit=[]
old_capital=capital
BTC=0
buybu=[]
buybuinst=[]
sellbu=[]
sellbuinst=[]
sellbureason=[]
vecchiu=[]
guadoz=[]
confirm=0
count=0
decrease=0
increase=0
prev_value=0
prev_gain=0
reason=""
vecchio=0
post_gain=-1
maxgain=0.5
old_val=0
data=[]

print("STARTING")
while(1):
    try:
        prices =  client.get_symbol_ticker(symbol="BTCBUSD")  
        #print(prices)
        current_val=prices["price"]
    except Exception as e: 
        print(e)
        current_val=old_val
                
        
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")    
    instant=int(current_time[-5:-3])
    minute_val.append(float(current_val))
    
    if instant!=old_instant:
        if len(minute_val):
            current_avg=sum(minute_val)/len(minute_val)
            minute_val=[]
        else:
            current_avg=old_avg
        old_instant=instant        
        
        if len(samples)==n_samples:
            samples.pop(-1)
            flag_start=True
        else:
            print("LOADING SAMPLES:",len(samples),"VS",n_samples)
            flag_start=False

        samples.insert(0,current_avg)
        
        
        if flag_start:
            grindfunc.calculate_values(samples, variables_definition,values)
            X=np.array([values])
            prediction = rf.predict(X)            
            
            action="NONE"
            if capital>0 and ((prediction[0]>1.6 and decrease<1 and post_gain<0) or prediction[0]>2.5):
                confirm+=1
                print(prediction[0],confirm)
                if confirm>1:
                    action="BUY"
                    BTC=capital/current_avg*(1-0.005)
                    msg=current_time+"\tBUY    P: "+str(prediction[0])+"\t"+str(int(current_avg))+"\tCapital\t"+str(int(capital))
                    old_capital=capital
                    capital=0
                    confirm=0
                    string1 = client.get_asset_balance(symbol1)
                    string2 = client.get_asset_balance(symbol2)
                    msg=msg+"\nPRE-BUY   \t"+symbol1+"\t"+string1["free"]+"\t"+symbol2+"\t"+string2["free"]
                    order = client.order_market_buy(symbol=symbol1+symbol2,quantity=0.001)
                    string1 = client.get_asset_balance(symbol1)
                    string2 = client.get_asset_balance(symbol2)
                    msg=msg+"\n"+"AFTER-BUY\t"+symbol1+"\t"+string1["free"]+"\t"+symbol2+"\t"+string2["free"]
                    print(msg)
                    for num in numeri:
                        send(msg,num)
            else:
                confirm=0
            
    
            flag_sell=False
    
            if current_avg<prev_value*0.999:
                decrease+=1
                #print("calina",decrease)
            else:
                decrease-=1
                if decrease<0:
                    decrease=0
            
            if current_avg>prev_value*1.001:
                increase+=1
                #print("calina",decrease)
            else:
                increase=0
                if increase<0:
                    increase=0
                
            gain=BTC*current_avg/old_capital
            
            if  BTC>0:
                reason=""
                if gain>maxgain:
                    maxgain=gain
                
                if  (prediction[0]< 0.5 and gain>1.01 and decrease>2 ):
                    flag_sell=True
                    reason=reason+"PREDICT "+str(grindfunc.twodec(gain))+str(decrease)
                    
                if  (gain>1.05 and decrease>3):
                    flag_sell=True
                    reason=reason+"5gain   "+str(grindfunc.twodec(gain))
        
                if gain<0.95:
                    flag_sell=True
                    reason=reason+"LOSS "+str(grindfunc.twodec(gain))
        
                if vecchio>240 and gain<0.97:
                    flag_sell=True
                    reason=reason+"VECCHIO "+str(grindfunc.twodec(gain))
        
                if vecchio>120 and gain>1.05 and(gain-1)<(maxgain-1)*0.4:
                    flag_sell=True
                    reason=reason+"DEGUADO "+str(grindfunc.twodec(gain))+" "+str(grindfunc.twodec(maxgain))
        
                    
                if decrease>3 and gain>1.0075:
                    flag_sell=True
                    reason=reason+"CALA "+str(grindfunc.twodec(gain))
                
                if decrease>20 and gain>1.02:
                    flag_sell=True
                    reason=reason+"CALETTA "+str(grindfunc.twodec(gain))
        
                if decrease>7 and gain>0.995:
                    flag_sell=True
                    reason=reason+"CALONA "+str(grindfunc.twodec(gain))
        
                    
                if flag_sell:
                    action="SELL"
                    post_gain=(gain-1)*3000
                    capital=BTC*current_avg
                    BTC=0
                    decrease=0
                    gain2=grindfunc.twodec(100*(capital-old_capital)/old_capital)
                    msg=current_time+"\tSELL\t"+reason+"\t"+str(round(current_avg))+"\tCapital\t"+str(round(capital))+"\t\t\t%\t"+str(round(gain2,2))+"\n"
                    reason=""
                    string1 = client.get_asset_balance(symbol1)
                    string2 = client.get_asset_balance(symbol2)
                    msg=msg+"PRE-SELL   \t"+symbol1+"\t"+string1["free"]+"\t"+symbol2+"\t"+string2["free"]
                    order = client.order_market_sell(symbol=symbol1+symbol2,quantity=0.001)
                    string1 = client.get_asset_balance(symbol1)
                    string2 = client.get_asset_balance(symbol2)
                    msg=msg+"\n"+"AFTER-SELL\t"+symbol1+"\t"+string1["free"]+"\t"+symbol2+"\t"+string2["free"]
                    print(msg)
                    for num in numeri:
                        send(msg,num)
            
            if BTC:
                vecchio=vecchio+1
            else:
                vecchio=0
            
            prev_gain=gain
            prev_value=current_avg
            post_gain=post_gain-1







            
            
            
            
            record=[current_time,round(current_avg),round(prediction[0],3),action,round(capital),round(BTC,5),round(gain,3),round(post_gain),confirm,increase,decrease,reason,vecchio]
            print(record)
            
            old_instant=instant
            data.append(record)
            count+=1
            if count>= savesize:
                columns=["TIME","VALUE","PREDICTION","ACTION","CAPITAL","BTC","GAIN","POST_GAIN","CONFIRM","INCREASE","DECREASE","REASON","VECCHIO"]
                df = pd.DataFrame (data,columns = columns)
                now = datetime.now()
                current_time = now.strftime("%Y_%m_%d_%H_%M_%S")    
                print("SAVING FILE: GRINDER_"+current_time+".csv")
                df.to_csv("GRINDER_"+current_time+".csv", index = False)
                count=0
                data=[]