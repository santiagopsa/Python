# Import necessary libraries
import numpy as np
import pandas as pd
import talib
import pickle
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Read the data from the file
df = pd.read_csv("btc_data_full.csv")

# Convert the timestamp columns to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

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
train_df = df[df.index < '2023-01-13']
test_df = df[df.index >= '2023-01-13']

# Check the number of rows in the dataframe
num_rows = df.shape[0]


# Check the names of the columns in the dataframe
column_names = df.columns

# Train a Random Forest Regressor model on the training data
model = RandomForestRegressor()
model.fit(train_df[features], train_df['close'])

# Save the model to a file
with open("model_2022_BTCUSDT.pkl", "wb") as file:
    pickle.dump(model, file)

'''
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
plt.plot(df['close_time'],df['close'])
print(df['close_time'][0])
plt.show()'''
