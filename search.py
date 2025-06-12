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


def Trade(asset, entry_time, position, take_profit):    

    print('TIEMPO DE ENTRADA == ',entry_time)
    entry_time = entry_time + dt.timedelta(hours=5)
    print('TIEMPO DE ENTRADA == ',entry_time)

    
    hours = pd.read_csv(f'binance_hourly_prices/{asset}.csv')

    hours.index = hours['time']
    hours = hours.drop('time', axis=1)
    hours = hours.drop('Unnamed: 0', axis=1)
    hours = hours.drop('volume', axis=1)
    hours = hours.fillna(0)
    
    hours.index = pd.to_datetime(hours.index)
    hours = hours.drop_duplicates()
    
    open = hours.loc[entry_time].open
    high = hours.loc[entry_time].high
    low = hours.loc[entry_time].low
    close = hours.loc[entry_time].close


    entry_price = statistics.mean([open, high, low, close])

    if position == 'LONG':
        print('entry price =', entry_price)
        slippage_cost = entry_price * 0.001
        entry_price = entry_price + slippage_cost
        print('entry price =', entry_price)

        if (
            entry_price >= take_profit and take_profit != 0
            ):
            
            print('TAKE PROFIT < ENTRY PRICE (LONG POSITION - BUG - PRICE GAPS) ')

            return entry_time

        if abs(entry_price - take_profit) < entry_price * 0.003:
            print('PRICE EXTREMELY CLOSE TO TAKE PROFIT LEVEL')
            return entry_time
        
        if take_profit == 0:
            take_profit = entry_price + (entry_price * 0.03)
            print(Fore.GREEN + 'Take profit =' + str(take_profit) + Style.RESET_ALL)
        
        else:
            take_profit = take_profit
            print(Fore.GREEN + 'Take profit =' + str(take_profit) + Style.RESET_ALL)
            
        stop_loss = entry_price - (entry_price * 0.03)
        print(Fore.RED + 'Stop loss =' + str(stop_loss) + Style.RESET_ALL)
        
    elif position == 'SHORT':
        print('entry price =', entry_price)
        slippage_cost = entry_price * 0.001
        entry_price = entry_price - slippage_cost
        print('entry price =', entry_price)

        if (
            entry_price <= take_profit and take_profit != 0
            ):
            
            print('TAKE PROFIT < ENTRY PRICE (SHORT POSITION - BUG - PRICE GAPS) ')
            return entry_time

        if abs(entry_price - take_profit) < entry_price * 0.003:
            print('PRICE EXTREMELY CLOSE TO TAKE PROFIT LEVEL')
            return entry_time

        if take_profit == 0:
            take_profit = entry_price - (entry_price * 0.03)
            print(Fore.GREEN + 'Take profit =' + str(take_profit) + Style.RESET_ALL)
        
        else:
            take_profit = take_profit
            print(Fore.GREEN + 'Take profit =' + str(take_profit) + Style.RESET_ALL)
        
        stop_loss = entry_price + (entry_price * 0.03)
        print(Fore.RED + 'Stop loss =' + str(stop_loss) + Style.RESET_ALL)

    hours = hours.loc[entry_time:]
    print(hours)

    for i in hours.index:
        print('time = ', hours.loc[i].name)
        time = hours.loc[i].name
        o = hours.loc[i, 'open']
        print('open =', o)
        h = hours.loc[i, 'high']
        print('high =', h)
        l = hours.loc[i, 'low']
        print('low =', l)
        c = hours.loc[i, 'close']
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
                     'entry price' : entry_price,
                     'exit price' : take_profit,
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
                     'entry price' : entry_price,
                     'exit price' : stop_loss,
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
                     'entry price' : entry_price,
                     'exit price' : take_profit,
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
                     'entry price' : entry_price,
                     'exit price' : stop_loss,
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
        
        


