import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#pd.set_option("display.max_rows", None)
import talib as ta
import datetime as dt
import statistics as statistics
from dateutil.relativedelta import relativedelta
from colorama import init, Fore, Style
init()

assets = ['BTC']  # 'EURUSD', 'AUDUSD', 'BTCUSD', 'META'
trades = pd.DataFrame(columns = ['asset', 'entry time', 'exit time' ,'entry price','exit price','returns', 'position'])

def updateStructures(daily, date):      
      print('CURRENT DATE =', date)
      six_months_ago = date - relativedelta(months=6)
      print('six months ago = ', six_months_ago)

      daily = daily.loc[six_months_ago:date]
      print(daily)

      structures = {}

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
                
                threshold = 0.03 * min(value1, value2)
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
      
      
      return structures


def Trade(asset, position, entry_time, structures, limites, entry_area):
    print('TIEMPO DE ENTRADA == ',entry_time)
    print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'Position = ' + str(position), Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'ENTRY AREA = ' + str(entry_area), Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'LIMITES DE LA AREA = ' + str(limites), Style.RESET_ALL)

            
    hours = pd.read_csv(f'binance_hourly_prices/{asset}.csv')

    hours.index = hours['time']
    hours = hours.drop('time', axis=1)
    hours = hours.drop('Unnamed: 0', axis=1)
    hours = hours.drop('volume', axis=1)
    hours = hours.fillna(0)
      
    hours.index = pd.to_datetime(hours.index)
    hours = hours.drop_duplicates()

    entry_time = entry_time + dt.timedelta(hours=1)

    hours = hours.loc[entry_time:]
    print(hours)

    entry_time = hours.loc[entry_time].name
    print(Fore.LIGHTRED_EX  + 'ENTRY TIME = ' + str(entry_time) + Style.RESET_ALL)
    o = hours.loc[entry_time, 'open']
    print('open =', o)
    h = hours.loc[entry_time, 'high']
    print('high =', h)
    l = hours.loc[entry_time, 'low']
    print('low =', l)
    c = hours.loc[entry_time, 'close']
    print('close =', c)

    entry_price = o
    print('entry time = ', entry_time)
    print('entry price = ', entry_price)
    slippage_cost = entry_price * 0.001
    stop_loss = 0
    trailing_stop_threshold = 0
      
    if position == 'LONG':
            entry_price = entry_price + slippage_cost
            print('entry price after slippage =', entry_price)

            stop_loss = entry_area - (entry_area * 0.005)
            print('Inital stop loss =', stop_loss)

            trailing_stop_threshold = entry_price + entry_price * 0.02
            print('trailing stop threshold = ', trailing_stop_threshold)


    elif position == 'SHORT':
            entry_price = entry_price - slippage_cost
            print('entry price after slippage =', entry_price)

            stop_loss = entry_area + (entry_area * 0.005)
            print('Initial stop loss =', stop_loss)

            trailing_stop_threshold = entry_price - entry_price * 0.02
            print('trailing stop threshold = ', trailing_stop_threshold)


    close_to_area = False
    returns = 0

    hours = hours.loc[entry_time:entry_time + dt.timedelta(days=5)]
    print(hours)

 
    OPEN_POSITION = True
    trailing_stop = False
    
    boundaries = {}

    for i in hours.index:
            print(Fore.LIGHTGREEN_EX  + 'close to area = ' + str(close_to_area) + Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX  + 'OPEN POSITION = ' + str(OPEN_POSITION) + Style.RESET_ALL)

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

            threshold = 0.01

            print(Fore.LIGHTYELLOW_EX + 'ENTRY AREA = ' + str(entry_area), Style.RESET_ALL)
            distances = []
            for date, area in structures.items():
                  #print('----------------------------------------')
                  #print(date, ' = ' , area)
                  #print('Area = ', area[0])
                  distance = abs(entry_area - area[0])
                  if distance != 0:
                        distances.append(distance)
            
            print('distances =' , distances)
            print('closest area = ', min(distances))

            take_profit = entry_price + min(distances)
            print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)

            if position == 'LONG':
                take_profit = entry_price + min(distances) - ((entry_price + min(distances)) * threshold)
                print('Take profit = ', take_profit)

                print(Fore.LIGHTRED_EX + 'Position = ' + str(position), Style.RESET_ALL)
                pnl = entry_price - c
                
                if pnl < 0:
                        pnl = abs(pnl)
                        print(Fore.LIGHTGREEN_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([entry_price, c])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTGREEN_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        
                        if c >= trailing_stop_threshold and trailing_stop == False:
                              trailing_stop_threshold = c
                              trailing_stop = True
                              stop_loss = c - (c * 0.01)
                              print(Fore.LIGHTYELLOW_EX  + 'TRAILING STOP = ', str(trailing_stop) + Style.RESET_ALL)
                              print(Fore.LIGHTYELLOW_EX  + 'STOP LOSS AT = ', str(stop_loss) + Style.RESET_ALL)
                              continue
                        
                        elif c >= trailing_stop_threshold and trailing_stop == True:
                              trailing_stop_threshold = c
                              trailing_stop = True
                              stop_loss = c - (c * 0.01)
                              print(Fore.LIGHTYELLOW_EX  + 'TRAILING STOP = ', str(trailing_stop) + Style.RESET_ALL)
                              print(Fore.LIGHTYELLOW_EX  + 'STOP LOSS AT = ', str(stop_loss) + Style.RESET_ALL)
                              continue
                              
                        
                elif pnl > 0:
                        print(Fore.LIGHTRED_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([entry_price, c])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTRED_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)


                if (o >= take_profit or h >= take_profit or l >= take_profit or c >= take_profit):
                    returns = pd.Series([entry_price, take_profit])
                    returns = round(returns.pct_change()[1], 4)  
                    returns = returns - (returns * 0.0007)
                    print(Fore.LIGHTGREEN_EX  + 'TAKE PROFIT REACHED = ' + str(returns) + Style.RESET_ALL)

                    print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        
                    trades.loc[time] = {
                              'asset' : asset, 
                              'returns' : returns, 
                              'entry time': entry_time, 
                              'exit time' : time,
                              'entry price' : entry_price,
                              'exit price' : take_profit,
                              'position' : position
                              }
                        
                    print('Trades = ' , trades)
                    OPEN_POSITION = False
                    print(Fore.LIGHTYELLOW_EX  + 'OPEN POSITION = ' + str(OPEN_POSITION) + Style.RESET_ALL)

                    return entry_time, time
                
                if (o <= stop_loss or h <= stop_loss or l <= stop_loss or c <= stop_loss):
                    returns = pd.Series([entry_price, stop_loss])
                    returns = round(returns.pct_change()[1], 4)  
                    returns = returns - (returns * 0.0007)
                    print(Fore.LIGHTRED_EX  + 'STOP LOSS TRIGGERED = ' + str(returns) + Style.RESET_ALL)

                    print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        
                    trades.loc[time] = {
                              'asset' : asset, 
                              'returns' : returns, 
                              'entry time': entry_time, 
                              'exit time' : time,
                              'entry price' : entry_price,
                              'exit price' : stop_loss,
                              'position' : position
                              }
                        
                    print('Trades = ' , trades)
                    OPEN_POSITION = False
                    print(Fore.LIGHTYELLOW_EX  + 'OPEN POSITION = ' + str(OPEN_POSITION) + Style.RESET_ALL)

                    return entry_time, time
             



            if position == 'SHORT':
                take_profit = (entry_price - min(distances)) + ((entry_price - min(distances)) * threshold)
                print('Take profit = ', take_profit)

                print(Fore.LIGHTRED_EX + 'Position = ' + str(position), Style.RESET_ALL)
                pnl = entry_price - c
                trailing_stop_threshold = entry_price - entry_price * 0.05
                print('trailing stop threshold = ', trailing_stop_threshold)

                if pnl > 0:
                        pnl = abs(pnl)
                        print(Fore.LIGHTGREEN_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([c, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTGREEN_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        if c <= trailing_stop_threshold and trailing_stop == False:
                              trailing_stop_threshold = c
                              trailing_stop = True
                              stop_loss = c + (c * 0.01)
                              print(Fore.LIGHTYELLOW_EX  + 'TRAILING STOP = ', str(trailing_stop) + Style.RESET_ALL)
                              print(Fore.LIGHTYELLOW_EX  + 'STOP LOSS AT = ', str(stop_loss) + Style.RESET_ALL)
                              continue
                        
                        elif c <= trailing_stop_threshold and trailing_stop == True:
                              trailing_stop_threshold = c
                              trailing_stop = True
                              stop_loss = c + (c * 0.01)
                              print(Fore.LIGHTYELLOW_EX  + 'TRAILING STOP = ', str(trailing_stop) + Style.RESET_ALL)
                              print(Fore.LIGHTYELLOW_EX  + 'STOP LOSS AT = ', str(stop_loss) + Style.RESET_ALL) 
                              continue                  
                        
                elif pnl < 0:
                        print(Fore.LIGHTRED_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([c, entry_price])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTRED_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
  


                if (o <= take_profit or h <= take_profit or l <= take_profit or c <= take_profit):
                    returns = pd.Series([take_profit, entry_price])
                    returns = round(returns.pct_change()[1], 4)  
                    returns = returns - (returns * 0.0007)
                    print(Fore.LIGHTGREEN_EX  + 'TAKE PROFIT REACHED = ' + str(returns) + Style.RESET_ALL)

                    print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        
                    trades.loc[time] = {
                              'asset' : asset, 
                              'returns' : returns, 
                              'entry time': entry_time, 
                              'exit time' : time,
                              'entry price' : entry_price,
                              'exit price' : take_profit,
                              'position' : position
                              }
                        
                    print('Trades = ' , trades)
                    OPEN_POSITION = False
                    print(Fore.LIGHTYELLOW_EX  + 'OPEN POSITION = ' + str(OPEN_POSITION) + Style.RESET_ALL)

                    return entry_time, time
                
                if (o >= stop_loss or h >= stop_loss or l >= stop_loss or c >= stop_loss):
                    returns = pd.Series([stop_loss, entry_price])
                    returns = round(returns.pct_change()[1], 4)  
                    returns = returns - (returns * 0.0007)
                    print(Fore.LIGHTRED_EX  + 'STOP LOSS TRIGGERED = ' + str(returns) + Style.RESET_ALL)

                    print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        
                    trades.loc[time] = {
                              'asset' : asset, 
                              'returns' : returns, 
                              'entry time': entry_time, 
                              'exit time' : time,
                              'entry price' : entry_price,
                              'exit price' : stop_loss,
                              'position' : position
                              }
                        
                    print('Trades = ' , trades)
                    OPEN_POSITION = False
                    print(Fore.LIGHTYELLOW_EX  + 'OPEN POSITION = ' + str(OPEN_POSITION) + Style.RESET_ALL)

                    return entry_time, time
             

            res = input('Continue ?')
            if res == '':
                print('-------------------------------------------------')
                continue

            



    if position == 'SHORT':
            returns = pd.Series([hours['close'].iloc[-1], entry_price])
            returns = round(returns.pct_change()[1], 4)
            returns = returns - (returns * 0.0007)

            print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        

            trades.loc[time] = {
                                    'asset' : asset, 
                                    'returns' : returns, 
                                    'entry time': entry_time, 
                                    'exit time' : hours.iloc[-1].name,
                                    'entry price' : entry_price,
                                    'exit price' : hours['close'].iloc[-1],
                                    'position' : position
                                    }
            
                              
            print('Trades = ' , trades)
            return entry_time, hours.iloc[-1].name

    elif position == 'LONG':
            returns = pd.Series([entry_price, hours['close'].iloc[-1], ])
            returns = round(returns.pct_change()[1], 4)
            returns = returns - (returns * 0.0007)

            print(Fore.LIGHTYELLOW_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        

            trades.loc[time] = {
                                    'asset' : asset, 
                                    'returns' : returns, 
                                    'entry time': entry_time, 
                                    'exit time' : hours.iloc[-1].name,
                                    'entry price' : entry_price,
                                    'exit price' : hours['close'].iloc[-1],
                                    'position' : position
                                    }
            
                              
            print('Trades = ' , trades)
            return entry_time, hours.iloc[-1].name


  

            
            
            


def zoom1Hr(trend, structures, agent_date):
    print('*******************************************************************')
    print(Fore.LIGHTYELLOW_EX + '1 HRS ZOOM' + Style.RESET_ALL)
    print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)
    print('Trades so far = ' , trades)

    
      
    hours = pd.read_csv(f'binance_hourly_prices/{asset}.csv')

    hours.index = hours['time']
    hours = hours.drop('time', axis=1)
    hours = hours.drop('Unnamed: 0', axis=1)
    hours = hours.drop('volume', axis=1)
    hours = hours.fillna(0)
      
    hours.index = pd.to_datetime(hours.index)
    hours = hours.drop_duplicates()

    end_date = agent_date + dt.timedelta(days=1)

    hours = hours.loc[agent_date:end_date]
    print(hours)

    trade_open = False

  
    close_to_area = False
    returns = 0
    boundaries = {}

    long = False
    short = False

    exit_time = 0
    AREA = 0



    for i in hours.index:
            print(Fore.LIGHTGREEN_EX  + 'Close to area = ' + str(close_to_area) + Style.RESET_ALL)
            print('Boundaries = ', boundaries)
            print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)

            time = hours.loc[i].name
            print(Fore.LIGHTRED_EX  + 'HOUR = ' + str(time) + Style.RESET_ALL)
            o = hours.loc[i, 'open']
            print('open =', o)
            h = hours.loc[i, 'high']
            print('high =', h)
            l = hours.loc[i, 'low']
            print('low =', l)
            c = hours.loc[i, 'close']
            print('close =', c)

            exit_time = time

            current_candle = np.where(c > o, 'BULL', 'BEAR')
            print('Current candle =', current_candle)

            marubozu_threshold = 0.01
   
            marubozu = abs(o - c) > (c * marubozu_threshold)

            if marubozu == True:
                print(Fore.LIGHTYELLOW_EX + 'POSSIBLE MARUBOZU' + Style.RESET_ALL)


            threshold = 0.02
            for date, area in structures.items():
                  #print('----------------------------------------')
                  #print(date, ' = ' , area)
                  #print('Area = ', area[0])

                    upper_zone = area[0] + area[0] * threshold
                    lower_zone = area[0] - area[0] * threshold

                    if (c < upper_zone and c > lower_zone):

                        close_to_area = True
                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                        print('Boundaries = ', boundaries)
                        print(Fore.LIGHTRED_EX  + 'Close To Area = ' + str(close_to_area) + Style.RESET_ALL)
                        print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                        AREA = area[0]
                        print('AREA = ', area[0])
                        break
                  
                    else:
                        close_to_area = False
            


            if close_to_area == False and len(boundaries) != 0:
    
                if trend == 'BULL':
                        
                        if (
                            (c >= boundaries['upper zone']) and 
                            (c < (boundaries['upper zone'] + boundaries['upper zone'] * 0.03)) and                         
                            current_candle == 'BULL' and 
                            marubozu == True    
                            ):
                              
                              print(Fore.LIGHTGREEN_EX + '*LONG ENTRY*' + Style.RESET_ALL)
                              long = True

                              return long, exit_time, boundaries, AREA
                        
                        elif c < boundaries['lower zone']:
                              print(Fore.LIGHTRED_EX + '*PRICE WENT DOWN..*' + Style.RESET_ALL)

                        """
                        elif (
                            (c >= boundaries['upper zone']) and 
                            (c < (boundaries['upper zone'] + boundaries['upper zone'] * 0.03)) and                      
                            current_candle == 'BULL'
                            ):
                              
                              print(Fore.LIGHTGREEN_EX + '*LONG ENTRY*' + Style.RESET_ALL)
                              long = True

                              return long, exit_time, boundaries, AREA
                        """
                        
                    
     
                if trend == 'BEAR' :
                        if (
                            c <= boundaries['lower zone'] and
                            (c > (boundaries['lower zone'] - boundaries['lower zone'] * 0.03)) and 
                            current_candle == 'BEAR' and 
                            marubozu == True
                            ):
                              
                              print(Fore.LIGHTRED_EX + '*SHORT ENTRY*' + Style.RESET_ALL)
                              short = True
         

                              return short, exit_time, boundaries, AREA
                        
                        elif c > boundaries['upper zone']:
                              print(Fore.LIGHTRED_EX + '*PRICE WENT UP..*' + Style.RESET_ALL)

                        """
                        elif (
                            (c <= boundaries['lower zone']) and 
                            (c > (boundaries['lower zone'] - boundaries['lower zone'] * 0.03)) and            
                            current_candle == 'BEAR'
                            ):
                              
                              print(Fore.LIGHTRED_EX + '*SHORT ENTRY*' + Style.RESET_ALL)
                              short = True

                              return short, exit_time, boundaries, AREA
                        """
                        

                        
            res = input('Continue ?')
            if res == '':
                        print('-------------------------------------------------')
                        continue

            
            

                 
    if short == True:
        return short, exit_time, boundaries, AREA
      
    elif long == True:
        return long, exit_time, boundaries, AREA

    else:
        return False, exit_time, boundaries, AREA


def INTRADAY_ZOOM_1Hr(trend, structures, agent_date):
    print('*******************************************************************')
    print(Fore.LIGHTYELLOW_EX + 'INTRADAY 1 HRS ZOOM' + Style.RESET_ALL)
    print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)
    print('Trades so far = ' , trades)

    
      
    hours = pd.read_csv(f'binance_hourly_prices/{asset}.csv')

    hours.index = hours['time']
    hours = hours.drop('time', axis=1)
    hours = hours.drop('Unnamed: 0', axis=1)
    hours = hours.drop('volume', axis=1)
    hours = hours.fillna(0)
      
    hours.index = pd.to_datetime(hours.index)
    hours = hours.drop_duplicates()

    end_date = (agent_date + dt.timedelta(days=1)).replace(hour=19, minute=0, second=0)

    hours = hours.loc[agent_date:end_date]
    print(hours)

    trade_open = False

  
    close_to_area = False
    returns = 0
    boundaries = {}

    long = False
    short = False

    exit_time = 0
    confirmations = 0
    AREA = 0
    

    for i in hours.index:
            print(Fore.LIGHTGREEN_EX  + 'Close to area = ' + str(close_to_area) + Style.RESET_ALL)
            print('Boundaries = ', boundaries)
            print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)

            time = hours.loc[i].name
            print(Fore.LIGHTRED_EX  + 'HOUR = ' + str(time) + Style.RESET_ALL)
            o = hours.loc[i, 'open']
            print('open =', o)
            h = hours.loc[i, 'high']
            print('high =', h)
            l = hours.loc[i, 'low']
            print('low =', l)
            c = hours.loc[i, 'close']
            print('close =', c)

            exit_time = time

            current_candle = np.where(c > o, 'BULL', 'BEAR')
            print('Current candle =', current_candle)

            marubozu_threshold = 0.01
   
            marubozu = abs(o - c) > (c * marubozu_threshold)

            if marubozu == True:
                print(Fore.LIGHTYELLOW_EX + 'POSSIBLE MARUBOZU' + Style.RESET_ALL)


            threshold = 0.02
            for date, area in structures.items():
                  #print('----------------------------------------')
                  #print(date, ' = ' , area)
                  #print('Area = ', area[0])

                    upper_zone = area[0] + area[0] * threshold
                    lower_zone = area[0] - area[0] * threshold

                    if (c < upper_zone and c > lower_zone):

                        close_to_area = True
                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                        print('Boundaries = ', boundaries)
                        print(Fore.LIGHTRED_EX  + 'Close To Area = ' + str(close_to_area) + Style.RESET_ALL)
                        print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                        AREA = area[0]
                        print('AREA = ', area[0])
                        break
                  
                    else:
                        close_to_area = False
            


            if close_to_area == False and len(boundaries) != 0:
    
                if trend == 'BULL':
                        
                        if (
                            (c >= boundaries['upper zone']) and 
                            (c < (boundaries['upper zone'] + boundaries['upper zone'] * 0.03)) and                  
                            current_candle == 'BULL' and 
                            marubozu == True    
                            ):
                              
                              print(Fore.LIGHTGREEN_EX + '*LONG ENTRY*' + Style.RESET_ALL)
                              long = True

                              return long, exit_time, boundaries, AREA

                        elif c < boundaries['lower zone']:
                              print(Fore.LIGHTRED_EX + '*PRICE WENT DOWN..*' + Style.RESET_ALL)

                        """
                        elif (
                            (c >= boundaries['upper zone']) and 
                            (c < (boundaries['upper zone'] + boundaries['upper zone'] * 0.03)) and             
                            current_candle == 'BULL'
                            ):
                              
                              print(Fore.LIGHTGREEN_EX + '*LONG ENTRY*' + Style.RESET_ALL)
                              long = True

                              return long, exit_time, boundaries, AREA
                        """

                        
                        
     

                if trend == 'BEAR' :
                        if (
                            c <= boundaries['lower zone'] and
                            (c > (boundaries['lower zone'] - boundaries['lower zone'] * 0.03)) and 
                            current_candle == 'BEAR' and 
                            marubozu == True
                            ):
                              
                              print(Fore.LIGHTRED_EX + '*SHORT ENTRY*' + Style.RESET_ALL)
                              short = True
         

                              return short, exit_time, boundaries, AREA
                        
                        elif c > boundaries['upper zone']:
                              print(Fore.LIGHTRED_EX + '*PRICE WENT UP..*' + Style.RESET_ALL)

                        """
                        elif (
                            (c <= boundaries['lower zone']) and 
                            (c > (boundaries['lower zone'] - boundaries['lower zone'] * 0.03)) and          
                            current_candle == 'BEAR'
                            ):
                              
                              print(Fore.LIGHTRED_EX + '*SHORT ENTRY*' + Style.RESET_ALL)
                              short = True

                              return short, exit_time, boundaries, AREA
                        """
                        

                    
            res = input('Continue ?')
            if res == '':
                        print('-------------------------------------------------')
                        continue

            

                
            
             
    if short == True:
        return short, exit_time, boundaries, AREA
      
    elif long == True:
        return long, exit_time, boundaries, AREA

    else:
        return False, exit_time, boundaries, AREA



for asset in assets:
    print(asset)
    
    daily = pd.read_csv(f'DAILY_OHLC_BINANCE.csv')
    daily.index = daily['time']
    daily = daily.drop('time', axis=1)
    daily = daily.drop('Unnamed: 0', axis=1)
    daily = daily.drop('volume', axis=1)
    daily = daily.fillna(0)

    daily.index = pd.to_datetime(daily.index)

    start_date = dt.datetime(2019, 6, 1, 19, 0, 0)

    structures = {}

    position = False

    exit_time = start_date - dt.timedelta(days=1)

    close_to_area = False
    boundaries = {}
    
    take_profit = 0
    last_position = None
    zona = 0
    entry_area = 0

       
    for day in range(0, len(daily)):
        
        date = daily.iloc[day].name
        print(Fore.YELLOW + 'Date = ' + str(date) + Style.RESET_ALL)
        
        if date == dt.datetime(2023, 7, 20, 19, 0, 0):
            break

        if date >= dt.datetime(2023, 1, 1, 19, 0, 0):

            structures = updateStructures(daily, date)
            print('***********************************************************************************')
            print('***********************************************************************************')

            print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)

            print(Fore.YELLOW + 'Actual Date = ' + str(date) + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)

            
            n = 30
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
                  trend = 'BULL'
            
            elif prices_direction < 0:
                  trend = 'BEAR'
            
            print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)

            if trend == 'BULL' and date >= exit_time:
                  position, exit_time, boundaries, entry_area = zoom1Hr(trend, structures, date)
            
            elif trend == 'BEAR' and date >= exit_time:
                  position, exit_time, boundaries, entry_area = zoom1Hr(trend, structures, date)
            
            
            print(Fore.LIGHTYELLOW_EX + 'Position = ' + str(position), Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)

            
            if position == True:
                  if trend == 'BEAR':
                        entry_time, exit_time = Trade(asset, 'SHORT', exit_time, structures, boundaries, entry_area)
                        position = False

                  elif trend == 'BULL':
                        entry_time, exit_time = Trade(asset, 'LONG', exit_time, structures, boundaries, entry_area)
                        position = False

            print('Trades = ' , trades)
            print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(date) + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)

            if (
                  exit_time < exit_time.replace(hour=19, minute=0, second=0) or
                  (
                  (exit_time.replace(hour=19, minute=0, second=0)) < exit_time and 
                  (exit_time < (exit_time + dt.timedelta(days=1)).replace(hour=19, minute=0, second=0))
                  )
                  ): 

                  position, exit_time, boundaries, entry_area = INTRADAY_ZOOM_1Hr(trend, structures, exit_time)

                  if position == True:
                        if trend == 'BEAR':
                              entry_time, exit_time= Trade(asset, 'SHORT', exit_time, structures, boundaries, entry_area)
                              position = False

                        elif trend == 'BULL':
                              entry_time, exit_time= Trade(asset, 'LONG', exit_time, structures, boundaries, entry_area)
                              position = False

   
                  print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(date) + Style.RESET_ALL)
                  print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)


            
   
pd.set_option("display.max_rows", None)

        
strategy_returns = trades
print(strategy_returns)
wins = 0
losses = 0
for i in strategy_returns.values:
        if i[-2]>0:
            wins += 1
        elif i[-2]<0:
            losses += 1

print('wins =', wins)
print('losses =', losses)


strategy_returns['cumsum returns'] = strategy_returns['returns'].cumsum()
strategy_returns['cumulative returns'] = (1 + strategy_returns['returns']).cumprod()
print(strategy_returns)

compound_returns = (strategy_returns['returns']+1).cumprod()
print('compound returns = ', compound_returns)
total_returns = (compound_returns.iloc[-1]-1)*100
print('The total returns from strategy {:,.2f}% '.format(total_returns))
print('Max returns =', compound_returns.max())

running_max = np.maximum.accumulate(compound_returns).dropna()
running_max[running_max < 1] = 1
drawdown = (compound_returns)/running_max - 1
max_dd = drawdown.min()*100
print('The maximum drawdown is %.2f' % max_dd)


(strategy_returns['returns']+1).cumprod().plot(figsize=(10, 7))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()

strategy_returns['returns'].cumsum().plot(figsize=(10, 7))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()
