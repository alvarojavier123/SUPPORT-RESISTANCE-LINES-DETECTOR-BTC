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



def Trade(asset, position, entry_time, structures):    

      print('TIEMPO DE ENTRADA == ',entry_time)
      print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)
      print(Fore.LIGHTYELLOW_EX + 'Position = ' + str(position), Style.RESET_ALL)

            
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

      entry_price = statistics.mean([o, h, l, c])
      print('entry time = ', entry_time)
      print('entry price = ', entry_price)
      slippage_cost = entry_price * 0.001
      entry_price = entry_price - slippage_cost
      print('entry price after slippage =', entry_price)

      close_to_area = False
      returns = 0

      hours = hours.loc[entry_time + dt.timedelta(hours=1):entry_time + dt.timedelta(days=3)]
      print(hours)

      AREA = 0

      for i in hours.index:
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


            if position == 'SHORT' and close_to_area == False:
                  print(Fore.LIGHTRED_EX + 'Position = ' + str(position), Style.RESET_ALL)
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
            
            elif position == 'LONG' and close_to_area == False:
                  print(Fore.LIGHTRED_EX + 'Position = ' + str(position), Style.RESET_ALL)
                  pnl = entry_price - c

                  if pnl < 0:
                        pnl = abs(pnl)
                        print(Fore.LIGHTGREEN_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([entry_price, c])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTGREEN_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)
                        
                  elif pnl > 0:
                        print(Fore.LIGHTRED_EX  + 'PNL = ', str(pnl) + Style.RESET_ALL)
                        returns = pd.Series([entry_price, c])
                        returns = round(returns.pct_change()[1], 4)  
                        print(Fore.LIGHTRED_EX  + 'Returns = ', str(returns) + Style.RESET_ALL)




            threshold = 0.005

            for date, area in structures.items():
                  #print('----------------------------------------')
                  #print(date, ' = ' , area)
                  #print('Area = ', area[0])

                if len(area) == 1:
                    upper_zone = area[0] + area[0] * threshold
                    lower_zone = area[0] - area[0] * threshold

                    if (c < upper_zone and c > lower_zone):

                        close_to_area = True
                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                        print('Boundaries = ', boundaries)
                        print(Fore.LIGHTRED_EX  + 'Close To Area = ' + str(close_to_area) + Style.RESET_ALL)
                        print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                        print('AREA = ', area[0])
                        break
                  
                else:
                    close_to_area = False

                
                if len(area) > 1:
         
                    upper_zone = max(area) + max(area) * threshold
                    lower_zone = min(area) - min(area) * threshold
            
                    if (c < upper_zone and c > lower_zone):

                        close_to_area = True
                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                        print('Boundaries = ', boundaries)
                        print(Fore.LIGHTRED_EX  + 'Close To Area = ' + str(close_to_area) + Style.RESET_ALL)
                        print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                        print('AREA = ', area)
                        break

                else:
                    close_to_area = False
                  

            print(Fore.LIGHTGREEN_EX + 'Trading..' + Style.RESET_ALL)


            if close_to_area == True:
                  if position == 'SHORT':
                        print(Fore.LIGHTRED_EX  + 'Price Close To Area' + Style.RESET_ALL)
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
                        return time, AREA
                  
                  elif position == 'LONG':
                        print(Fore.LIGHTRED_EX  + 'Price Close To Area' + Style.RESET_ALL)
                        returns = pd.Series([entry_price, c])
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
                        return time, AREA


                       
            res = input('Continue ?')
            if res == '':
                  print('-------------------------------------------------')
                  continue

      
      if position == 'SHORT':
            returns = pd.Series([hours['close'].iloc[-1], entry_price])
            returns = round(returns.pct_change()[1], 4)  
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
            return hours.iloc[-1].name, AREA

      elif position == 'LONG':
            returns = pd.Series([entry_price, hours['close'].iloc[-1], ])
            returns = round(returns.pct_change()[1], 4)  
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
            return hours.iloc[-1].name, AREA




