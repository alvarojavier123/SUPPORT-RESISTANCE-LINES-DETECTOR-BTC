import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


pairs = ['BTCUSDT']

print(pairs)

url = 'https://api.binance.com/api/v3/klines'

for symbol in pairs:
    startTime = str(int(dt.datetime(2017, 1, 1).timestamp() * 1000))
    endTime = dt.datetime.now()
    data = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    while True:
        print(symbol)
        separator = ' '
        params = {
            'symbol' : symbol,
            'interval' : '4h',
            'startTime' : startTime,
            'endTime' : str(int(dt.datetime.now().timestamp() * 1000))
        }

        req = requests.get(url, params= params)
        req = json.loads(req.text)
        for x in req:
            time = dt.datetime.fromtimestamp(x[0] / 1000)
            print(time)
            open = x[1]
            high = x[2]
            low = x[3]
            close = x[4]
            volume = x[5]
            data = data.append({
                'time' : time,
                'open' : open,
                'high' : high,
                'low' : low,
                'close' : close,
                'volume' : volume
            }, ignore_index=True)

        if str(data.iloc[-1].time) == '2023-07-30 15:00:00':
            data.to_csv(f'binance_4_hrs/{symbol}.csv')
            break
        else:   
            startTime = str(int(data.iloc[-1].time.timestamp() * 1000))
            print(data.iloc[-1].time)
            continue


