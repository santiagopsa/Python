# Import necessary libraries
import numpy as np
import requests
import pickle
import pandas as pd
import talib
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import keys

# Set the API key and secret
api_key = keys.binance_api_key
api_secret = keys.binance_api_key
# Set the asset, interval, and dates
asset = 'BTCUSDT'
interval = '5m'

# Create a new start_date string in the correct format
start_date_str = '2023-01-13'

# Convert the start_date string to a datetime object
start_date = datetime.datetime.fromisoformat(start_date_str)

# Convert the datetime object to a Unix timestamp in milliseconds
start_timestamp = int(start_date.timestamp() * 1000)

# Create a new end_date string in the correct format
end_date_str = '2023-01-14'

# Convert the end_date string to a datetime object
end_date = datetime.datetime.fromisoformat(end_date_str)

# Convert the datetime object to a Unix timestamp in milliseconds
end_timestamp = int(end_date.timestamp() * 1000)

# Set the URL and headers for the request
url = f'https://api.binance.com/api/v3/klines?symbol={asset}&interval={interval}&startTime={start_timestamp}&endTime={end_timestamp}'
headers = {'X-MBX-APIKEY': api_key}

# Send the request and retrieve the data
data = requests.get(url, headers=headers).json()
print(data)
# Convert the data to a pandas dataframe
df = pd.DataFrame(data, columns=[
  'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
  'quote_asset_volume', 'trades', 'taker_buy_base_asset_volume',
  'taker_buy_quote_asset_volume', 'ignore'
])
# Convert the timestamp columns to datetime
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

# Set the timestamp column as the index
df.set_index('open_time', inplace=True)
print(df)

# Convert the open, high, low, and close columns to floats
df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

# Calculate various technical indicators to use as features for the machine learning model
df['sma_5'] = df['close'].rolling(5).mean()
df['sma_10'] = df['close'].rolling(10).mean()
df['sma_20'] = df['close'].rolling(20).mean()
df['sma_50'] = df['close'].rolling(50).mean()
df['sma_200'] = df['close'].rolling(200).mean()
df['rsi_14'] = talib.RSI(df['close'], 14)
df['willr_14'] = talib.WILLR(df['high'], df['low'], df['close'], 14)
df['adx_14'] = talib.ADX(df['high'], df['low'], df['close'], 14)
df['cci_14'] = talib.CCI(df['high'], df['low'], df['close'], 14)
df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['atr_14'] = talib.ATR(df['high'], df['low'], df['close'], 14)
df['bollinger_upper'], df['bollinger_middle'], df['bollinger_lower'] = talib.BBANDS(df['close'], timeperiod=14, nbdevup=2, nbdevdn=2)

# fill nan values with 0
df['sma_5'] = df['sma_5'].fillna(0)
df['sma_10'] = df['sma_10'].fillna(0)
df['sma_20'] = df['sma_20'].fillna(0)
df['sma_50'] = df['sma_50'].fillna(0)
df['sma_200'] = df['sma_200'].fillna(0)
df['rsi_14'] = df['rsi_14'].fillna(0)
df['willr_14'] = df['willr_14'].fillna(0)
df['adx_14'] = df['adx_14'].fillna(0)
df['cci_14'] = df['cci_14'].fillna(0)
df['macd'] = df['macd'].fillna(0)
df['macd_signal'] = df['macd_signal'].fillna(0)
df['macd_hist'] = df['macd_hist'].fillna(0)
df['atr_14'] = df['atr_14'].fillna(0)
df['bollinger_upper'] = df['bollinger_upper'].fillna(0)
df['bollinger_middle'] = df['bollinger_middle'].fillna(0)
df['bollinger_lower'] = df['bollinger_lower'].fillna(0)

# Select the features to use for training
features = ['sma_5', 'sma_10', 'sma_20', 'sma_50', 'sma_200', 'rsi_14', 'willr_14', 'adx_14', 'cci_14', 'macd', 'macd_signal', 'macd_hist','atr_14','bollinger_upper','bollinger_middle','bollinger_lower']


# Split the data into a training set and a testing set
train_df = df[df.index < '2023-01-14']
test_df = df[df.index >= '2023-01-14']

# Check the number of rows in the dataframe
num_rows = df.shape[0]


# Check the names of the columns in the dataframe
column_names = df.columns

# Train a Random Forest Regressor model on the training data
model = RandomForestRegressor()
model.fit(train_df[features], train_df['close'])

# Use the model to make predictions on the testing data
predictions = model.predict(test_df[features])


#print('Predictions: '+ str(np.array_str(predictions)))

# Iterate through the predictions and decide whether to buy or sell
# Set a threshold for deciding whether to buy or sell
threshold = 100

# Iterate through the predictions and decide whether to buy or sell
for i in range(len(predictions)):
  if int(predictions[i]) > int(test_df.iloc[i]['close'] + threshold):
    print('Buy at ', test_df.iloc[i].name)
    print(test_df.iloc[i]['close'])
    print(test_df.iloc[i]['close_time'])
  elif int(predictions[i]) < int(test_df.iloc[i]['close'] - threshold):
    print('Sell at ', test_df.iloc[i].name)
    print(test_df.iloc[i]['close'])
    print(test_df.iloc[i]['close_time'])

#plt.plot(df['close_time'],df['close'])
plt.plot(test_df['close_time'],test_df['close'])
plt.show()
