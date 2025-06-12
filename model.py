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
trades = pd.DataFrame(columns = ['asset', 'entry time', 'exit time' ,'entry price','exit price','returns', 'position'])



def Trade(asset, position, entry_time, structures, last_position, last_zone):    

    print('TIEMPO DE ENTRADA == ',entry_time)
    print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)

    
    boundaries = {}
    
    hours = pd.read_csv(f'binance_hourly_prices/{asset}.csv')

    hours.index = hours['time']
    hours = hours.drop('time', axis=1)
    hours = hours.drop('Unnamed: 0', axis=1)
    hours = hours.drop('volume', axis=1)
    hours = hours.fillna(0)
    
    hours.index = pd.to_datetime(hours.index)
    hours = hours.drop_duplicates()

    hours = hours.loc[entry_time:]
    print(hours)

    trade_open = False

    entry_price = 0
    close_to_area = False
    returns = 0
    zona = last_zone

    price_above_last_area = False

    
    for i in hours.index:
        print(Fore.LIGHTCYAN_EX + 'ZONE = ' + str(zona) +  Style.RESET_ALL)
        print(Fore.LIGHTCYAN_EX + 'LAST ZONE = ' + str(last_zone) +  Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX  + 'close to area = ' + str(close_to_area) + Style.RESET_ALL)

        time = hours.loc[i].name
        print(Fore.LIGHTRED_EX  + 'TIME = ' + str(time) + Style.RESET_ALL)
        o = hours.loc[i, 'open']
        print('open =', o)
        h = hours.loc[i, 'high']
        print('high =', h)
        l = hours.loc[i, 'low']
        print('low =', l)
        c = hours.loc[i, 'close']
        print('close =', c)

        threshold = 0.025

        for date, area in structures.items():
            #print('----------------------------------------')
            #print(date, ' = ' , area)
            #print('Area = ', area[0])
            upper_zone = area[0] + area[0] * threshold
            lower_zone = area[0] - area[0] * threshold
            
            if (c < upper_zone and c > lower_zone):

                close_to_area = True
                zona = area[0]
                boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                print('Boundaries = ', boundaries)
                print(Fore.LIGHTRED_EX  + 'close to area = ' + str(close_to_area) + Style.RESET_ALL)
                print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                print('AREA = ', area[0])
                break
            
            else:
                close_to_area = False
     
            


        if close_to_area == False:
            print(Fore.LIGHTGREEN_EX  + 'Price away from area = ' + str(c) + Style.RESET_ALL)
            if last_zone != 0:
                price_above_last_area = c > last_zone
                
            if position == 'SHORT' and price_above_last_area == False:
                print(Fore.LIGHTRED_EX + 'Position = ' + str(position), Style.RESET_ALL)

                if trade_open == False:
                    entry_price = statistics.mean([o, h, l, c])
                    print('entry time = ', time)
                    print('entry price = ', entry_price)
                    entry_time = time
                    

                    slippage_cost = entry_price * 0.001
                    entry_price = entry_price - slippage_cost
                    print('entry price =', entry_price)

                    print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)
                    trade_open = True
                    print(Fore.LIGHTGREEN_EX + 'Trade Open = ' + str(trade_open) + Style.RESET_ALL)


                else:
                    print('entry time = ', time)
                    print(Fore.LIGHTRED_EX + 'Time = ' + str(time) + Style.RESET_ALL)
                    print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)
                    pnl = entry_price - c

                    if pnl > 0:
                        pnl = abs(pnl)
                        print(Fore.LIGHTGREEN_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([c, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTGREEN_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
             
                    elif pnl < 0:
                        print(Fore.LIGHTRED_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([c, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTRED_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
            
            elif position == 'SHORT' and price_above_last_area == True and last_zone == zona:
                print(Fore.LIGHTRED_EX + 'Trade Not Open - PRICE ABOVE LAST ZONE AND POSITION WAS A SHORT..' + Style.RESET_ALL)
                return time, position, last_zone


            elif position == 'SHORT' and price_above_last_area == True and c < zona and last_zone != zona:
                print(Fore.LIGHTRED_EX + 'Position = ' + str(position), Style.RESET_ALL)
                if trade_open == False:
                    entry_price = statistics.mean([o, h, l, c])
                    print('entry time = ', time)
                    print('entry price = ', entry_price)
                    entry_time = time
                    

                    slippage_cost = entry_price * 0.001
                    entry_price = entry_price - slippage_cost
                    print('entry price =', entry_price)

                    print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)
                    trade_open = True
                    print(Fore.LIGHTGREEN_EX + 'Trade Open = ' + str(trade_open) + Style.RESET_ALL)


                else:
                    print('entry time = ', time)
                    print(Fore.LIGHTRED_EX + 'Time = ' + str(time) + Style.RESET_ALL)
                    print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)
                    pnl = entry_price - c

                    if pnl > 0:
                        pnl = abs(pnl)
                        print(Fore.LIGHTGREEN_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([c, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTGREEN_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
             
                    elif pnl < 0:
                        print(Fore.LIGHTRED_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([c, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTRED_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
            
                 
        
        elif close_to_area == True and trade_open == True:
            print(Fore.LIGHTRED_EX  + 'Price In Area = ' + str(c) + Style.RESET_ALL)
            returns = pd.Series([c, entry_price])
            returns = round(returns.pct_change()[1], 4)  
            print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
            
            trades.loc[time] = {
                     'asset' : asset, 
                     'returns' : returns, 
                     'entry time': entry_time, 
                     'exit time' : time,
                     'entry price' : entry_price,
                     'exit price' : c,
                     'position' : position
                     }
            print('Trades = ' , trades)
     
            return time, last_position, zona
                   
        res = input('Continue ?')
        if res == '':
            print('-------------------------------------------------')
            continue





        
for asset in assets:
    print(asset)
    
    daily = pd.read_csv(f'DAILY_OHLC_BINANCE.csv')
    daily.index = daily['time']
    daily = daily.drop('time', axis=1)
    daily = daily.drop('Unnamed: 0', axis=1)
    daily = daily.drop('volume', axis=1)
    daily = daily.fillna(0)

    daily.index = pd.to_datetime(daily.index)

    start_date = dt.datetime(2021, 10, 1, 19, 0, 0)

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


    for day in range(5, len(daily) - 5):
        print('***********************************************************************************')
        print('***********************************************************************************')
        
        date = daily.iloc[day].name
        print(Fore.YELLOW + 'Date = ' + str(date) + Style.RESET_ALL)

        past_5_open = daily['open'].iloc[day - 5]
        print('past 5 open =', past_5_open)

        past_5_high = daily['high'].iloc[day - 5]
        print('past 5 high =', past_5_high)

        past_5_low = daily['low'].iloc[day - 5]
        print('past 5 low =', past_5_low)

        past_5_close = daily['close'].iloc[day - 5]
        print('past 5 close =', past_5_close)
        print('-----------------------------')


        past_4_open = daily['open'].iloc[day - 4]
        print('past 4 open =', past_4_open)

        past_4_high = daily['high'].iloc[day - 4]
        print('past 4 high =', past_4_high)

        past_4_low = daily['low'].iloc[day - 4]
        print('past 4 low =', past_4_low)

        past_4_close = daily['close'].iloc[day - 4]
        print('past 4 close =', past_4_close)
        print('-----------------------------')
        
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

        future_4_open = daily['open'].iloc[day + 4]
        print('future 4 open = ' + str(future_4_open))

        future_4_high = daily['high'].iloc[day + 4]
        print('future 4 high = ' + str(future_4_high))

        future_4_low = daily['low'].iloc[day + 4]
        print('future 4 low = ' +  str(future_4_low))

        future_4_close = daily['close'].iloc[day + 4]
        print('future 5 close = '+ str(future_4_close))
        print('-----------------------------')

        future_5_open = daily['open'].iloc[day + 5]
        print('future 5 open = ' + str(future_5_open))

        future_5_high = daily['high'].iloc[day + 5]
        print('future 5 high = ' + str(future_5_high))

        future_5_low = daily['low'].iloc[day + 5]
        print('future 5 low = ' +  str(future_5_low))

        future_5_close = daily['close'].iloc[day + 5]
        print('future 5 close = '+ str(future_5_close))
        print('-----------------------------')


        print(Fore.YELLOW + 'Date = ' + str(date) + Style.RESET_ALL)
        
        agent_date = daily.iloc[day + 5].name

        if agent_date == dt.datetime(2023, 7, 1, 19, 0, 0):
             break

        print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
        
        current_price = future_5_close
        print('Current price =', current_price)

        current_candle = np.where(future_5_close > future_5_open, 'BULL', 'BEAR')
        print('Current candle =', current_candle)


        if (
            (abs(future_4_open - future_4_close) <= current_price * 0.15 and abs(future_4_open - future_4_close) >= current_price * 0.05) 
            or
            (abs(future_3_open - future_3_close) <= current_price * 0.15 and abs(future_3_open - future_3_close) >= current_price * 0.05) 
            or
            (abs(future_2_open - future_2_close) <= current_price * 0.15 and abs(future_2_open - future_2_close) >= current_price * 0.05) 
            or 
            (abs(past_3_open - past_3_close) <= current_price * 0.15 and abs(past_3_open - past_3_close) >= current_price * 0.05) 
            or
            (abs(past_2_open - past_2_close) <= current_price * 0.15 and abs(past_2_open - past_2_close) >= current_price * 0.05) 
            or
            (abs(past_4_open - past_4_close) <= current_price * 0.15 and abs(past_4_open - past_4_close) >= current_price * 0.05) 
            or
            (abs(past_5_open - past_5_close) <= current_price * 0.15 and abs(past_5_open - past_5_close) >= current_price * 0.05) 
            ):
            
            print(Fore.LIGHTYELLOW_EX + 'CANDLE SIZE ' + Style.RESET_ALL)

            ayer = (abs(future_4_open - future_4_close) <= current_price * 0.15 and abs(future_4_open - future_4_close) >= current_price * 0.05) 
            print('AYER = ', ayer)
            antier = (abs(future_3_open - future_3_close) <= current_price * 0.15 and abs(future_3_open - future_3_close) >= current_price * 0.05) 
            print('ANTIER = ', antier)
            tres_dias_atras = (abs(future_2_open - future_2_close) <= current_price * 0.15 and abs(future_2_open - future_2_close) >= current_price * 0.05) 
            print('3 DIAS ATRAS = ', tres_dias_atras)
            cuatro_dias_atras = (abs(future_open - future_close) <= current_price * 0.15 and abs(future_open - future_close) >= current_price * 0.05) 
            print('4 DIAS ATRAS = ', cuatro_dias_atras)
            cinco_dias_atras = (abs(today_open - today_close) <= current_price * 0.15 and abs(today_open - today_close) >= current_price * 0.05) 
            print('5 DIAS ATRAS = ', cinco_dias_atras)
            seis_dias_atras = (abs(past_open - past_close) <= current_price * 0.15 and abs(past_open - past_close) >= current_price * 0.05) 
            print('6 DIAS ATRAS = ', seis_dias_atras)
            siete_dias_atras = (abs(past_2_open - past_2_close) <= current_price * 0.15 and abs(past_2_open - past_2_close) >= current_price * 0.05) 
            print('7 DIAS ATRAS = ', siete_dias_atras)
            ocho_dias_atras = (abs(past_3_open - past_3_close) <= current_price * 0.15 and abs(past_3_open - past_3_close) >= current_price * 0.05) 
            print('8 DIAS ATRAS = ', ocho_dias_atras)
            nueve_dias_atras = (abs(past_4_open - past_4_close) <= current_price * 0.15 and abs(past_4_open - past_4_close) >= current_price * 0.05) 
            print('9 DIAS ATRAS = ', nueve_dias_atras)
            diez_dias_atras = (abs(past_5_open - past_5_close) <= current_price * 0.15 and abs(past_5_open - past_5_close) >= current_price * 0.05) 
            print('10 DIAS ATRAS = ', diez_dias_atras)

            max_price = {
                daily.iloc[day + 4].name : future_4_close,
                daily.iloc[day + 3].name : future_3_close,
                daily.iloc[day + 2].name : future_2_close,
                daily.iloc[day + 1].name : future_close,
                daily.iloc[day].name : today_close,
                daily.iloc[day - 1].name : past_close,
                daily.iloc[day - 2].name : past_2_close,
                daily.iloc[day - 3].name : past_3_close,
                daily.iloc[day - 4].name : past_4_close,
                daily.iloc[day - 5].name : past_5_close,
            }

            print(max_price)

            max_value = max(max_price.values())
            max_key = max(max_price, key=max_price.get)

            print(Fore.LIGHTGREEN_EX + 'MAX PRICE LAST 10 DAYS = ' + str(max_key), ' = ', str(max_value), Style.RESET_ALL)

            if (
                current_price <= (max_value - (max_value * 0.05)) 
                and
                current_price > past_5_close
                ):
                print(Fore.YELLOW + 'PRICE BELOW A MAX ' + Style.RESET_ALL)

                max_candle_type = np.where(daily.loc[max_key,'close'] > daily.loc[max_key,'open'], 'BULL', 'BEAR')
                print('MAX CANDLE TYPE = ', max_candle_type)

                if max_candle_type == 'BULL' and max_value not in structures:
                        structures[str(max_key)] = [daily.loc[max_key,'close']]
                        print(Fore.GREEN + 'Area = ' + str(daily.loc[max_key,'close']) + Style.RESET_ALL)

                elif max_candle_type == 'BEAR' and max_value not in structures:
                        structures[str(max_key)] = [daily.loc[max_key,'open']]
                        print(Fore.GREEN + 'Area = ' + str(daily.loc[max_key,'open']) + Style.RESET_ALL)
            
            min_price = {
                daily.iloc[day + 4].name : future_4_close,
                daily.iloc[day + 3].name : future_3_close,
                daily.iloc[day + 2].name : future_2_close,
                daily.iloc[day + 1].name : future_close,
                daily.iloc[day].name : today_close,
                daily.iloc[day - 1].name : past_close,
                daily.iloc[day - 2].name : past_2_close,
                daily.iloc[day - 3].name : past_3_close,
                daily.iloc[day - 4].name : past_4_close,
                daily.iloc[day - 5].name : past_5_close,
            }

            print(min_price)

            min_value = min(min_price.values())
            min_key = min(min_price, key=min_price.get)

            print(Fore.LIGHTRED_EX + 'MIN PRICE LAST 10 DAYS = ' + str(min_key) + ' = ' + str(min_value), Style.RESET_ALL)

            if ( 
                current_price >= (min_value + (min_value * 0.05)) and 
                current_price < past_5_close
                ):
                print(Fore.YELLOW + 'PRICE ABOVE A BOTTOM ' + Style.RESET_ALL)

                min_candle_type = np.where(daily.loc[min_key,'close'] > daily.loc[min_key,'open'], 'BULL', 'BEAR')
                print('MIN CANDLE TYPE = ', min_candle_type)

                if min_candle_type == 'BULL' and min_value not in structures:
                        structures[str(min_key)] = [daily.loc[min_key,'open']]
                        print(Fore.GREEN + 'Area = ' + str(daily.loc[min_key,'open']) + Style.RESET_ALL)

                elif min_candle_type == 'BEAR' and min_value not in structures:
                        structures[str(min_key)] = [daily.loc[min_key,'close']] 
                        print(Fore.GREEN + 'Area = ' + str(daily.loc[min_key,'close']) + Style.RESET_ALL)


        
        def is_close(value1, value2):
                if int(value1) == int(value2): 
                    return True
                
                threshold = 0.02 * min(value1, value2)
                return abs(value1 - value2) < threshold

        keys_to_drop = []
        LinkedPriceLevels = {}
        for key1, value1 in structures.items():
                for key2, value2 in structures.items():
                    if key1 != key2 and is_close(float(value1[0]), float(value2[0])):
                        if key1 in keys_to_drop or key2 in keys_to_drop:
                            continue
                        
                        else:
                            LinkedPriceLevels[key1 + ' - ' + key2] = [statistics.mean([value1[0], value2[0]])]
                            keys_to_drop.append(key1)
                            keys_to_drop.append(key2)

        if len(keys_to_drop) != 0:
                for key, value in LinkedPriceLevels.items():
                    structures[key] = value

                for i in keys_to_drop:
                    structures.pop(i)
        
        
        print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)


        if agent_date >= dt.datetime(2022, 3, 5, 19, 0, 0):
            n = 30
            prices = daily.loc[agent_date  - dt.timedelta(days=90):agent_date, 'close']
            std = prices.pct_change().rolling(window=n).std()
            average_std = std.rolling(window=n).mean()
            VF = std / average_std

            lookbacks = VF * 20
            lookbacks = lookbacks.fillna(0)

            todays_lookback = int(lookbacks[-1])
            print(Fore.LIGHTGREEN_EX + 'todays lookback = ', str(todays_lookback) + Style.RESET_ALL)

            prices = prices.loc[agent_date - dt.timedelta(days=todays_lookback - 1):agent_date]
            prices_direction = prices[-1] - prices[0]
            print('Lookback date = ' , prices.index[0])
            print('price direction =', prices_direction)

            if prices_direction  > 0:
                  position = 'LONG'
            
            elif prices_direction < 0:
                  position = 'SHORT'
            
            entry_time = prices.index[-1]
            

            if position == 'SHORT' and agent_date >= exit_time:

                exit_time, last_position, zona = Trade(asset,'SHORT', entry_time, structures, last_position, zona)
            
            elif position == 'LONG' and agent_date >= exit_time:

                exit_time, last_position, zona = Trade(asset,'LONG', entry_time, structures, last_position, zona)

            print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX + 'Last Position Was: = ' + str(last_position) + Style.RESET_ALL)
            print('ULTIMA ZONA DE CONTACTO = ', zona)


            res = input('Continue ?')
            if res == '':
                    close_to_area = False
                    print('-------------------------------------------------')
                    continue



    