def zoom1Hr(trend, structures, agent_date):
    print('*******************************************************************')
    print(Fore.LIGHTYELLOW_EX + '1 HRS ZOOM' + Style.RESET_ALL)
    print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)

    
      
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
    


    for i in hours.index:
            print(Fore.LIGHTGREEN_EX  + 'Close to area = ' + str(close_to_area) + Style.RESET_ALL)
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


            if close_to_area == True:
                  if trend == 'BEAR':
                        print(Fore.LIGHTRED_EX + '*CHECK FOR SHORT ENTRIES OR CLOSE OPEN SHORT*' + Style.RESET_ALL)
                        print('Boundaries = ', boundaries)
                        if c < boundaries['lower zone']:
                              print(Fore.LIGHTRED_EX + '*SHORT ENTRY*' + Style.RESET_ALL)
                              close_to_area = False
                              short = True
                              return short, exit_time
                        
                        elif c > boundaries['upper zone']:
                              print(Fore.LIGHTRED_EX + '*PRICE WENT UP..*' + Style.RESET_ALL)
                              close_to_area = False
                   
                  
                  elif trend == 'BULL':
                        print(Fore.LIGHTGREEN_EX + '*CHECK FOR LONG ENTRIES OR CLOSE OPEN LONG*' + Style.RESET_ALL)
                        print('Boundaries = ', boundaries)
                        if c > boundaries['upper zone']:
                              print(Fore.LIGHTGREEN_EX + '*LONG ENTRY*' + Style.RESET_ALL)
                              close_to_area = False
                              long = True
                              return long, exit_time
                        
                        elif c < boundaries['lower zone']:
                              print(Fore.LIGHTRED_EX + '*PRICE WENT DOWN..*' + Style.RESET_ALL)
                              close_to_area = False


            threshold = 0.015
            for date, area in structures.items():
                  #print('----------------------------------------')
                  #print(date, ' = ' , area)
                  #print('Area = ', area[0])

                if len(area) == 1:
                    upper_zone = area[0] + area[0] * threshold
                    lower_zone = area[0] - area[0] * threshold

                    if (c < upper_zone and c > lower_zone):

                        close_to_area = True
                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                        print('Boundaries = ', boundaries)
                        print(Fore.LIGHTRED_EX  + 'Close To Area = ' + str(close_to_area) + Style.RESET_ALL)
                        print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                        print('AREA = ', area[0])
                        break
                  
                else:
                    close_to_area = False

                
                if len(area) > 1:
         
                    upper_zone = max(area) + max(area) * threshold
                    lower_zone = min(area) - min(area) * threshold
            
                    if (c < upper_zone and c > lower_zone):

                        close_to_area = True
                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                        print('Boundaries = ', boundaries)
                        print(Fore.LIGHTRED_EX  + 'Close To Area = ' + str(close_to_area) + Style.RESET_ALL)
                        print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(c) + Style.RESET_ALL)
                        print('AREA = ', area)
                        break

                else:
                    close_to_area = False
            


            res = input('Continue ?')
            if res == '':
                    print('-------------------------------------------------')
                    continue
    

    if short == True:
        return short, exit_time
      
    elif long == True:
        return long, exit_time

    else:
        return False, exit_time

 

