import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

'''start_date = "2023-07-15"
end_date = "2023-08-15"
frais = 99.5/100
PHI = 0
ema_window = 1'''

stock = "BTC-USD"
start_date = "2010-01-01"
end_date = "2023-02-01"
frais = 99.5/100

btc_data = yf.download(stock, start=start_date, end=end_date, interval="1d")

def strat(stock, start_date, end_date, PHI, PHI2, ema_window, frais):
    

    #btc_data = yf.download(stock, start=start_date, end=end_date, interval="1d")
    #btc_data['Close'] = [40000-btc_data['Close'][_] for _ in btc_data.index]
    btc_data['LogReturns'] = np.log(btc_data['Close'] / btc_data['Close'].shift(1))
    prix = btc_data['Close']
    btc_data['LogPrice'] = np.log(btc_data['Close'])
    lreturns = btc_data['LogReturns']
    close = btc_data['LogPrice']
    btc_data['EMA_LogReturns'] = btc_data['LogReturns'].ewm(span=ema_window).mean()
    #btc_data['EMA_LogReturns'] = btc_data['LogReturns']



    PNL = [0]
    trend = 0
    openpos = btc_data['Close'][0]
    i = 0
    for signal in btc_data['EMA_LogReturns']:
        used = 0
        if trend == 1 and used == 0:
            if signal > -PHI2:
                PNL.append(PNL[-1])
            if signal <= -PHI:
                trend = -1
                used = 1
                closepos = btc_data['Close'][i]
                PNL.append(PNL[-1] + frais*(closepos - openpos))
                openpos = closepos
            if signal <= -PHI2 and signal > -PHI:
                trend = 0
                used = 1
                closepos = btc_data['Close'][i]
                PNL.append(PNL[-1] + frais*(closepos - openpos))
                
        if trend == -1 and used ==0:
            if signal < PHI2:
                PNL.append(PNL[-1])
            if signal >= PHI:
                trend = 1
                used = 1
                closepos = btc_data['Close'][i]
                PNL.append(PNL[-1] + frais*(openpos - closepos))
                openpos = closepos
            if signal >= PHI2 and signal < PHI:
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
    PNL.pop(0)

    maxloss = np.min(PNL)
    vol = np.std(PNL)
    result = PNL[-1]
    resultrien = prix[-1] - prix[0]
    perf = np.abs(result/resultrien)

    
    # Create a grid of subplots
    fig = plt.figure(figsize=(12, 7))
    gs = fig.add_gridspec(3, 1, hspace=0.2)

    # Subplot 1: Plot BTC-USD prices
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(btc_data.index, btc_data['Close'], label='Stock Close Price', color='blue')
    ax1.set_ylabel('Price (USD)')
    ax1.legend()
    ax1.grid(True)

    # Subplot 2: Plot 10-Day EMA of log returns
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
    ax2.plot(btc_data.index, btc_data['EMA_LogReturns'], label='EMA of Log Returns', color='orange')
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
    plt.suptitle('Stock Price, EMA of Log Returns, and P&L (daily)')
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust the position of the suptitle
    print(maxloss, vol, result, perf)
    plt.show()
    
    return result



PHI = 1.7e-5
PHI2 = 0
ema = 91

strat(stock, start_date, end_date, PHI, PHI2, ema, frais)
max = 0
'''
for phi in range(0, 10000):
    for emaw in range(89, 94):
        
        phii = phi/100000000
        k = strat(stock, start_date, end_date, phii, PHI2, emaw, frais)
        if k > max:
            max = k
            
            print(max, phii, emaw)
'''


