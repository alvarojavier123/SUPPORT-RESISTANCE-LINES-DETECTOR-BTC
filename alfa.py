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

assets = ['AMZN', 'EURUSD', 'AUDUSD', 'BTCUSD', 'META']
trades = pd.DataFrame(columns = ['asset', 'entry time', 'exit time' ,'returns', 'position'])

def Trade(asset, entry_time, position):

    if asset in ['AMZN', 'EURUSD', 'AUDUSD', 'META']:
        entry_time = pd.to_datetime(entry_time).to_numpy()
        entry_time = entry_time.astype('datetime64[D]')

        entry_time = pd.to_datetime(np.busday_offset(entry_time, 1))
        entry_time = entry_time.replace(hour=10, minute=0, second=0)
        print('Entry time =', entry_time)

    
    else:
        print('Entry time =', entry_time)
        entry_time = entry_time + dt.timedelta(hours=1)
        print('Entry time =', entry_time)
         

    M30 = pd.DataFrame(columns=['open', 'high', 'low', 'close'])

    data = pd.read_csv(f'MARKET_DATA/{asset}m_M30.csv')
    for i in data.values:
                data_values = i[0].split('\t')
                date = data_values[0] + ' ' + data_values[1]
                date = dt.datetime.strptime(date, "%Y.%m.%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                open = float(data_values[2])
                high = float(data_values[3])
                low = float(data_values[4])
                close = float(data_values[5])
                M30.loc[date] = {'open' : open, 'high' : high, 'low': low, 'close': close}


    M30.index = pd.to_datetime(M30.index)
    print(M30)

    print(M30.loc[entry_time])
    open = M30.loc[entry_time].open
    high = M30.loc[entry_time].high
    low = M30.loc[entry_time].low
    close = M30.loc[entry_time].close

    entry_price = statistics.mean([open, high, low, close])

    if position == 'LONG':
        print('entry price =', entry_price)
        slippage_cost = entry_price * 0.001
        entry_price = entry_price + slippage_cost
        print('entry price =', entry_price)

        take_profit = entry_price + (entry_price * 0.015)
        print(Fore.GREEN + 'Take profit =' + str(take_profit) + Style.RESET_ALL)
        
        stop_loss = entry_price - (entry_price * 0.015)
        print(Fore.RED + 'Stop loss =' + str(stop_loss) + Style.RESET_ALL)
        
    elif position == 'SHORT':
        print('entry price =', entry_price)
        slippage_cost = entry_price * 0.001
        entry_price = entry_price - slippage_cost
        print('entry price =', entry_price)

        take_profit = entry_price - (entry_price * 0.015)
        print(Fore.GREEN + 'Take profit =' + str(take_profit) + Style.RESET_ALL)

        stop_loss = entry_price + (entry_price * 0.015)
        print(Fore.RED + 'Stop loss =' + str(stop_loss) + Style.RESET_ALL)

    M30 = M30.loc[entry_time:]
    print(M30)

    for i in M30.index:
        print('time = ', M30.loc[i].name)
        time = M30.loc[i].name
        o = M30.loc[i, 'open']
        print('open =', o)
        h = M30.loc[i, 'high']
        print('high =', h)
        l = M30.loc[i, 'low']
        print('low =', l)
        c = M30.loc[i, 'close']
        print('close =', c)

        if position == 'LONG':
    
            if o >= take_profit or h >= take_profit or l >= take_profit or c >= take_profit:
                returns = pd.Series([entry_price, take_profit])
                returns = round(returns.pct_change()[1], 4) 
                print('Returns = ', returns) 
                returns = returns - (returns * 0.0007)
                print(Fore.LIGHTGREEN_EX + f'Profit at {str(time)} = ' + str(returns) + Style.RESET_ALL)
                trades.loc[time] = {
                     'asset' : asset, 
                     'returns' : returns, 
                     'entry time': entry_time, 
                     'exit time' : time,
                     'position' : position
                     }
                print('Trades = ' , trades)
                return time
                        
            elif o <= stop_loss or h <= stop_loss or l <= stop_loss or c <= stop_loss:
                returns = pd.Series([entry_price, stop_loss])
                returns = round(returns.pct_change()[1], 4)  
                print('Returns = ', returns)
                returns = returns - (returns * 0.0007)
                print(Fore.LIGHTRED_EX  + f'Loss at {str(time)} = ' + str(returns) + Style.RESET_ALL)
                trades.loc[time] = {
                     'asset' : asset, 
                     'returns' : returns, 
                     'entry time': entry_time, 
                     'exit time' : time,
                     'position' : position
                     }
                print('Trades = ' , trades)
                return time

            else:
                print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL )
        
        if position == 'SHORT':
            
            if o <= take_profit or h <= take_profit or l <= take_profit or c <= take_profit:
                returns = pd.Series([take_profit, entry_price])
                returns = round(returns.pct_change()[1], 4)  
                print('Returns = ', returns)
                returns = returns - (returns * 0.0007)
                print(Fore.LIGHTGREEN_EX + f'Profit at {str(time)} = ' + str(returns) + Style.RESET_ALL)
                trades.loc[time] = {
                     'asset' : asset, 
                     'returns' : returns, 
                     'entry time': entry_time, 
                     'exit time' : time,
                     'position' : position
                     }
                print('Trades = ' , trades)
                return time
            
            elif o >= stop_loss or h >= stop_loss or l >= stop_loss or c >= stop_loss:
                returns = pd.Series([stop_loss, entry_price])
                returns = round(returns.pct_change()[1], 4)  
                print('Returns = ', returns)
                returns = returns - (returns * 0.0007)
                print(Fore.LIGHTRED_EX  + f'Loss at {str(time)} = ' + str(returns) + Style.RESET_ALL)
                trades.loc[time] = {
                     'asset' : asset, 
                     'returns' : returns, 
                     'entry time': entry_time, 
                     'exit time' : time,
                     'position' : position
                     }
                print('Trades = ' , trades)
                return time
            
            else:
                print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)
                               
        """
        res = input('Continue ?')
        if res == '':
            print('-------------------------------------------------')
            continue
        """

     