def zoom4hrs(asset, time, boundaries, structures, trend):
    print('**************************************************')
    print('TREND = ', trend)
    print(Fore.LIGHTYELLOW_EX + '4 HRS ZOOM' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + ' DAILY AGENT TIME = ' + str(time) + Style.RESET_ALL)

    short_confirmations = 0
    long_confirmations = 0

    prices_last_confimation = {}
    take_profit = 0


    H4 = pd.DataFrame(columns=['open', 'high', 'low', 'close'])
    
    H4 = pd.read_csv(f'binance_4_hrs/{asset}.csv')

    H4.index = H4['time']
    H4 = H4.drop('time', axis=1)
    H4 = H4.drop('Unnamed: 0', axis=1)
    H4 = H4.drop('volume', axis=1)
    H4 = H4.fillna(0)

    H4.index = pd.to_datetime(H4.index)
    H4 = H4.drop_duplicates()

    print(H4)
    
    end_iteration_time = time + dt.timedelta(days=4)

    try:
        print(H4.loc[end_iteration_time])

    except:
        end_iteration_time = time + dt.timedelta(days=3)


    H4 = H4.loc[time:end_iteration_time]
    print(H4)


    for i in H4.index:
        print('time = ', H4.loc[i].name)
        time = H4.loc[i].name
        o = H4.loc[i, 'open']
        print('open =', o)
        h = H4.loc[i, 'high']
        print('high =', h)
        l = H4.loc[i, 'low']
        print('low =', l)
        c = H4.loc[i, 'close']
        print('close =', c)

        if c > o:
            current_candle = 'BULL'
        
        elif c < o:
            current_candle = 'BEAR'
        
        print('CURRENT CANDLE = ', current_candle)

        if c < boundaries['lower zone'] and current_candle == 'BEAR' and trend == 'BEAR':

            if short_confirmations == 0:
                print('boundaries["lower zone"]  = ' ,boundaries['lower zone'])
                prices_last_confimation['BEAR'] = c
                short_confirmations += 1
                print(Fore.LIGHTRED_EX  + 'SHORT CONFIRMATIONS = ', str(short_confirmations) + Style.RESET_ALL)
            
            elif short_confirmations == 1 and (c < prices_last_confimation['BEAR'] - prices_last_confimation['BEAR'] * 0.015):
                short_confirmations += 1
                print(Fore.LIGHTRED_EX  + 'SHORT CONFIRMATIONS = ', str(short_confirmations) + Style.RESET_ALL)

                entry_time = time
                objectives = []
                
                for date, area in structures.items():
                            print('-------------------------------')
                            print(date, ' = ' , area)
                            print('Area = ', area[0])

                            if len(area) == 1:

                                if (
                                    c < area[0] + area[0] * 0.04 and
                                    c > area[0] 
                                    ):

                                    print('Price close to another structure = ' + date, ' = ' , area)
                                    if (c < area[0] + area[0] * 0.003 and 
                                        c > area[0]):
                                        print('Price too close to another structure = ', area[0])
                                        upper_zone = area[0] + area[0] * 0.012
                                        lower_zone = area[0] - area[0] * 0.012

                                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                        print('New Boundaries = ', boundaries)
                                        short_confirmations = 0
                                        print(Fore.LIGHTRED_EX  + 'SHORT CONFIRMATIONS = ', str(short_confirmations) + Style.RESET_ALL)
                                        prices_last_confimation['BEAR'] = 0
                                        objectives = []
                                        break

                                    else:
                                        
                                        objectives.append(area[0])

                                elif (c < area[0] and c > area[0] - area[0] * 0.003):
                                        print('Price too close to another structure = ', area[0])
                                        upper_zone = area[0] + area[0] * 0.012
                                        lower_zone = area[0] - area[0] * 0.012

                                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                        print('New Boundaries = ', boundaries)
                                        short_confirmations = 0
                                        print(Fore.LIGHTRED_EX  + 'BEAR CONFIRMATIONS = ', str(short_confirmations) + Style.RESET_ALL)
                                        prices_last_confimation['BEAR'] = 0
                                        objectives = []
                                        break

                                else:
                                    print('Structures away..')

                            elif len(area) > 1:
                                    if (
                                    c < max(area) + max(area) * 0.04 and 
                                    c > max(area)
                                    ):

                                        print('Price close to another structure = ' + date, ' = ' , max(area))

                                        if(c < max(area) + max(area) * 0.003 and 
                                            c > max(area)):
                                            print('Price too close to another structure = ', area)
                                            upper_zone = max(area) + max(area) * 0.012
                                            lower_zone = min(area) - min(area) * 0.012

                                            boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                            print('New Boundaries = ', boundaries)
                                            short_confirmations = 0
                                            print(Fore.LIGHTRED_EX  + 'BEAR CONFIRMATIONS = ', str(short_confirmations) + Style.RESET_ALL)
                                            prices_last_confimation['BEAR'] = 0
                                            objectives = []
                                            break

                                        else:
                                        
                                            objectives.append(max(area))

                                    elif (c < max(area) and c > max(area) - max(area) * 0.003):
                                        print('Price too close to another structure = ', area[0])
                                        upper_zone = max(area) + max(area) * 0.012
                                        lower_zone = min(area) - min(area) * 0.012

                                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                        print('New Boundaries = ', boundaries)
                                        short_confirmations = 0
                                        print(Fore.LIGHTRED_EX  + 'BEAR CONFIRMATIONS = ', str(short_confirmations) + Style.RESET_ALL)
                                        prices_last_confimation['BEAR'] = 0
                                        objectives = []
                                        break
                                        
                                    else:
                                        print('Structures away..')
                            
                            

                if len(objectives) == 1:
                         take_profit = objectives[0]
                    
                elif len(objectives) > 1:
                         take_profit = max(objectives)
                         
                
                if short_confirmations == 2:
                    return entry_time, 'SHORT', take_profit
            
            
        elif c > boundaries['upper zone'] and current_candle == 'BULL' and trend == 'BULL':
             
            if long_confirmations == 0:
                print('boundaries["upper zone"]  = ' ,boundaries['upper zone'])
                prices_last_confimation['BULL'] = c
                long_confirmations += 1
                print(Fore.LIGHTGREEN_EX  + 'BULL CONFIRMATIONS = ', str(long_confirmations) + Style.RESET_ALL)
            
            elif long_confirmations == 1 and (c > prices_last_confimation['BULL'] + prices_last_confimation['BULL'] * 0.015):
                long_confirmations += 1
                print(Fore.LIGHTGREEN_EX  + 'BULL CONFIRMATIONS = ', str(long_confirmations) + Style.RESET_ALL)

                entry_time = time
                objectives = []
                for date, area in structures.items():
                            print('-------------------------------')
                            print(date, ' = ' , area)
                            print('Area = ', area[0])

                            if len(area) == 1:

                                if (
                                    c > area[0] - area[0] * 0.04 and 
                                    c < area[0]
                                    ):

                                    print('Price close to another structure = ' + date, ' = ' , area)

                                    if (c > area[0] - area[0] * 0.003 and 
                                        c < area[0]):
                                        print('Price too close to another structure = ', area[0])
                                        upper_zone = area[0] + area[0] * 0.012
                                        lower_zone = area[0] - area[0] * 0.012

                                        boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                        print('New Boundaries = ', boundaries)
                                        long_confirmations = 0
                                        print(Fore.LIGHTGREEN_EX  + 'BULL CONFIRMATIONS = ', str(long_confirmations) + Style.RESET_ALL)
                                        prices_last_confimation['BULL'] = 0
                                        objectives = []
                                        break

                                    else:
                                        
                                        objectives.append(area[0])

                                
                                elif (c > area[0] and c < area[0] + area[0] * 0.003):
                                    print('Price too close to another structure = ', area[0])
                                    upper_zone = area[0] + area[0] * 0.012
                                    lower_zone = area[0] - area[0] * 0.012

                                    boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                    print('New Boundaries = ', boundaries)
                                    long_confirmations = 0
                                    print(Fore.LIGHTGREEN_EX  + 'BULL CONFIRMATIONS = ', str(long_confirmations) + Style.RESET_ALL)
                                    prices_last_confimation['BULL'] = 0
                                    objectives = []
                                    break

                                else:
                                    print('Structures away..')

                                
                            elif len(area) > 1:
                                if (
                                    c > min(area) - min(area) * 0.04 and 
                                    c < min(area)
                                    ):

                                        print('Price close to another structure = ' + date, ' = ' , min(area))

                                        if(c > min(area) - min(area) * 0.003 and 
                                            c < min(area)):
                                            print('Price too close to another structure = ', area)
                                            upper_zone = max(area) + max(area) * 0.012
                                            lower_zone = min(area) - min(area) * 0.012

                                            boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                            print('New Boundaries = ', boundaries)
                                            long_confirmations = 0
                                            print(Fore.LIGHTGREEN_EX  + 'BULL CONFIRMATIONS = ', str(long_confirmations) + Style.RESET_ALL)
                                            prices_last_confimation['BULL'] = 0
                                            objectives = []
                                            break
                                    
                                        else:

                                            objectives.append(min(area))

                                elif (c > min(area) and c < min(area) + min(area) * 0.003):
                                    print('Price too close to another structure = ', area[0])
                                    upper_zone = max(area) + max(area) * 0.012
                                    lower_zone = min(area) - min(area) * 0.012

                                    boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                                    print('New Boundaries = ', boundaries)
                                    long_confirmations = 0
                                    print(Fore.LIGHTGREEN_EX  + 'BULL CONFIRMATIONS = ', str(long_confirmations) + Style.RESET_ALL)
                                    prices_last_confimation['BULL'] = 0
                                    objectives = []
                                    break

                                else:
                                    print('Structures away..')

                                
                                        
                            

                if len(objectives) == 1:
                         take_profit = objectives[0]
                    
                elif len(objectives) > 1:
                         take_profit = min(objectives)
                
                if long_confirmations == 2:
                        return entry_time, 'LONG' , take_profit
        

        """
        res = input('Continue ?')
        if res == '':
            print('-------------------------------------------------')
            continue
        """
        
        
    
    if long_confirmations < 2 or short_confirmations < 2:
          return None, None , 0
    


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


    for day in range(3, len(daily) - 3):
        print('***********************************************************************************')
        print('***********************************************************************************')
        
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

        if agent_date == dt.datetime(2023, 7, 1, 19, 0, 0):
             break

        print(Fore.LIGHTRED_EX + 'Agent Date = ' + str(agent_date) + Style.RESET_ALL)
        
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
            

        print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)

        def is_close(value1, value2):
                threshold = 0.02 * min(value1, value2)
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
                

        print(Fore.LIGHTCYAN_EX + 'Structures = ' + str(structures) +  Style.RESET_ALL)


        if agent_date >= dt.datetime(2022, 1, 1, 19, 0, 0):

            n = 30
            prices = daily.loc[agent_date  - dt.timedelta(days=90):agent_date, 'close']
            std = prices.pct_change().rolling(window=n).std()
            average_std = std.rolling(window=n).mean()
            VF = std / average_std

            lookbacks = VF * 30
            lookbacks = lookbacks.fillna(0)

            todays_lookback = int(lookbacks[-1])
            print('todays lookback = ', todays_lookback)

            prices = prices.loc[agent_date - dt.timedelta(days=todays_lookback - 1):agent_date]
            prices_direction = prices[-1] - prices[0]
            print('price direction =', prices_direction)

            

            if prices_direction < 0:
                trend = 'BEAR'
            
            elif prices_direction > 0:
                trend = 'BULL'


            threshold = 0.012

            if len(structures) != 0 and agent_date > exit_time:

                for date, area in structures.items():
                    print('-------------------------------')
                    print(date, ' = ' , area)
                    if len(area) == 1:
                        print('Area = ', area[0])
                        upper_zone = area[0] + area[0] * threshold
                        lower_zone = area[0] - area[0] * threshold
            
                        if (
                            current_price < upper_zone and current_price > lower_zone
                            ) and close_to_area != True:

                            close_to_area = True
                            boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                            print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(current_price) + Style.RESET_ALL)
                            continue

                    elif len(area) > 1:
                        print('Area = ', area)
                        upper_zone = max(area) + max(area) * threshold
                        lower_zone = min(area) - min(area) * threshold
            
                        if (
                            current_price < upper_zone and current_price > lower_zone or
                            current_price >= min(area) and current_price <= max(area)
                            ) and close_to_area != True:

                            close_to_area = True
                            boundaries = {'upper zone' : upper_zone, 'lower zone' : lower_zone}
                            print(Fore.LIGHTRED_EX + 'Price in Area = ' + str(current_price) + Style.RESET_ALL)
                            continue
            
            

            print(Fore.LIGHTBLUE_EX + 'Exit Time = ' + str(exit_time) + Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX  + 'close to area = ' + str(close_to_area) + Style.RESET_ALL)
            print('Boundaries = ', boundaries)

            
            if len(boundaries) != 0 and close_to_area == True and agent_date > exit_time:
                print('Upper zone = ', boundaries['upper zone'])
                print('Lower zone = ', boundaries['lower zone'])

                entry_time, position , take_profit = zoom4hrs(asset, agent_date, boundaries, structures, trend)
                print('ENTRY TIME = ', entry_time)
            

                
            print('Take profit = ', take_profit)
            print('Position = ' + str(position))

            if position == 'SHORT':

                exit_time = Trade(asset, entry_time, 'SHORT', take_profit)
                position = None
                boundaries = {}
                close_to_area = False
                take_profit = 0
            
            elif position == 'LONG':

                exit_time = Trade(asset, entry_time, 'LONG', take_profit)
                position = None
                boundaries = {}
                close_to_area = False
                take_profit = 0
                
            """
            res = input('Continue ?')
            if res == '':
                close_to_area = False
                print('-------------------------------------------------')
                continue
            """
            
            
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
