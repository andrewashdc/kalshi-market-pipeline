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

def get_live_ticker():
    # Find 1 open market
    response = client.get_markets(limit=1, status="open")
    return response.markets[0].ticker

def is_market_open(ticker):
    # Check the specific market's status
    market_response = client.get_market(ticker)
    return market_response.market.status == "open"

# Initial setup
current_ticker = get_live_ticker()
print(f"Tracking new live market: {current_ticker}")

last_status_check = time.time()
check_interval = 12 * 60 * 60  # 12 hours in seconds

while True:
    try:
        # --- 1. SCANNING LOGIC ---
        market_response = client.get_market(current_ticker)
        market_data = market_response.market
        
        if market_data.yes_bid:
            print(f"{current_ticker} Active Yes Bid: {market_data.yes_bid}")
        else:
            print(f"{current_ticker} Scanning... (No active Yes bids right now)")
        
        # --- 2. 12-HOUR REFRESH LOGIC ---
        if time.time() - last_status_check > check_interval:
            print("\n12 hours passed. Verifying market status...")
            
            if not is_market_open(current_ticker):
                print("Market closed. Finding a new live market...\n")
                current_ticker = get_live_ticker()
            else:
                print("Market still open. Keeping it.\n")
            
            last_status_check = time.time()
        
        # Standard loop delay so we don't hit rate limits
        time.sleep(5)

    except KeyboardInterrupt:
        print("\nScanner gracefully stopped.")
        break