import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

start_date = "2023-07-15"
end_date = "2023-08-15"
frais = 99.5/100

btc_data = yf.download("BTC-USD", start=start_date, end=end_date, interval="1h")

#btc_data['Close'] = [40000-btc_data['Close'][_] for _ in btc_data.index]

btc_data['LogReturns'] = np.log(btc_data['Close'] / btc_data['Close'].shift(1))
btc_data['LogPrice'] = np.log(btc_data['Close'])
lreturns = btc_data['LogReturns']
close = btc_data['LogPrice']
ema_window = 1
btc_data['EMA_LogReturns'] = btc_data['LogReturns'].ewm(span=ema_window).mean()
#btc_data['EMA_LogReturns'] = btc_data['LogReturns']

'''
plt.figure(figsize=(12, 6))  
plt.plot(btc_data.index, lreturns, label='BTC-USD LogReturn', color='blue') 
plt.plot(btc_data.index, btc_data["EMA_LogReturns"], label='EMA', color='red') 
plt.title('Bitcoin (BTC) Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()  
plt.grid(True) 
#plt.show()  






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
#plt.show()'''


PHI = 0
PNL = [0]
trend = 0
openpos = btc_data['Close'][0]
i = 0
for signal in btc_data['EMA_LogReturns']:
    used = 0
    if trend == 1 and used ==0:
        if signal > -PHI/2:
            PNL.append(PNL[-1])
        if signal <= -PHI:
            trend = -1
            used = 1
            closepos = btc_data['Close'][i]
            PNL.append(PNL[-1] + frais*(closepos - openpos))
            openpos = closepos
        if signal <= -PHI/2 and signal > -PHI:
            trend = 0
            used = 1
            closepos = btc_data['Close'][i]
            PNL.append(PNL[-1] + frais*(closepos - openpos))
            
    if trend == -1 and used ==0:
        if signal < PHI/2:
            PNL.append(PNL[-1])
        if signal >= PHI:
            trend = 1
            used = 1
            closepos = btc_data['Close'][i]
            PNL.append(PNL[-1] + frais*(openpos - closepos))
            openpos = closepos
        if signal >= PHI/2 and signal < PHI:
            trend = 0
            used = 1
            closepos = btc_data['Close'][i]
            PNL.append(PNL[-1] + frais*(openpos - closepos))
            
    if trend == 0 and used ==0:
        if signal > PHI:
            trend = 1
            used = 1
            openpos = btc_data['Close'][i]
            PNL.append(PNL[-1])
            
        elif signal < -PHI:
            trend = -1
            used = 1
            openpos = btc_data['Close'][i]
            PNL.append(PNL[-1])
            
        else: 
            PNL.append(PNL[-1])
    i+=1
PNL.pop(-1)

# Create a grid of subplots
fig = plt.figure(figsize=(12, 10))
gs = fig.add_gridspec(3, 1, hspace=0.2)

# Subplot 1: Plot BTC-USD prices
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(btc_data.index, btc_data['Close'], label='BTC Close Price', color='blue')
ax1.set_ylabel('Price (USD)')
ax1.legend()
ax1.grid(True)

# Subplot 2: Plot 10-Day EMA of log returns
ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
ax2.plot(btc_data.index, btc_data['EMA_LogReturns'], label='10-Day EMA of Log Returns', color='orange')
ax2.set_ylabel('EMA')
ax2.legend()
ax2.grid(True)

# Subplot 3: Plot PNL data
ax3 = fig.add_subplot(gs[2, 0], sharex=ax1)

ax3.plot(btc_data.index, PNL, label='P&L', color='green')
ax3.set_xlabel('Date and Time')
ax3.set_ylabel('P&L')
ax3.legend()
ax3.grid(True)

# Set the title for the entire figure
plt.suptitle('Bitcoin (BTC) Price, 10-Day EMA of Log Returns, and P&L (Hourly)')
plt.xticks(rotation=45)
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust the position of the suptitle
plt.show()