for asset in assets:
    print(asset)
    daily = pd.DataFrame(columns=['open', 'high', 'low', 'close'])

    data = pd.read_csv(f'MARKET_DATA/{asset}m_Daily.csv')
    for i in data.values:

                data_values = i[0].split('\t')
                date = data_values[0]
                date = dt.datetime.strptime(data_values[0], "%Y.%m.%d").strftime("%Y-%m-%d")

                open = float(data_values[1])
                high = float(data_values[2])
                low = float(data_values[3])
                close = float(data_values[4])
                daily.loc[date] = {'open' : open, 'high' : high, 'low': low, 'close': close}

    daily.index = pd.to_datetime(daily.index)
    """"
    M30 = pd.DataFrame(columns=['open', 'high', 'low', 'close'])
    data = pd.read_csv(f'MARKET_DATA/{asset}m_M30.csv')
    for i in data.values:
                data_values = i[0].split('\t')
                date = data_values[0] + ' ' + data_values[1]
                date = dt.datetime.strptime(date, "%Y.%m.%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                open = float(data_values[2])
                high = float(data_values[3])
                low = float(data_values[4])
                close = float(data_values[5])
                M30.loc[date] = {'open' : open, 'high' : high, 'low': low, 'close': close}

    M30.index = pd.to_datetime(M30.index)
    print(M30)

    start_date = dt.datetime.strptime(str(M30.iloc[0].name), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    print(start_date)
    """
    start_date = dt.datetime(2021, 7, 16, 0, 0, 0)

    daily = daily.loc[start_date:]
    print('daily =', daily)

    structures = {}
    bottoms = {}
    tops = {}
    top_counter = 0
    confirmations = 0
    exit_time = 0
    tradeLock = False
    close_to_top = False
    close_to_bottom = False

    for day in range(3, len(daily) - 3):
        
        date = daily.iloc[day].name
        print(Fore.YELLOW + 'Date = ' + str(date) + Style.RESET_ALL)
        
        past_3_open = daily['open'].iloc[day - 3]
        print('past 3 open =', past_3_open)

        past_3_high = daily['high'].iloc[day - 3]
        print('past 3 high =', past_3_high)

        past_3_low = daily['low'].iloc[day - 3]
        print('past 3 low =', past_3_low)

        past_3_close = daily['close'].iloc[day - 3]
        print('past 3 close =', past_3_close)
        print('-----------------------------')

        past_2_open = daily['open'].iloc[day - 2]
        print('past 2 open =', past_2_open)

        past_2_high = daily['high'].iloc[day - 2]
        print('past 2 high =', past_2_high)

        past_2_low = daily['low'].iloc[day - 2]
        print('past 2 low =', past_2_low)

        past_2_close = daily['close'].iloc[day - 2]
        print('past 2 close =', past_2_close)
        print('-----------------------------')

        past_open = daily['open'].iloc[day - 1]
        print('past open =', past_open)

        past_high = daily['high'].iloc[day - 1]
        print('past high =', past_high)

        past_low = daily['low'].iloc[day - 1]
        print('past low =', past_low)

        past_close = daily['close'].iloc[day - 1]
        print('past close =', past_close)
        print('-----------------------------')
        
        today_open = daily['open'].iloc[day]
        print('open =', today_open)

        today_high = daily['high'].iloc[day]
        print('high =', today_high)

        today_low = daily['low'].iloc[day]
        print('low =', today_low)

        today_close = daily['close'].iloc[day]
        print('close =', today_close)
        print('-----------------------------')

        future_open = daily['open'].iloc[day + 1]
        print('future open =', future_open)

        future_high = daily['high'].iloc[day + 1]
        print('future high =', future_high)

        future_low = daily['low'].iloc[day + 1]
        print('future low =', future_low)

        future_close = daily['close'].iloc[day + 1]
        print('future close =', future_close)
        print('-----------------------------')

        future_2_open = daily['open'].iloc[day + 2]
        print('future 2 open =', future_2_open)

        future_2_high = daily['high'].iloc[day + 2]
        print('future 2 high =', future_2_high)

        future_2_low = daily['low'].iloc[day + 2]
        print('future 2 low =', future_2_low)

        future_2_close = daily['close'].iloc[day + 2]
        print('future 2 close =', future_2_close)
        print('-----------------------------')

        future_3_open = daily['open'].iloc[day + 3]
        print('future 3 open = ' + str(future_3_open))

        future_3_high = daily['high'].iloc[day + 3]
        print('future 3 high = ' + str(future_3_high))

        future_3_low = daily['low'].iloc[day + 3]
        print('future 3 low = ' +  str(future_3_low))

        future_3_close = daily['close'].iloc[day + 3]
        print('future 3 close = '+ str(future_3_close))
        print('-----------------------------')

        print(Fore.YELLOW + 'Date = ' + str(date) + Style.RESET_ALL)
        agent_date = daily.iloc[day + 3].name
        print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)

        current_price = future_3_close
        print('Current price =', current_price)

        current_candle = np.where(future_3_close > future_3_open, 'BULL', 'BEAR')
        print('Current candle =', current_candle)

        print(Fore.LIGHTCYAN_EX + 'Exit time = ' + str(exit_time), Style.RESET_ALL)

        if exit_time != 0:
            if exit_time > agent_date and close_to_top != True and close_to_bottom != True:
                tradeLock = True
                print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
            else:
                tradeLock = False
                print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
                 
        
        if (
            (future_3_close < today_close) and (today_close > past_3_close) and 
            (future_2_close < today_close) and (today_close > past_2_close) and 
            (future_close < today_close) and (today_close > past_close) and
            (future_3_close < future_close) and (past_3_close < past_close)
            ):

            print(Fore.RED + '***TOP***' + Style.RESET_ALL)
            print('Top at = ', date)
            candle_type = np.where(today_close > today_open, 'BULL', 'BEAR')
            print('Top candle type =', candle_type)

            if candle_type == 'BULL':
                    tops[str(date)] = today_close
                    print(Fore.RED + 'Top =' + str(today_close) + Style.RESET_ALL)

            elif candle_type == 'BEAR':
                    tops[str(date)] = today_open
                    print(Fore.RED + 'Top =' + str(today_open) + Style.RESET_ALL)
        
        elif (
              (today_close < future_3_close) and (today_close < past_3_close) and
              (today_close < future_2_close) and (today_close < past_2_close) and
              (today_close < future_close) and (today_close < past_close) and
              (future_3_close > future_close) and (past_3_close > past_close)
            ):

            print(Fore.GREEN + '***BOTTOM***' + Style.RESET_ALL)
            print('Bottom at = ', date)
            candle_type = np.where(today_close > today_open, 'BULL', 'BEAR')
            print('Top candle type =', candle_type)

            if candle_type == 'BULL':
                bottoms[str(date)] = today_open
                print(Fore.GREEN + 'Bottom = ' + str(today_open) + Style.RESET_ALL)

            elif candle_type == 'BEAR':
                bottoms[str(date)] = today_close
                print(Fore.GREEN + 'Bottom = ' + str(today_close) + Style.RESET_ALL)


        strength = 0.01
        
        print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)


        if len(tops) != 0:
            print('tops = ', tops)
            last_top = list(tops.values())[-1]
            print(Fore.RED + 'Top =', str(last_top) + Style.RESET_ALL)

            if len(tops) >= 2:
                print('Tops = ', tops)
                last_top_2 = list(tops.values())[-2]
                last_top = list(tops.values())[-1]
                print(Fore.GREEN + 'Last top =', str(last_top) + Style.RESET_ALL)
                print('More than 2 Tops')
                print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)

                if close_to_top == True:

                    if (
                        current_price >= last_top and 
                        abs(current_price - last_top) > current_price * strength
                        and current_candle == 'BULL' and tradeLock != True):

                        print('Price above top with strength')
                        if tradeLock == True:
                            tradeLock = False
                            print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
                        
                        for date, bottom in bottoms.items():
            
                                if bottom - abs(current_price - bottom) >= (bottom - (bottom * 0.02)) and current_price < bottom:
                                    print(date , ', BOTTOM = ' , bottom)
                                    print('Current price =', current_price)
                                    print('Price close to a bottom')
                                    close_to_bottom = True
                            
                        
                        print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
                        confirmations += 1
                        print('Confirmation = ', confirmations)
                        if confirmations >= 2:
                            print('LONG')
                            close_to_top = False
                            print('close to top = ', close_to_top)
                            entry_time = agent_date
                            exit_time = Trade(asset, entry_time, 'LONG')
                            confirmations = 0
                            continue

                    
                    elif (
                        current_price > last_top and 
                        abs(current_price - last_top) < current_price * strength
                        ):

                        print('Price above top with NO strength')
                        if tradeLock == True:
                            tradeLock = False
                            print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
                        
                        for date, bottom in bottoms.items():
            
                                if bottom - abs(current_price - bottom) >= (bottom - (bottom * 0.02)) and current_price < bottom:
                                    print(date , ', BOTTOM = ' , bottom)
                                    print('Current price =', current_price)
                                    print('Price close to a bottom')
                                    close_to_bottom = True
                             
                    
                        print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)

                                      

            else:
                if (
                    current_price > last_top and 
                    abs(current_price - last_top) > current_price * strength and 
                    current_candle == 'BULL' and tradeLock == False
                    ):

                    print('Price above top with strength')
                    confirmations += 1
                    print('Confirmation = ', confirmations)
                    if confirmations >= 2:
                        print('LONG')
                        entry_time = agent_date
                        exit_time = Trade(asset, entry_time, 'LONG')
                        confirmations = 0
                        tradeLock = True
                        continue
                        

                elif current_price > last_top and abs(current_price - last_top) < current_price * strength:
                    print('Price above top with NO strength')
                
                elif current_price < last_top:
                    print('Price below top')
            

        if len(bottoms) != 0:
        
            if len(bottoms) >= 2:


                last_bottom_2 = list(bottoms.values())[-2]
                last_bottom = list(bottoms.values())[-1]
                print(Fore.GREEN + 'Last bottom =', str(last_bottom) + Style.RESET_ALL)
                print('More than 2 Bottoms')
                print('Bottoms = ', bottoms)
                
                if abs(current_price - last_bottom) > abs(current_price - last_bottom_2):
                    print('Closest bottom = ', list(bottoms.values())[-2] , 'of date =', list(bottoms.keys())[-2])

                    if (
                        current_price >= last_bottom_2 and 
                        abs(current_price - last_bottom_2) > current_price * strength and close_to_top == False
                        and current_candle == 'BULL' and tradeLock != True):


                        tradeLock = False
                        print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
                        confirmations += 1
                        print('Price above bottom ' + str(last_bottom_2) + ' with strength')
                        print('confirmations = ', confirmations)

                    elif (
                        current_price >= last_bottom_2 and 
                        abs(current_price - last_bottom_2) < current_price * strength and close_to_top == False
                        ):
                        
                        tradeLock = False
                        print(Fore.LIGHTMAGENTA_EX + 'Trade Lock = ' +  str(tradeLock)  + Style.RESET_ALL)
                        
                        print('Price above bottom ' + str(last_bottom_2) + ' with  NO strength')
                        print('confirmations = ', confirmations)
                        

                        for date, top in tops.items():
        
                            if top - abs(current_price - top) >= (top - (top * 0.02)) and current_price < top:
                                print('Current price =', current_price)
                                print('Price close to a top')
                                print(date , ', TOP = ' , top)
                                close_to_top = True
                       
                 

            else:

                print('bottoms = ', bottoms)
                last_bottom = list(bottoms.values())[-1]
                print(Fore.GREEN + 'Last bottom =', str(last_bottom) + Style.RESET_ALL)

                if (
                    current_price > last_bottom and 
                    abs(current_price - last_bottom) > current_price * strength and
                    len(structures) < 2 
                    ):
                    
                    print('Price above last bottom with strength')
                
                elif (
                    current_price > last_bottom and 
                    abs(current_price - last_bottom) < current_price * strength and
                    len(structures) < 2 
                    ):
                    
                    print('Price above last bottom with NO strength')


                elif (
                    current_price < last_bottom and 
                    abs(last_bottom - current_price) > current_price * strength and 
                    current_candle == 'BEAR' and tradeLock == False and close_to_bottom == False
                    ):

                    print('Price below bottom with strength')
                    confirmations += 1
                    print('Confirmation = ', confirmations)
                    if confirmations >= 2:
                        print('SHORT')
                        entry_time = agent_date
                        exit_time = Trade(asset, entry_time, 'SHORT')
                        confirmations = 0
                        tradeLock = True
                        continue

                elif current_price < last_bottom and abs(last_bottom - current_price) < current_price * strength:
                    print('Price below bottom with NO strength')
                
                elif current_price < last_bottom:
                    print('Price below bottom')



        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')

        """
        res = input('Continue ?')
        if res == '':
            print('-------------------------------------------------')
            continue
        """


        

        
    

        
        
                   

    break
    print('-----------------------------------------------------------------------')