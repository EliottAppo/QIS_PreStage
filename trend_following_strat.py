import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

start_date = "2023-01-01"
end_date = "2023-06-30"

btc_data = yf.download("BTC-USD", start=start_date, end=end_date, interval="1h")

btc_data['LogReturns'] = np.log(btc_data['Close'] / btc_data['Close'].shift(1))
btc_data['LogPrice'] = np.log(btc_data['Close'])
lreturns = btc_data['LogReturns']
close = btc_data['LogPrice']
ema_window = 2
btc_data['EMA_LogReturns'] = btc_data['LogReturns'].rolling(window=ema_window).mean()


plt.figure(figsize=(12, 6))  
plt.plot(btc_data.index, lreturns, label='BTC-USD LogReturn', color='blue') 
plt.plot(btc_data.index, btc_data["EMA_LogReturns"], label='EMA', color='red') 
plt.title('Bitcoin (BTC) Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()  
plt.grid(True) 
#plt.show()  

def strat(phi, indicator):

    return 0




fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax1.plot(btc_data.index, btc_data['Close'], label='BTC-USD Close Price', color='blue')
ax1.set_ylabel('Price (USD)')
ax1.legend()
ax1.grid(True)

ax2.plot(btc_data.index, btc_data['EMA_LogReturns'], label='?-Day EMA of Log Returns', color='orange')
ax2.set_xlabel('Date and Time')
ax2.set_ylabel('EMA')
ax2.legend()
ax2.grid(True)

plt.suptitle('Bitcoin (BTC) Price and EMA of Log Returns (Hourly)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()