from kalshi_python import Configuration, KalshiClient
import config

conf = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
conf.api_key_id = config.KEY_ID
conf.private_key_pem = config.PRIVATE_KEY

client = KalshiClient(conf)

print("Fetching 5 active tickers directly from the API...")
response = client.get_markets(limit=5)

for market in response.markets:
    print(f"Ticker: {market.ticker}")