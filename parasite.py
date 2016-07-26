from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import  strftime
import csv

def alter(string):
    mid_str = ''.join(string)
    out_string = str(mid_str[1:len(mid_str)])
    return out_string

def alter_date(string):
    init_str = ''.join(string)
    if init_str[0] == '0':
        mid_str = init_str[1:len(string)]
        mid_str = ''.join(mid_str)
        
        if mid_str[2] == '0':
            out_str = str(mid_str[0:2] + mid_str[3:len(mid_str)])
    else:
        mid_str = ''.join(init_str)
        
        if mid_str[3] == '0':
            out_str = str(mid_str[0:3] + mid_str[4:len(mid_str)])
    

    return out_str


#date = alter_date(strftime("%m/%d/%Y"))
date = '8/8/2014'
j = 0
order = []
stock = []
long = []
short = []
quantity = []

top_fiddy = 'C:\Users\Harry\Documents\Algo\da_bes.csv'
df = pd.read_csv(top_fiddy)
URLS = df.Address 

address = 'http://www.investopedia.com/simulator/Portfolio'
browser = webdriver.Firefox()
browser.get(address)

email = browser.find_element_by_id('edit-email')
password = browser.find_element_by_id('edit-password')
sign_in = browser.find_element_by_css_selector('a.ui-button.ui-button-a')

email.send_keys('harryphilpott1@gmail.com')
password.send_keys('123qweasdzxc123')
sign_in.click()
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'divPortfolioDetails')))
table = str(browser.find_element_by_id('divPortfolioDetails').text)

for i in range(0, len(table)):
    if table[i] == 'Sell':
        long.append(table[i+1])

    if table[i] == 'Cover':
        short.append(table[i+1])
        

for i in range(1, 2):
    j = j + 1
    browser.get(URLS[i])
    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'gvTradeHistory')))
        table = browser.find_element_by_id('gvTradeHistory').text
        table = table.split()
        print table[14]
        
        for i in range(0, len(table)): 
            if table[i] == date:   #14

                if table[i+4] == 'Short':
                    if table[i+9] == 'Open':
                        stock.append(table[i+9])
                        order.append('Short')
                        quantity.append(alter(table[i+11]))
                    else:
                        stock.append(table[i+8])
                        order.append('Short')
                        quantity.append(alter(table[i+10]))
                         

                if table[i+4] == 'Buy' and table[i+3] == 'Option':
                    if table[i+7] == 'Open':
                        stock.append(table[i+8])
                        quantity.append(alter(table[i+10]))
                        order.append('Buy')
                    else:
                        stock.append(table[i+7])
                        quantity.append(alter(table[i+9]))
                        order.append('Buy')
                                        

                if table[i+4] == 'Sell' and table[i+3] == 'Option':
                    if table[i+7] == 'Open':
                        stock.append(table[i+8])
                        quantity.append(alter(table[i+10]))
                        order.append('Sell')
                    else:
                        stock.append(table[i+7])
                        quantity.append(alter(table[i+9]))
                        order.append('Sell')
                                        

                if table[i+4] == 'Cover':
                    if table[i+9] == 'Open':
                        stock.append(table[i+10])
                        quantity.append(alter(table[i+12]))
                        order.append('Cover')
                    else:
                        stock.append(table[i+9])
                        quantity.append(alter(table[i+11]))
                        order.append('Cover')
                    


            if j == 3:
                browser.close()
                browser = webdriver.Firefox()
                browser.get(address)
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'edit-email')))
                email = browser.find_element_by_id('edit-email')
                password = browser.find_element_by_id('edit-password')
                sign_in = browser.find_element_by_css_selector('a.ui-button.ui-button-a')

                email.send_keys('harryphilpott1@gmail.com')
                password.send_keys('123qweasdzxc123')
                sign_in.click()
                j = 0
    except:
        print 'shitty data', i

browser.close()
output_file = 'C:\Users\Harry\Documents\Algo\output.csv'
print len(stock), len(order), len(quantity)

i = - 1

with open(output_file, 'a') as output:
    writer = csv.writer(output, dialect='excel')
    while i < len(stock):
        i = i + 1
        for j in range(0, len(long)):
            if stock[i] == long[j] and order[i] != 'Buy':
                stock[i:len(stock)] = stock[i+1:len(stock)]
                order[i:len(stock)] = order[i+1:len(stock)]
                quantity[i:len(stock)] = quantity[i+1:len(stock)]
                i = i - 1
        
            if stock[i] == short[j] and order[i] != 'Short':
                stock[i:len(stock)] = stock[i+1:len(stock)]
                order[i:len(stock)] = order[i+1:len(stock)]
                quantity[i:len(stock)] = quantity[i+1:len(stock)]
                i = i - 1

            if stock[i] != short[j] and order[i] != 'Cover':
                stock[i:len(stock)] = stock[i+1:len(stock)]
                order[i:len(stock)] = order[i+1:len(stock)]
                quantity[i:len(stock)] = quantity[i+1:len(stock)]
                i = i - 1

            if stock[i] != long[j] and order[i] != 'Sell':
                stock[i:len(stock)] = stock[i+1:len(stock)]
                order[i:len(stock)] = order[i+1:len(stock)]
                quantity[i:len(stock)] = quantity[i+1:len(stock)]
                i = i - 1
                

        write_data = [stock[i], order[i], quantity[i]]    
        writer.writerow(write_data)
        print stock[i], order[i], quantity[i]
    

