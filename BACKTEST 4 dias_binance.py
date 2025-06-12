import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
#pd.set_option("display.max_rows", None)
import talib as ta
import datetime as dt
import statistics


pairs = [
    'BTC'
    ]


signals = pd.read_csv(
    'signals.csv'
    )

_2017 = pd.to_datetime('2017-01-01 19:00:00')
_2018 = pd.to_datetime('2018-01-01 19:00:00')
_2018_06_01 = pd.to_datetime('2018-06-01 19:00:00')
_2019 = pd.to_datetime('2019-01-01 19:00:00')
_2019_06_01 = pd.to_datetime('2019-06-01 19:00:00')
_2019_08_01 = pd.to_datetime('2019-08-01 19:00:00')
_2020 = pd.to_datetime('2020-01-01 19:00:00')
_2020_04_10 = pd.to_datetime('2020-04-10 19:00:00')
_2020_06_01 = pd.to_datetime('2020-06-01 19:00:00')
_2020_08_01 = pd.to_datetime('2020-08-01 19:00:00')
_2020_10_01 = pd.to_datetime('2020-10-01 19:00:00')
_2021_02_01 = pd.to_datetime('2021-02-01 19:00:00')
_2021_03_01 = pd.to_datetime('2021-03-01 19:00:00')
_2021_04_01 = pd.to_datetime('2021-04-01 19:00:00')
_2021_05_01 = pd.to_datetime('2021-05-01 19:00:00')
_2021_06_01 = pd.to_datetime('2021-06-01 19:00:00')
_2021_07_01 = pd.to_datetime('2021-07-01 19:00:00')
_2021_08_01 = pd.to_datetime('2021-08-01 19:00:00')
_2021_09_01 = pd.to_datetime('2021-09-01 19:00:00')
_2021_10_01 = pd.to_datetime('2021-10-01 19:00:00')
_2021_11_01 = pd.to_datetime('2021-11-01 19:00:00')
_2021_11_08 = pd.to_datetime('2021-11-08 19:00:00')
_2021_12_01 = pd.to_datetime('2021-12-01 19:00:00')
_2021 = pd.to_datetime('2021-01-01 19:00:00')
_2022 = pd.to_datetime('2022-01-01 19:00:00')
_2022_01_06 = pd.to_datetime('2022-01-06 19:00:00')
_2022_02_01 = pd.to_datetime('2022-02-01 19:00:00')
_2022_02_15 = pd.to_datetime('2022-02-15 19:00:00')
_2022_02_28 = pd.to_datetime('2022-02-28 19:00:00')
_2022_03_01 = pd.to_datetime('2022-03-01 19:00:00')
_2022_04_01 = pd.to_datetime('2022-04-01 19:00:00')
_2022_04_10 = pd.to_datetime('2022-04-10 19:00:00')
_2022_04_26 = pd.to_datetime('2022-04-26 19:00:00')
_2022_05_01 = pd.to_datetime('2022-05-01 19:00:00')
_2022_05_09 = pd.to_datetime('2022-05-09 19:00:00')
_2022_05_10 = pd.to_datetime('2022-05-10 19:00:00')
_2022_05_13 = pd.to_datetime('2022-05-13 19:00:00')
_2022_05_19 = pd.to_datetime('2022-05-19 19:00:00')
_2022_05_20 = pd.to_datetime('2022-05-20 19:00:00')
_2022_06_01 = pd.to_datetime('2022-06-01 19:00:00')
_2022_06_06 = pd.to_datetime('2022-06-06 19:00:00')
_2022_06_12 = pd.to_datetime('2022-06-12 19:00:00')
_2022_06_14 = pd.to_datetime('2022-06-14 19:00:00')
_2022_06_18 = pd.to_datetime('2022-06-18 19:00:00')
_2022_06_19 = pd.to_datetime('2022-06-19 19:00:00')
_2022_06_20 = pd.to_datetime('2022-06-20 19:00:00')
_2022_07_01 = pd.to_datetime('2022-07-01 19:00:00') 
_2022_07_02 = pd.to_datetime('2022-07-02 19:00:00') 
_2022_07_12 = pd.to_datetime('2022-07-12 19:00:00')
_2022_07_18 = pd.to_datetime('2022-07-18 19:00:00')
_2022_07_29 = pd.to_datetime('2022-07-29 19:00:00')
_2022_08_01 = pd.to_datetime('2022-08-01 19:00:00')
_2022_08_11 = pd.to_datetime('2022-08-11 19:00:00')
_2022_09_01 = pd.to_datetime('2022-09-01 19:00:00')
_2022_09_02 = pd.to_datetime('2022-09-02 19:00:00')
_2022_09_10 = pd.to_datetime('2022-09-10 19:00:00')
_2022_09_22 = pd.to_datetime('2022-09-22 19:00:00')
_2022_10_01 = pd.to_datetime('2022-10-01 19:00:00')
_2022_10_28 = pd.to_datetime('2022-10-28 19:00:00')
_2022_11_01 = pd.to_datetime('2022-11-01 19:00:00')
_2022_11_03 = pd.to_datetime('2022-11-03 19:00:00')
_2022_11_08 = pd.to_datetime('2022-11-08 19:00:00')
_2022_11_15 = pd.to_datetime('2022-11-15 19:00:00')
_2022_11_17 = pd.to_datetime('2022-11-17 19:00:00')
_2022_12_01 = pd.to_datetime('2022-12-01 19:00:00')
_2022_12_10 = pd.to_datetime('2022-12-10 19:00:00')
_2023 = pd.to_datetime('2023-01-01 19:00:00')
_2023_01_24 = pd.to_datetime('2023-01-24 19:00:00')
_2023_02_01 = pd.to_datetime('2023-02-01 19:00:00')
_2023_02_28 = pd.to_datetime('2023-02-28 19:00:00')
_2023_03_01 = pd.to_datetime('2023-03-01 19:00:00')
_2023_04_10 = pd.to_datetime('2023-04-10 19:00:00')
_2023_05_09 = pd.to_datetime('2023-05-09 19:00:00')
_2023_05_13 = pd.to_datetime('2023-05-13 19:00:00')
_2023_05_19 = pd.to_datetime('2023-05-19 19:00:00')
_2023_05_20 = pd.to_datetime('2023-05-20 19:00:00')


