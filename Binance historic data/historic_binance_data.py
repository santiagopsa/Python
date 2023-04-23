import requests
import pandas as pd
import time

def get_all_historical_data(symbol, interval, start_time, end_time, filename):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 500
    }
    data = []
    end_time_constant=params["endTime"]
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve data: {response.text}")
        data += response.json()
        if len(response.json()) < 500:
            break
        params["startTime"] = data[-1][6] + 1
        print(end_time_constant-params["startTime"])
        time.sleep(0.1)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

start_time = int(time.mktime(time.strptime("01-01-2022", "%d-%m-%Y"))) * 1000
end_time = int(time.mktime(time.strptime("13-01-2023", "%d-%m-%Y"))) * 1000
get_all_historical_data("BTCUSDT", "1m", start_time, end_time, "btc_data_full.csv")



