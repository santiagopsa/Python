import requests

# Set the symbol and endpoint URL
symbol = "BTCUSDT"
url = f"https://api.binance.com/api/v3/trades?symbol={symbol}"

# Send the GET request
response = requests.get(url)

# Print the response
info_actual = response.json()

print(info_actual[0]['price'])