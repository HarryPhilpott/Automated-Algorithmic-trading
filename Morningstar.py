import pandas as pd
import numpy as np
from time import gmtime, strftime
import csv

def EMA(period, close, ema):
    multiplier = (2/float(period + 1))
    emanew = ((close - ema) * multiplier) + ema
    return emanew

def signal(para,address):
    global date
    df = pd.read_csv(address)
    open = df.Open
    close = df.close
    high = df.High
    low = df.Low
    volume = df.Volume
    date = df.Date
    
    global neg_trades
    global num_trades
    neg_trades = 0
    num_trades = 0
    start = 0
    end = len(date)
    alt_open = open[start:end]
    alt_close = close[start:end]
    close_price = close[end-1]
    run_profit = 95000    
    Pri_Sma = 0
    Sec_Sma = 0
    signal_Sma = 0
    Hist_Sma = 0
    buy = 0
    sell = 0
    profit = 0
    j = 0
    k = 0
    l = 0
    buy_sell = 'No Trade'
    order = 2   #0=buy, 1=sell, 2=no position
    hist = []
    price_range = []
    signal = []
    Pri_Ema = []
    Sec_Ema = []
    macd = []


    for i in range(0, len(date)):
        price_range.append(abs(alt_open[i] - alt_close[i]))
        av_price_range = np.mean(price_range)

        if i < 12:
            Pri_Sma = Pri_Sma + alt_close[i]/float(12)

        if (i == 11):
            Pri_Ema.append(Pri_Sma)

        if i < 26:
            Sec_Sma = Sec_Sma + alt_close[i]/float(26)
            
        if (i > 11):
            Pri_Ema.append(EMA(12, alt_close[i], Pri_Ema[j]))
            j = j + 1

            if (i == 25):
                Sec_Ema.append(Sec_Sma)
                macd.append(Pri_Ema[j] - Sec_Ema[k])
                signal_Sma = signal_Sma + macd[k]/float(9)

            if (i > 25):
                Sec_Ema.append(EMA(26, alt_close[i], Sec_Ema[k]))
                k = k + 1
                macd.append(Pri_Ema[j] - Sec_Ema[k])
                
                if (i < 34):
                        signal_Sma = signal_Sma + macd[k]/float(9)

                if (i == 33):                                   
                    signal.append(signal_Sma)
                    hist.append(macd[k] - signal[l])
                    Hist_Sma = Hist_Sma + hist[l]/float(9)
                
                if (i > 33):    
                    signal.append(EMA(9, macd[k], signal[l]))
                    hist.append(macd[k] - signal[l])
                    l = l + 1
                    Hist_Sma = Hist_Sma + hist[l]/float(9)

                    if (i == 38):
                        hist_ema = EMA(5, hist[l], Hist_Sma)

                    if (i > 38):
                        hist_ema = EMA(5, hist[l], hist_ema)

                        if (alt_close[i] < alt_open[buy]*0.96 and order == 0):
                            profit = 5000*(alt_close[i] - alt_open[buy])/alt_open[buy] - 40
                            run_profit = run_profit + profit
                            num_trades = num_trades + 1
                            neg_trades = neg_trades + 1
                            buy = 0
                            sell = 0
                            order = 2
                            

                        if (alt_close[i] > alt_open[sell]*1.04 and order == 1):
                            profit = 5000*(alt_open[sell] - alt_close[i])/alt_close[sell] - 40
                            run_profit = run_profit + profit
                            num_trades = num_trades + 1
                            neg_trades = neg_trades + 1
                            buy = 0
                            sell = 0
                            order = 2


                        if (price_range[i] < (av_price_range*para[0]) and abs(hist[l]) > abs(hist_ema*para[1]) and hist[l] < 0 and order != 0):   #low
                            if i == len(date)-1:
                                buy_sell = 'Buy'
                            order = 0
                            buy = i + 1
                            
                            
                            
                            if (buy*sell != 0):
                                profit = 5000*(alt_open[sell] - alt_open[buy])/alt_open[buy] - 40
                                if profit < 0:
                                    neg_trades = neg_trades + 1
                                run_profit = run_profit + profit
                                num_trades = num_trades + 1
                                order = 2
                    
                        if (price_range[i] < (av_price_range*para[2]) and abs(hist[l]) > abs(hist_ema*para[3]) and hist[l] > 0 and order != 1):   #high
                            if i == len(date)-1:
                                buy_sell = 'Sell'
                            order = 1
                            sell = i + 1
                            

                            if(buy*sell !=0):
                                profit = 5000*(alt_open[sell] - alt_open[buy])/alt_open[buy] - 40
                                if profit < 0:
                                    neg_trades = neg_trades + 1
                                run_profit = run_profit + profit
                                num_trades = num_trades + 1
                                order = 2
                                
                                    
    return buy_sell, close_price

profit = 0
bloop = 0
quantity = 0
result = ''
header = ['Ticker', 'Order', 'Close']
para = [0.14,1.01,0.17,1.00]
df = pd.read_csv('list.csv')
output_file = 'C:\Users\Harry\Documents\Algo\output.csv'
ticker = df.Ticker

with open(output_file, 'wb') as output:
    writer = csv.writer(output, dialect='excel')
    writer.writerow(header)
    for i in range(0, len(df)):
        address = 'C:\Users\Harry\Documents\Algo\Tickers\_' + ticker[i] + '.csv'
        try:
            result, quantity = signal(para,address)
            if result == 'Sell' or result == 'Buy': 
                write_data = [ticker[i], result, quantity]
                writer.writerow(write_data)
        except:
            bloop = 5

##address = 'C:\Users\Harry\Documents\Algo\op3.csv'
##test = 0
##increase = signal(para, address)
##print 'Profit = ', increase, 'number of trades = ', num_trades
##increase = 0
##
##for i in range(0,101):
##    para[1] = 1.0 + i*0.01
##    print '   ', 1.0 + i*0.01, strftime("%H:%M:%S")
##    for i in range(0,6):
##        para[3] = 1.0 + i*0.01
##        test = signal(para, address)
##        if test > increase*0.9:
##            print 'profit = ', test, 'para[1] = ', para[1], 'para[3] = ', para[3], 'number of trades = ', num_trades
##            if test > increase:
##                increase = test
##            


