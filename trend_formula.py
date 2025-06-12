import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
#pd.set_option("display.max_rows", None)
import talib as ta
import datetime as dt
import statistics as statistics
from colorama import init, Fore, Style
init()

assets = ['BTC']  # 'EURUSD', 'AUDUSD', 'BTCUSD', 'META'
signals = pd.DataFrame(columns=['BTC'])


        
for asset in assets:
    print(asset)
    
    daily = pd.read_csv(f'DAILY_OHLC_BINANCE.csv')
    daily.index = daily['time']
    daily = daily.drop('time', axis=1)
    daily = daily.drop('Unnamed: 0', axis=1)
    daily = daily.drop('volume', axis=1)
    daily = daily.fillna(0)

    daily.index = pd.to_datetime(daily.index)

    start_date = dt.datetime(2019, 1, 1, 19, 0, 0)

    daily = daily.loc[start_date:]
    print('daily =', daily)

    structures = {}

    position = None

    exit_time = start_date - dt.timedelta(days=1)

    close_to_area = False
    boundaries = {}
    
    take_profit = 0
    last_position = None
    zona = 0


    for day in range(0, len(daily)):
        print('***********************************************************************************')
        print('***********************************************************************************')
        
        date = daily.iloc[day].name
        print(Fore.YELLOW + 'Date = ' + str(date) + Style.RESET_ALL)

    
        if date >= dt.datetime(2020, 1, 1, 19, 0, 0):
            n = 40
            prices = daily.loc[date  - dt.timedelta(days=90):date, 'close']
            std = prices.pct_change().rolling(window=n).std()
            average_std = std.rolling(window=n).mean()
            VF = std / average_std

            lookbacks = VF * 30
            lookbacks = lookbacks.fillna(0)

            todays_lookback = int(lookbacks[-1])
            print(Fore.LIGHTGREEN_EX + 'todays lookback = ', str(todays_lookback) + Style.RESET_ALL)

            prices = prices.loc[date - dt.timedelta(days=todays_lookback - 1):date]
            prices_direction = prices[-1] - prices[0]
            print('Lookback date = ' , prices.index[0])
            print('price direction =', prices_direction)

            if prices_direction  > 0:
                  signals.loc[date, asset] = 1
            
            elif prices_direction < 0:
                  signals.loc[date, asset] = -1
            
            
            
signals.to_csv('signals.csv')

    
