import matplotlib.pyplot as plt
from binance.client import Client
import time
import keys

# Replace YOUR_API_KEY and YOUR_API_SECRET with your own Binance API key and secret
client = Client(keys.binance_api_key,keys.binance_api_secret)

# Initialize empty lists for the timestamps and closing prices
timestamps = []
closing_prices = []

# Set the number of points to plot on the graph
num_points = 100

while True:
    # Get the BTC/USDT historical data
    klines = client.futures_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE)

    # Extract the timestamp and closing price from the latest candlestick
    timestamp = int(klines[-1][0]) / 1000
    closing_price = float(klines[-1][4])

    # Add the timestamp and closing price to the lists
    timestamps.append(timestamp)
    closing_prices.append(closing_price)

    # Keep the lists at a fixed length
    if len(timestamps) > num_points:
        timestamps.pop(0)
        closing_prices.pop(0)

    # Create the plot
    plt.plot(timestamps, closing_prices)

    # Show the plot
    plt.show(block=False)
    plt.pause(1)
    plt.clf()

    # Sleep for 1 second
    time.sleep(1)
