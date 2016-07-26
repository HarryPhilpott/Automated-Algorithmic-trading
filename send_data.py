from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

d_list = 'C:\Users\Harry\Documents\Algo\output.csv'
df = pd.read_csv(d_list)
tickers = df.Ticker
order = df.Order
close = df.Close


address = 'http://www.investopedia.com/simulator/portfolio/'

browser = webdriver.Firefox()
browser.get(address)

email = browser.find_element_by_id('edit-email')
password = browser.find_element_by_id('edit-password')
sign_in = browser.find_element_by_css_selector('a.ui-button.ui-button-a')

email.send_keys('/////////')
password.send_keys('/////')
sign_in.click()

table = str(browser.find_element_by_id('divPortfolioDetails').text)
sell = browser.find_elements_by_link_text('Sell')
cover = browser.find_elements_by_link_text('Cover')
table = table.split()

long = []
short = []
long_quant = [] 
short_quant = []

for i in range(0, len(table)):
    if table[i] == 'Sell':
        long.append(table[i+1])

    if table[i] == 'Cover':
        short.append(table[i+1])
k = 0
i = 0
while i < len(cover):
    for j in range(0, len(tickers)):
        if short[i] == tickers[j]:
            k = k + 1
            cover = browser.find_elements_by_link_text('Cover')
            cover[i].click()
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "previewOrderButton")))
            preview = browser.find_element_by_id('previewOrderButton')
            preview.click()
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "submitOrder")))
            submit = browser.find_element_by_id('submitOrder')
            submit.click()
            browser.get(address)

            if k == 2:
                k = 0
                browser.close()
                browser = webdriver.Firefox()
                browser.get(address)
                email = browser.find_element_by_id('edit-email')
                password = browser.find_element_by_id('edit-password')
                sign_in = browser.find_element_by_css_selector('a.ui-button.ui-button-a')
                email.send_keys('harryphilpott1@gmail.com')
                password.send_keys('123qweasdzxc123')
                sign_in.click()

    i = i + 1

while i < len(sell):
    for j in range(0, len(tickers)):
        if long[i] == tickers[j]:
            k = k +1
            sell = browser.find_elements_by_link_text('Sell')
            cover = browser.find_elements_by_link_text('Cover')
            sell[i].click()
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "previewOrderButton")))
            preview = browser.find_element_by_id('previewOrderButton')
            preview.click()
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "submitOrder")))
            submit = browser.find_element_by_id('submitOrder')
            submit.click()
            browser.get(address)

            if k == 2:
                k = 0
                browser.close()
                browser = webdriver.Firefox()
                browser.get(address)
                email = browser.find_element_by_id('edit-email')
                password = browser.find_element_by_id('edit-password')
                sign_in = browser.find_element_by_css_selector('a.ui-button.ui-button-a')
                email.send_keys('harryphilpott1@gmail.com')
                password.send_keys('123qweasdzxc123')
                sign_in.click()
            
    i = i + 1

k = 0
            
address = 'http://www.investopedia.com/simulator/trade/tradestock.aspx'
browser.get(address)

for i in range(0, len(tickers)):
    k = k + 1
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'symbolTextbox')))
    stock_symbol = browser.find_element_by_id('symbolTextbox')
    transaction = Select(browser.find_element_by_id('transactionTypeDropDown'))
    quantity = browser.find_element_by_id('quantityTextbox')
    preview = browser.find_element_by_id('previewOrderButton')
    
    amount = str(int(5000/float(close[i])))
    quantity.send_keys(amount)
    stock_symbol.send_keys(tickers[i])
    
    if order[i] == 'Sell':
        transaction.select_by_visible_text('Sell Short')

    if order[i] == 'Buy':
        transaction.select_by_visible_text('Buy')
        
    preview.click()
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'submitOrder')))
    submit = browser.find_element_by_id('submitOrder')
    submit.click()
    browser.get(address)

    if k == 2:
        k = 0
        browser.close()
        browser = webdriver.Firefox()
        browser.get(address)
        email = browser.find_element_by_id('edit-email')
        password = browser.find_element_by_id('edit-password')
        sign_in = browser.find_element_by_css_selector('a.ui-button.ui-button-a')
        email.send_keys('harryphilpott1@gmail.com')
        password.send_keys('123qweasdzxc123')
        sign_in.click()

browser.close()


