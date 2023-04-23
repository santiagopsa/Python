import time
import ccxt
def bitcoin_ticker():
    # Initialize the Binance exchange object
    exchange = ccxt.binance()

    # Number of retries
    retries = 3

    # Delay between retries (in seconds)
    retry_delay = 5

    # Try to fetch ticker data
    for i in range(retries):
        try:
            return exchange.fetch_ticker('BTC/USDT')
            break
        except Exception as e:
            if i < retries - 1:
                print(f'Error: {e}. Retrying in {retry_delay} seconds.')
                time.sleep(retry_delay)
            else:
                print(f'Error: {e}. Maximum retries reached.')
                raise e