date_start = _2022_09_01
date_end = _2023

signals.index = pd.to_datetime(signals['time'])
signals = signals.drop('time', axis=1)
signals = signals.loc[date_start:]
print(signals)

strategy_returns  = pd.DataFrame(columns=['returns', 'coins traded', 'positions'], index = signals.index)
exit_time = ''


for date in signals.index:
    print('----------------------------------')
    print('date =', date)
    day_returns = []
    coins_traded = []
    positions = []

    entry_time = date
 
    if (date == dt.datetime(2023, 6, 15, 19, 0, 0) or 
        date == dt.datetime(2023, 6, 18, 19, 0, 0) or 
        date == dt.datetime(2023, 6, 19, 19, 0, 0)
        ):
        break

    if exit_time == '':

        for coin in pairs:
            print(coin)
            stop_loss_touch = False
            signal = signals.loc[date, coin]
            if signal == 1 or signal == -1:
                print(signal)
                asset_hourly_data = pd.read_csv(f'binance_hourly_prices/{coin}.csv')
                asset_hourly_data.index = pd.to_datetime(asset_hourly_data['time'])
                asset_hourly_data = asset_hourly_data.drop('Unnamed: 0', axis=1)
                asset_hourly_data = asset_hourly_data.drop('volume', axis=1)
                asset_hourly_data = asset_hourly_data.drop('time', axis=1)
                asset_hourly_data = asset_hourly_data.drop_duplicates()
                
                print(asset_hourly_data)
                
                entry_time = asset_hourly_data.loc[date + dt.timedelta(hours=2)].name
                print('entry time =', entry_time)
                open = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'open']
                high = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'high']
                low = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'low']
                close = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'close']
                entry_price = statistics.mean([open, high, low, close])
                #print('entry price =', entry_price)

                coins_traded.append(coin)
                positions.append(signal)

                exit_time = asset_hourly_data.loc[date + dt.timedelta(days=4)].name
                print('exit time =', exit_time)
                print('HOUR OF EXIT =', asset_hourly_data.loc[date + dt.timedelta(hours=98)].name)
                close_price = statistics.mean([
                        asset_hourly_data['open'].loc[date + dt.timedelta(hours=98)],
                        asset_hourly_data['high'].loc[date + dt.timedelta(hours=98)],
                        asset_hourly_data['low'].loc[date + dt.timedelta(hours=98)],
                        asset_hourly_data['close'].loc[date + dt.timedelta(hours=98)]
                                ])
                #print('close price =', close_price)

                trade = asset_hourly_data.loc[date + dt.timedelta(hours=3):date + dt.timedelta(hours=97)]
                print(trade)


                if signal == 1:
        
                    slippage_cost = entry_price * 0.001
                    entry_price = entry_price + slippage_cost
                
                    stop_loss = entry_price*(1-0.08)

                    for i in trade.index:
                        hour = i
                        open = trade.loc[i].open
                        high = trade.loc[i].high
                        low = trade.loc[i].low
                        close = trade.loc[i].close

                        if open <=stop_loss or high<=stop_loss or low<=stop_loss or close<=stop_loss:
                            returns = pd.Series([entry_price, stop_loss])
                            returns = round(returns.pct_change()[1], 4)  
                            returns = returns - (returns * 0.0007)
                            day_returns.append(returns)
                            print('entry price =', entry_price, 'close price =', stop_loss)
                            print('return =', returns)
                            print('stop loss touched')
                            stop_loss_touch = True
                            break
                    
                    if stop_loss_touch == False:
            
                        returns = pd.Series([entry_price, close_price])
                        returns = round(returns.pct_change()[1], 4)
                        returns = returns - (returns * 0.0007)
                        day_returns.append(returns)
                        print('entry price =', entry_price, 'close price =', close_price)
                        print('retrun =', returns)
                        print('stop loss not touched')

                elif signal == -1:

                    slippage_cost = entry_price * 0.001
                    entry_price = entry_price - slippage_cost
                
                    
                    stop_loss = entry_price*(1+0.08)

                    for i in trade.index:
                        hour = i
                        open = trade.loc[i].open
                        high = trade.loc[i].high
                        low = trade.loc[i].low
                        close = trade.loc[i].close

                        if open >=stop_loss or high>=stop_loss or low>=stop_loss or close>=stop_loss:
                            returns = pd.Series([stop_loss, entry_price])
                            returns = round(returns.pct_change()[1], 4)  
                            returns = returns - (returns * 0.0007)
                            day_returns.append(returns)
                            print('entry price =', entry_price, 'close price =', stop_loss)
                            print('return =', returns)
                            print('stop loss touched')
                            stop_loss_touch = True

                            break
                    
                    if stop_loss_touch == False:
                        returns = pd.Series([close_price, entry_price])
                        returns = round(returns.pct_change()[1], 4)
                        returns = returns - (returns * 0.0007)
                        day_returns.append(returns)
                        print('entry price =', entry_price, 'close price =', close_price)
                        print('return =', returns)
                        print('stop loss not touched')
        
        print('day returns =', day_returns)
        if len(day_returns) > 0:
                print('dat returns =', sum(day_returns) / len(day_returns))
                strategy_returns.loc[exit_time, 'returns']  = sum(day_returns) / len(day_returns)
                strategy_returns.loc[exit_time, 'coins traded']  = coins_traded
                strategy_returns.loc[exit_time, 'positions']  = positions
        
        if len(positions) == 0:
                exit_time = ''
        


    elif date == exit_time:
        print('exit time match with date= ', exit_time)
        for coin in pairs:
            print(coin)
            stop_loss_touch = False
            signal = signals.loc[date, coin]
            if signal == 1 or signal == -1:
                print(signal)
                asset_hourly_data = pd.read_csv(f'binance_hourly_prices/{coin}.csv')
                asset_hourly_data.index = pd.to_datetime(asset_hourly_data['time'])
                asset_hourly_data = asset_hourly_data.drop('Unnamed: 0', axis=1)
                asset_hourly_data = asset_hourly_data.drop('volume', axis=1)
                asset_hourly_data = asset_hourly_data.drop('time', axis=1)
                asset_hourly_data = asset_hourly_data.drop_duplicates()
                
                print(asset_hourly_data)

                entry_time = asset_hourly_data.loc[date + dt.timedelta(hours=2)].name
                print('entry time =', entry_time)
                open = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'open']
                high = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'high']
                low = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'low']
                close = asset_hourly_data.loc[date + dt.timedelta(hours=2), 'close']
                entry_price = statistics.mean([open, high, low, close])
                #print('entry price =', entry_price)

                coins_traded.append(coin)
                positions.append(signal)

                exit_time = asset_hourly_data.loc[date + dt.timedelta(days=4)].name
                print('exit time =', exit_time)
                print('HOUR OF EXIT =', asset_hourly_data.loc[date + dt.timedelta(hours=98)].name)

                close_price = statistics.mean([
                        asset_hourly_data['open'].loc[date + dt.timedelta(hours=98)],
                        asset_hourly_data['high'].loc[date + dt.timedelta(hours=98)],
                        asset_hourly_data['low'].loc[date + dt.timedelta(hours=98)],
                        asset_hourly_data['close'].loc[date + dt.timedelta(hours=98)]
                                ])
                #print('close price =', close_price)

                trade = asset_hourly_data.loc[date + dt.timedelta(hours=3):date + dt.timedelta(hours=97)]
                print(trade)


                if signal == 1:
        
                    slippage_cost = entry_price * 0.001
                    entry_price = entry_price + slippage_cost
                
                    stop_loss = entry_price*(1-0.08)

                    for i in trade.index:
                        hour = i
                        open = trade.loc[i].open
                        high = trade.loc[i].high
                        low = trade.loc[i].low
                        close = trade.loc[i].close

                        if open <=stop_loss or high<=stop_loss or low<=stop_loss or close<=stop_loss:
                            returns = pd.Series([entry_price, stop_loss])
                            returns = round(returns.pct_change()[1], 4)  
                            returns = returns - (returns * 0.0007)
                            day_returns.append(returns)
                            print('entry price =', entry_price, 'close price =', stop_loss)
                            print(returns)
                            print('stop loss touched')
                            stop_loss_touch = True
                
                            break

                    if stop_loss_touch == False:
                        returns = pd.Series([entry_price, close_price])
                        returns = round(returns.pct_change()[1], 4)
                        returns = returns - (returns * 0.0007)
                        day_returns.append(returns)
                        print('entry price =', entry_price, 'close price =', close_price)
                        print(returns)
                        print('stop loss not touched')


                elif signal == -1:

                    slippage_cost = entry_price * 0.001
                    entry_price = entry_price - slippage_cost
                
                    
                    stop_loss = entry_price*(1+0.08)

                    for i in trade.index:
                        hour = i
                        open = trade.loc[i].open
                        high = trade.loc[i].high
                        low = trade.loc[i].low
                        close = trade.loc[i].close
                        
                        if open >= stop_loss or high >= stop_loss or low >= stop_loss or close >= stop_loss:
                            returns = pd.Series([stop_loss, entry_price])
                            returns = round(returns.pct_change()[1], 4)  
                            returns = returns - (returns * 0.0007)
                            day_returns.append(returns)
                            print('entry price =', entry_price, 'close price =', stop_loss)
                            print(returns)
                            print('stop loss touched')
                            stop_loss_touch = True
        
                            break

                    if stop_loss_touch == False:
                        returns = pd.Series([close_price, entry_price])
                        returns = round(returns.pct_change()[1], 4)
                        returns = returns - (returns * 0.0007)
                        day_returns.append(returns)
                        print('entry price =', entry_price, 'close price =', close_price)
                        print(returns)
                        print('stop loss not touched')

        print('day returns =', day_returns)
        if len(day_returns) > 0:
                print('dat returns =', sum(day_returns) / len(day_returns))
                strategy_returns.loc[exit_time, 'returns']  = sum(day_returns) / len(day_returns)
                strategy_returns.loc[exit_time, 'coins traded']  = coins_traded
                strategy_returns.loc[exit_time, 'positions']  = positions

        if len(positions) == 0:
                exit_time = ''

pd.set_option("display.max_rows", None)
print(strategy_returns)
strategy_returns = strategy_returns.dropna()
print(strategy_returns)
wins = 0
losses = 0
for i in strategy_returns.values:
    if i[0]>0:
        wins += 1
    elif i[0]<0:
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

# Plot the cumulative strategy returns
#daily_returns['returns'].cumsum().plot(figsize=(10, 7))
(strategy_returns['returns']+1).cumprod().plot(figsize=(10, 7))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()

strategy_returns['returns'].cumsum().plot(figsize=(10, 7))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()


