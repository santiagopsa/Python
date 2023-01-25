import requests
import pickle
import pandas as pd
import talib
from datetime import datetime, timedelta
import ccxt
import get_current_bitcoin_price
import time
import keys
import matplotlib.pyplot as plt

# Set the API key and secret
api_key = keys.binance_api_key
api_secret = keys.binance_api_secret

# Load the model from the .pkl file
with open("model_2022_BTCUSDT.pkl", "rb") as file:
    model = pickle.load(file)

# Set a fake starting balance
print('Setting an initial balance of $ 10.000')
balance = 10000

print('*'*50)
# Set a risk factor to leave the trade compared to the prediction price
print('\nSetting a risk of 30% for defining sell price')
risk = 0.20

print('*'*50)
# Set a threshold for when to execute trades
print('\nSetting a threshold of 20 to execute trades')
threshold = 40

# set a variable to store the amount of bitcoin user have
btc_owned = 0

print('*' * 20)
# Setting the amount to spend per trade
print('\nSetting the amount to spend per trade')
amount_to_spend = 300
print('*' * 20)

#Getting a flag to know when there was a buy or sell transaction and for win/lost transactions
bsflag = 'no trade'


print('*'*50)
# Initialize an empty dataframe to store the values later to save in the CSV
results_df = pd.DataFrame(columns=['timestamp','btc_owed', 'balance', 'mae'])

# Initialize the exchange object
exchange = ccxt.binance({
    'rateLimit': 2000,
    'enableRateLimit': True,
})
print('\nAccesing Binance Exchange and setting a rate limit to 2000 to avoid blocking')
print('*' * 50)

