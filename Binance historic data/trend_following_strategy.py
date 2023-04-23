import numpy as np
from binance.client import Client
import keys

client = Client(keys.binance_api_key, keys.binance_api_secret)
def trend_following(symbol, interval, fast_period, slow_period):
    # Replace YOUR_API_KEY and YOUR_API_SECRET with your own Binance API key and secret


    # Initialize empty lists for the timestamps and closing prices
    timestamps = []
    closing_prices = []

    # Get the historical data
    klines = client.futures_klines(symbol=symbol, interval=interval)

    # Extract the timestamp and closing price from the historical data
    for kline in klines:
        timestamps.append(int(kline[0]) / 1000)
        closing_prices.append(float(kline[4]))

    # Convert the lists to numpy arrays
    timestamps = np.array(timestamps)
    closing_prices = np.array(closing_prices)

    # Calculate the fast and slow moving averages
    fast_moving_average = np.mean(closing_prices[-fast_period:])
    slow_moving_average = np.mean(closing_prices[-slow_period:])

    # Check if the fast moving average is above the slow moving average
    if fast_moving_average > slow_moving_average:
        # The trend is up, so return 1
        return 1
    else:
        # The trend is down, so return -1
        return -1

closing_prices = []
while True:
    trend = trend_following("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, 12, 26)
    klines = client.futures_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE)
    for kline in klines:
        #print(float(kline[4]))
        closing_prices.append(float(kline[4]))
    print(trend)

'''symbol: The symbol of the asset to follow (e.g. "BTCUSDT")
interval: The interval of the historical data to retrieve (e.g. Client.KLINE_INTERVAL_1MINUTE)
fast_period: The number of periods to include in the fast moving average
slow_period: The number of periods to include in the slow moving average'''
