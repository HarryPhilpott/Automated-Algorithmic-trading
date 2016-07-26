from selenium import webdriver
import pandas as pd
import csv

df = pd.read_csv('list.csv')
ticker = df.Ticker

def get_data(ticker):
    print ticker

    address = 'https://uk.finance.yahoo.com/q/hp?s=' + ticker
    output_file = 'C:\Users\Harry\Documents\Algo\Tickers\_' + ticker + '.csv'
    browser.get(address)
    table = browser.find_element_by_class_name('yfnc_datamodoutline1').text
    
    data = table.split()
    
    data[6] = data[6] + data[7]
    length = len(data)
    
    for i in range(0, length-11):
        try:
            if (data[i] == 'Split'):
                
                data[i-6:len(data)] = data[i+1:len(data)-7]
                length = len(data)
        except:
             print'Stock split error'


    for i in range(0, length-11):
        try:
            if (data[i] == 'Dividend'):
                data[i-4:len(data)] = data[i+1:len(data)-5]
                length = len(data)
        except:
             print'Dividend error'
            
        
    for i in range(8,length-2,7):
        try:
            data[i] = data[i] + data[i+1] + data[i+2]
            for j in range(i+1, length-2):
                data[j] = data[j+2]
        except:
            print 'fuck'


    with open(output_file, 'wb') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(data[0:7])
        for i in range(456,7,-7):
            writer.writerow(data[i:i+7])

j = 0
browser = webdriver.Firefox()
for i in range(0, len(ticker)):
    try:
        get_data(ticker[i])
    except:
        print ticker[i], ' error'

    j = j + 1

    if j == 8:
        browser.close()
        browser = webdriver.Firefox()
        j = 0

browser.close()








