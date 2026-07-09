import time
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from kalshi_python import Configuration, KalshiClient
import config

# 1. Connect using your working auth logic
conf = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
conf.api_key_id = config.KEY_ID
conf.private_key_pem = config.PRIVATE_KEY
client = KalshiClient(conf)

# 2. List the Tickers you want to watch
WATCHLIST = ['KXMVESPORTSMULTIGAMEEXTENDED-S20266A70F1D57FE-4359ED59184'] 

print(f"--- LIVE MARKET SCANNER ---")
print("Press Ctrl+C to stop scanning.\n")

# Wrap the scanner in an infinite loop
while True:
    for ticker in WATCHLIST:
        try:
            # Get the specific market data
            market = client.get_market(ticker)
            title = market.market.title
            
            # Check if there is an active bid before doing math
            if market.market.yes_bid is not None:
                price = market.market.yes_bid / 100
                print(f"{ticker}: ${price:.2f} | {title}")
            else:
                print(f"{ticker}: No active bids | {title}")
                
        except Exception as e:
            print(f"Could not find {ticker}. Error: {e}")
            
    # Pause for 5 seconds before scanning again so Kalshi doesn't block you
    time.sleep(5)