for asset in assets:
    print(asset)
    
    daily = pd.read_csv(f'DAILY_OHLC_BINANCE.csv')
    daily.index = daily['time']
    daily = daily.drop('time', axis=1)
    daily = daily.drop('Unnamed: 0', axis=1)
    daily = daily.drop('volume', axis=1)
    daily = daily.fillna(0)

    daily.index = pd.to_datetime(daily.index)


    start_date = dt.datetime(2021, 5, 1, 0, 0, 0)

    daily = daily.loc[start_date:]
    print('daily =', daily)

    structures = {}

    position = None

    exit_time = start_date - dt.timedelta(days=1)

    close_to_area = False
    boundaries = {}
    
    take_profit = 0
    last_area = 0


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
        print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)
        
        current_price = future_3_close
        print('Current price =', current_price)

        current_candle = np.where(future_3_close > future_3_open, 'BULL', 'BEAR')
        print('Current candle =', current_candle)



        if (
            (future_3_close < today_close) and (today_close > past_3_close) and 
            (future_2_close < today_close) and (today_close > past_2_close) and 
            (future_close < today_close) and (today_close > past_close) and
            (future_3_close < future_close) and (past_3_close < past_close)
            ):

            print(Fore.GREEN + '***AREA***' + Style.RESET_ALL)
            print('Crucial Area at = ', date)
            candle_type = np.where(today_close > today_open, 'BULL', 'BEAR')
            print('Crucial candle type =', candle_type)

            if candle_type == 'BULL':
                    structures[str(date)] = [today_close]
                    print(Fore.GREEN + 'Area = ' + str(today_close) + Style.RESET_ALL)

            elif candle_type == 'BEAR':
                    structures[str(date)] = [today_open]
                    print(Fore.GREEN + 'Area = ' + str(today_open) + Style.RESET_ALL)


        elif (
              (today_close < future_3_close) and (today_close < past_3_close) and
              (today_close < future_2_close) and (today_close < past_2_close) and
              (today_close < future_close) and (today_close < past_close) and
              (future_3_close > future_close) and (past_3_close > past_close)
            ):

            print(Fore.GREEN + '***AREA***' + Style.RESET_ALL)
            print('Crucial Area at = ', date)
            candle_type = np.where(today_close > today_open, 'BULL', 'BEAR')
            print('Crucial candle type =', candle_type)

            if candle_type == 'BULL':
                structures[str(date)] = [today_open]
                print(Fore.GREEN + 'Area = ' + str(today_open) + Style.RESET_ALL)

            elif candle_type == 'BEAR':
                structures[str(date)] = [today_close]
                print(Fore.GREEN + 'Area = ' + str(today_close) + Style.RESET_ALL)

        
        def is_close(value1, value2):
                threshold = 0.01 * min(value1, value2)
                return abs(value1 - value2) < threshold


        keys_to_drop = []
        LinkedPriceLevels = {}
        for key1, value1 in structures.items():
                for key2, value2 in structures.items():
                    if key1 != key2 and is_close(value1[0], value2[0]):
                        if key1 in keys_to_drop or key2 in keys_to_drop:
                            continue
                        
                        else:
                            LinkedPriceLevels[key1 + ' - ' + key2] = [value1[0], value2[0]]
                            keys_to_drop.append(key1)
                            keys_to_drop.append(key2)

        if len(keys_to_drop) != 0:
                for key, value in LinkedPriceLevels.items():
                    structures[key] = value

                for i in keys_to_drop:
                    structures.pop(i)
                

   

        
        if agent_date >= dt.datetime(2022, 1, 1, 19, 0, 0):

            print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)

            n = 30
            prices = daily.loc[agent_date  - dt.timedelta(days=90):agent_date, 'close']
            std = prices.pct_change().rolling(window=n).std()
            average_std = std.rolling(window=n).mean()
            VF = std / average_std

            lookbacks = VF * 30
            lookbacks = lookbacks.fillna(0)

            todays_lookback = int(lookbacks[-1])
            print(Fore.LIGHTGREEN_EX + 'todays lookback = ', str(todays_lookback) + Style.RESET_ALL)

            prices = prices.loc[agent_date - dt.timedelta(days=todays_lookback - 1):agent_date]
            prices_direction = prices[-1] - prices[0]
            print('Lookback date = ' , prices.index[0])
            print('price direction =', prices_direction)

            if prices_direction  > 0:
                  trend = 'BULL'
            
            elif prices_direction < 0:
                  trend = 'BEAR'
            
            print(Fore.LIGHTYELLOW_EX + 'Trend = ' + str(trend), Style.RESET_ALL)

            if trend == 'BULL' and agent_date >= exit_time:
                  position, exit_time = zoom1Hr(trend, structures, agent_date)
            
            elif trend == 'BEAR' and agent_date >= exit_time:
                  position, exit_time = zoom1Hr(trend, structures, agent_date)
            

            print(Fore.LIGHTYELLOW_EX + 'Position = ' + str(position), Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)

            if position == True:
                  if trend == 'BEAR':
                        exit_time, last_area = Trade(asset, 'SHORT', exit_time, structures)
                        position = False

                  elif trend == 'BULL':
                        exit_time, last_area = Trade(asset, 'LONG', exit_time, structures)
                        position = False


            print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)
            print('ULTIMA ZONA DE CONTACTO = ', last_area)
           




            res = input('Continue ?')
            if res == '':
                    close_to_area = False
                    print('-------------------------------------------------')
                    continue


        
    
      



    