while True:


    # Setting Win Loss flag within the loop
    wl = 'neutral'

    # Fetch ticker data for the BTC/USDT trading pair
    ticker=get_current_bitcoin_price.bitcoin_ticker()
    print('\nGetting current Bitcoin price')
    print('*' * 50)

    # Extract the last traded price from the ticker data
    btc_price = ticker['last']


    # Fetch the historical data
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '5m')
    print('Defining a 1h span for getting data')
    print('*' * 50)

    # Convert the data to a pandas dataframe
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate the indicators
    df['sma_5'] = talib.SMA(df['close'], timeperiod=5)
    df['sma_10'] = talib.SMA(df['close'], timeperiod=10)
    df['sma_20'] = talib.SMA(df['close'], timeperiod=20)
    df['sma_50'] = talib.SMA(df['close'], timeperiod=50)
    df['sma_200'] = talib.SMA(df['close'], timeperiod=200)
    df['rsi_14'] = talib.RSI(df['close'], timeperiod=14)
    df['willr_14'] = talib.WILLR(df['high'], df['low'], df['close'], timeperiod=14)
    df['adx_14'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    df['cci_14'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=14)
    macd, macd_signal, macd_hist = talib.MACD(df['close'])
    df['macd'] = macd
    df['macd_signal'] = macd_signal
    df['macd_hist'] = macd_hist
    df['atr_14'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
    upper, middle, lower = talib.BBANDS(df['close'])
    df['bollinger_upper'] = upper
    df['bollinger_middle'] = middle
    df['bollinger_lower'] = lower

    print('\nConverting data to indicators for bitcoin prediction')
    print('*' * 50)


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
    features = ['sma_5', 'sma_10', 'sma_20', 'sma_50', 'sma_200', 'rsi_14', 'willr_14', 'adx_14', 'cci_14', 'macd',
                'macd_signal', 'macd_hist', 'atr_14', 'bollinger_upper', 'bollinger_middle', 'bollinger_lower']



    # Use the model to make predictions on the real-time data
    predictions = model.predict(df[features])
    print('\nPredicting bitcoin price............')

    # Get the last prediction from the list
    last_prediction = predictions[-1]
    print(f'\nBitcoin prediction is ${round(last_prediction,2)} USD')
    print('*' * 20)

    # Get the actual price of Bitcoin
    btc_price = float(btc_price)

    # Calculate the absolute difference between the prediction and actual price
    absolute_error = abs(last_prediction - btc_price)

    # Calculate the mean absolute error
    mae = absolute_error / len(predictions)

    # Print the mean absolute error
    print("Mean Absolute Error: ", mae)
    prediction_difference = int(abs(last_prediction-float(btc_price)))
    percentage_error = (mae / float(btc_price)) * 100
    print(f'Current bitcoin price is: {int(btc_price)} and predicted value is: {int(last_prediction)}, the difference is {prediction_difference}')

    #make sure to buy if the prediction price is higher by a Threshold compared to the actual price
    if last_prediction > float(btc_price) and absolute_error > threshold:
        # Make a buy decision
        bsflag='buy'
        print(f'Getting into a trade with a prediction of {last_prediction} and a risk of {risk*100}%')
        # Set an expected sell price given a risk
        expected_sell = float(btc_price)+((abs(last_prediction-float(btc_price)))*risk)
        print(f'Leaving trade at {round(expected_sell,2)}')
        amount_bought = amount_to_spend / float(btc_price)
        btc_owned += amount_bought
        balance -= amount_to_spend
        print("Buy decision made. Bought {:.8f} BTC at {}. Current balance: $ {}".format(amount_bought, btc_price,
                                                                                         balance))
        print(f'Bitcoin Balance is: {btc_owned}')
        # Get current timestamp
        timestamp = datetime.now()

        # Create a new dataframe with the new data
        new_data = {
            'timestamp': timestamp,
            'bitcoin_owed': btc_owned,
            'bitcoin_price': float(ticker["last"]),
            'balance': balance,
            'mae': mae,
            'buy_sell_flag': bsflag,
            'Win_loss': wl
        }
        new_df = pd.DataFrame.from_records([new_data])

        # Concatenate the new dataframe with the existing dataframe
        results_df = pd.concat([results_df, new_df], ignore_index=True)

        # Save the results_df to a CSV file
        current_time = datetime.now().strftime("%Y_%m_%d")
        results_df.to_csv(f'results_{current_time}.csv', index=False)
        start_time = time.time()
        while True:
            # Fetch ticker data for the BTC/USDT trading pair
            ticker = get_current_bitcoin_price.bitcoin_ticker()
            print(f'Current price is {float(ticker["last"])} expected {expected_sell} or more')
            if ticker["last"] >= expected_sell:
                # Make a sell decision
                bsflag='sell'
                btc_owned -= amount_bought
                balance += float(ticker["last"]) * amount_bought
                wl = 'win'
                print("Sell decision made. Sold {:.8f} BTC at {}. Current balance: $ {}".format(
                    amount_bought, ticker["last"], balance))
                print(f'Bitcoin Balance is: {btc_owned}')
                # Get current timestamp
                timestamp = datetime.now()

                # Create a new dataframe with the new data
                new_data = {
                    'timestamp': timestamp,
                    'bitcoin_owed': btc_owned,
                    'bitcoin_price': float(ticker["last"]),
                    'balance': balance,
                    'mae': mae,
                    'buy_sell_flag': bsflag,
                    'Win_loss': wl
                }
                new_df = pd.DataFrame.from_records([new_data])

                # Concatenate the new dataframe with the existing dataframe
                results_df = pd.concat([results_df, new_df], ignore_index=True)

                # Save the results_df to a CSV file
                current_time = datetime.now().strftime("%Y_%m_%d")
                results_df.to_csv(f'results_{current_time}.csv', index=False)
                break
            elif time.time() - start_time >= 120:  # 5 minutes in seconds
                # Make a sell decision
                bsflag = 'sell'
                wl = 'lost'
                btc_owned -= amount_bought
                balance += float(ticker["last"]) * amount_bought
                print("Sell decision made. Sold {:.8f} BTC at {}. Current balance: $ {}".format(
                    amount_bought, ticker["last"], balance))
                print('Selling at loss, did not get to the expected price...... :(')
                # Get current timestamp
                timestamp = datetime.now()

                # Create a new dataframe with the new data
                new_data = {
                    'timestamp': timestamp,
                    'bitcoin_owed': btc_owned,
                    'bitcoin_price': float(ticker["last"]),
                    'balance': balance,
                    'mae': mae,
                    'buy_sell_flag': bsflag,
                    'Win_loss': wl
                }
                new_df = pd.DataFrame.from_records([new_data])

                # Concatenate the new dataframe with the existing dataframe
                results_df = pd.concat([results_df, new_df], ignore_index=True)

                # Save the results_df to a CSV file
                current_time = datetime.now().strftime("%Y_%m_%d")
                results_df.to_csv(f'results_{current_time}.csv', index=False)
                break

    elif last_prediction <= float(btc_price) and mae > 0.5:
        if amount_to_spend / float(btc_price) <= btc_owned:
            # Make a sell decision
            btc_owned -= amount_to_spend / float(btc_price)
            balance += amount_to_spend
            print("Sell decision made. Sold {:.8f} BTC at {}. Current balance: $ {}".format(
                amount_to_spend / float(btc_price), btc_price, balance))
            print(f'Bitcoin Balance is: {btc_owned}')
            # Get current timestamp
            timestamp = datetime.now()

            # Create a new dataframe with the new data
            new_data = {
                'timestamp': timestamp,
                'bitcoin_owed': btc_owned,
                'bitcoin_price': float(ticker["last"]),
                'balance': balance,
                'mae': mae,
                'buy_sell_flag': bsflag,
                'Win_loss': wl
            }
            new_df = pd.DataFrame.from_records([new_data])

            # Concatenate the new dataframe with the existing dataframe
            results_df = pd.concat([results_df, new_df], ignore_index=True)

            # Save the results_df to a CSV file
            current_time = datetime.now().strftime("%Y_%m_%d")
            results_df.to_csv(f'results_{current_time}.csv', index=False)

        else:
            print("You don't have enough bitcoin to sell.")
            print(f'Bitcoin Balance is: {btc_owned}')

    else:
        print(f"Difference of {round((prediction_difference/btc_price)*100,2)}% is too low, not executing the trade.")

