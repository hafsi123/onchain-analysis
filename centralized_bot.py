import os
import math
import requests
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup
from decimal import Decimal

warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")


df = pd.read_csv('c:\\Users\\uber\\desktop\\onchain\\dataframe.csv')


print(df.head(5))
time.sleep(20)
    
# Nadarya variables
l = []
w = []
ws = 0
s = 0
for i in range(500):
  l=l+[i]
  gaus=[math.exp(-(math.pow(i,2)/(40.5)))]
  ws+=gaus[0]
  w=w+gaus

symbols = ["SOLUSDT", "GRTUSDT", "XRPUSDT", "1INCHUSDT", "FETUSDT","FLOKIUSDT"]

# Nadarya function
def onchain(df,symbol):
    links=df['networks'][df['name']==symbol]
    s=0
    for link in links :
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--disable-gpu') 
        options.add_argument('--no-sandbox')

        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(link)
            driver.implicitly_wait(5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            tbody = soup.find('tbody', class_='align-middle text-nowrap')
            td_elements = tbody.find_all('td')

            total_sum = sum(Decimal(td.get_text(strip=True).replace('$', '').replace(',', '')) for td in td_elements)
            s+=total_sum
        finally:
            driver.quit()
        return s

    
def nad(row, index,cdf):
    sum= 0
    j = 500
    for i in range(index-1 , index - 500, -1):
        j -= 1
        current=cdf.iloc[i]
        sum+=current['Close']*w[j]
    out = sum / ws
    sume1 = abs(row - out)
    mae = sume1 / (4.5 * 2.5)
    u = row + mae
    l = row - mae
    return float(u), float(l)

def binance(s):
    api_key='driaBQg3PSsqotcuKgC9WqeDTmOjp59eGKLOo88pGevkfNyer2Ig3eHMwaqJwMp9'
    symbol = s  

    # Binance API endpoint for historical K-line data
    api_url = 'https://api.binance.com/api/v3/klines'

    # Calculate the timestamp for the start time (current time - 500 hours)
    start_time = int((datetime.utcnow() - timedelta(hours=501)).timestamp()) * 1000

    params = {
        'symbol': symbol,
        'interval': '1h',  # Fetch data hourly
        'startTime': start_time,
        'limit': 502 # Number of candles
    }
    df_hourly = pd.DataFrame(columns=['Time', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Make the API request
    response = requests.get(api_url, params=params, headers={'X-MBX-APIKEY': api_key})

    if response.status_code == 200:
        data = response.json()

        # Process the data and append it to the df_hourly DataFrame
        for kline in data:
            open_time = datetime.utcfromtimestamp(kline[0] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            volume = float(kline[5])

            # Append the data to the DataFrame
            df_hourly = df_hourly.append({
                'Time': open_time,
                'Symbol': symbol,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume,
                'ema':None,
                'upper_band':None,
                'lower_band':None,
                'variation':None
            }, ignore_index=True)
        return df_hourly

        # Print the DataFrame or perform further operations

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None 



def get_binance_prices(df_hourly,s):
    api_key='driaBQg3PSsqotcuKgC9WqeDTmOjp59eGKLOo88pGevkfNyer2Ig3eHMwaqJwMp9'
    symbol = s  

    api_url = 'https://api.binance.com/api/v3/klines'

    start_time = int((datetime.utcnow() - timedelta(hours=0)).timestamp()) * 1000

    params = {
        'symbol': symbol,
        'interval': '1h',  # Fetch data hourly
        'startTime': start_time,
        'limit': 1  # Number of candles
    }

    response = requests.get(api_url, params=params, headers={'X-MBX-APIKEY': api_key})

    if response.status_code == 200:
        data = response.json()

        # Process the data and append it to the df_hourly DataFrame
        for kline in data:
            open_time = datetime.utcfromtimestamp(kline[0] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            volume = float(kline[5])

            # Append the data to the DataFrame
            df_hourly = df_hourly.append({
                'Time': open_time,
                'Symbol': symbol,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume,
                'ema':None,
                'upper_band':None,
                'lower_band':None
            }, ignore_index=True)
    else:
        print(f"Error {response.status_code}: {response.text}")


# Fetch current ticker price
def fetch_ticker_data(symbol):
    api_key = 'driaBQg3PSsqotcuKgC9WqeDTmOjp59eGKLOo88pGevkfNyer2Ig3eHMwaqJwMp9'
    symbol = symbol
    api_url = 'https://api.binance.com/api/v3/ticker/price'
    params = {'symbol': symbol}

    response = requests.get(api_url, params=params, headers={'X-MBX-APIKEY': api_key})

    if response.status_code == 200:
        data = response.json()
        current_price = float(data['price'])
        current_time = datetime.utcnow()
        return [current_time, current_price]
    else:
        return None

def emah(df,index):
    ema_value = df['High'].rolling(window=5, min_periods=1).mean().iloc[index]
    return float(ema_value)

trade=[]
in_trade=[]
dfl=[]
ema=[]
lower=[]
for i in range (len(symbols)):
    dfl.append(binance(symbols[i]))
    
i=0
for f in dfl :
    in_trade.append(False)
    f['ema']=None
    row=f.tail(1)
    x,y=nad(row['Close'],len(f)-1,f)
    lower.append(y)
    z=len(dfl[i])-1
    dfl[i]['lower_band'].iloc[z]=y
    dfl[i]['upper_band'].iloc[z]=x
    dfl[i]['ema'] = dfl[i]['High'].ewm(span=5, adjust=False).mean()
    ema.append(dfl[i]['ema'].iloc[-1])
    file_path = fr'C:\Users\uber\Desktop\hyper z\{symbols[i]}data.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
    dfl[i].to_csv(file_path, index=False)
    i+=1

last_time = dfl[0]['Time'].iloc[-1]
t = pd.to_datetime(last_time)
last_hour = t.hour
x =8
while True:
    i=0
    for symbol in symbols :
       
        data=fetch_ticker_data(symbol)
        
        if data[0].hour != last_hour:
            print(last_hour)
            print(data[0].hour-1)
            row=dfl[i].tail(1)
            o=row['Close']
            get_binance_prices(dfl[i],symbol)
            u,l=nad(o,len(dfl[i])-1,dfl[i])
            dfl[0].loc[dfl[0].index[-1], 'upper_band']=u
            dfl[0].loc[dfl[0].index[-1], 'lower_band']=l
            lower[i]=l
            upper[i]=y
            last_row_index = dfl[i].index[-1]
            ema[i] = emah(dfl[i],last_row_index)
            dfl[i].loc[last_row_index, 'ema'] = ema[i]
            file_path = fr'C:\Users\uber\Desktop\hyper z\{symbol}data.csv'
            if os.path.exists(file_path):
                os.remove(file_path)
            dfl[i].to_csv(file_path, index=False)
            print(symbol)
            print("hour added")
            if i==5:
                last_hour+=1
                
        
        v= float(data[1])>=upper[i] or float(data[1])>=ema[i]
        
        if (in_trade[i]==False) and (v==True)  :
            print("----------------------")
            print("trade entry")
            print(symbol)
            print(data[i])
            in_trade[i]=True
            entry_price=data[1]
            entry_index=len(dfl[i])-1
            entry_time =datetime.now()
            sl=entry_price*0.97
            tp=dfl[i]['ema'].iloc[-1]
            exit_price=None
            exit_time=None
            exit_index=None
            print("Entry Price:", entry_price)

            trade[i] = trade[i].append({
                'entry_price': entry_price,
                'entry_index': entry_index,
                'entry_time': entry_time,
                'sl': sl,
                'tp': tp,
                'exit_price': exit_price,
                'exit_time': exit_time,
                'exit_index': exit_index
                }, ignore_index=True)
        if (in_trade[i]==True) and (data[1]>=dfl[i]['ema'].iloc[-1] or data[1]<=trade[i]['sl'].iloc[-1]):
            in_trade[i]=False
            trade[i].loc[in_trade.index[-1], 'Exit_Price'] = data[1]
            trade[i].loc[in_trade.index[-1], 'Exit_Time'] = datetime.now()
            trade[i].loc[in_trade.index[-1], 'Exit_Index'] = len(dfl[i])-1
            file_path = fr'C:\Users\uber\Desktop\hyper z\{symbol}_trade.csv'
            if os.path.exists(file_path):
                os.remove(file_path)
            trade[i].to_csv(file_path, index=False)
        if x>0:
            print(v)
            print(data[1])
            print(lower[i])
            print(ema[i]) 
            print(in_trade[i])
            print(last_hour)
            print(data[0].hour)
            x-=1
        i+=1 
    time.sleep(20)
            
            
