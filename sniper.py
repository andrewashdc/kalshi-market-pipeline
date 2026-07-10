import os
import time
import requests
import ast
import ssl
import certifi
from datetime import datetime

# --- NUCLEAR SSL FIX (Crucial for Mac) ---
# This forces Python to trust the connection, bypassing the SSL error you saw earlier.
os.environ['SSL_CERT_FILE'] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

# Try to import Kalshi
try:
    from kalshi_python import KalshiClient, Configuration
except ImportError:
    print("❌ ERROR: kalshi-python not installed. Run the setup script.")
    exit()

# --- CONFIGURATION ---
# I have pre-filled your Key ID based on your previous logs to save you time.
DEFAULT_KEY_ID = "556d4bd1-575f-4786-bef7-97e9c70971a3" 
DEFAULT_KEY_FILE_PATH = "AndrewAsh_Edge_hunter.txt"

def get_polymarket_price(query_term):
    """Checks Polymarket for a price discrepancy."""
    try:
        url = f"https://gamma-api.polymarket.com/events?q={query_term}&limit=1"
        response = requests.get(url).json()
        if response and len(response) > 0:
            market = response[0]['markets'][0]
            outcome_prices = ast.literal_eval(market['outcomePrices']) 
            return float(outcome_prices[0]), market['question']
    except:
        pass
    return None, None

def main():
    print("\n⚡ KALSHI MARKET SNIPER ⚡")
    print("----------------------------")

    # 1. AUTHENTICATION
    key_id = DEFAULT_KEY_ID
    key_path = DEFAULT_KEY_FILE_PATH
    
    # Auto-find the key file if it's in the current folder
    if not os.path.exists(key_path):
        key_path = input(f"Key file '{key_path}' not found. Enter full path: ").strip()

    try:
        with open(key_path, "r") as f:
            private_key = f.read()
        
        # --- CONFIGURATION FIX ---
        config = Configuration()
        # The error explicitly told us to use this host:
        config.host = "https://api.elections.kalshi.com/trade-api/v2"
        config.api_key_id = key_id
        config.private_key_pem = private_key

        client = KalshiClient(config)
        
        # Test Connection
        balance_resp = client.get_balance()
        print(f"✅ CONNECTED. Balance: ${balance_resp.balance / 100:,.2f}")
        
    except Exception as e:
        print(f"❌ AUTH FAILED: {e}")
        return

    # 2. SCANNING
    print("\n🔍 Scanning Markets for Edge...")
    try:
        # Fetch active markets
        markets_resp = client.get_markets(limit=100, status='open')
        markets = markets_resp.markets
    except Exception as e:
        print(f"❌ Error fetching markets: {e}")
        return

    found_opportunities = 0
    print(f"\n{'MARKET':<40} | {'KALSHI':<8} | {'POLY':<8} | {'EDGE':<8}")
    print("-" * 75)

    for m in markets:
        # Filter: Economics & Politics
        # Note: Using DOT NOTATION (m.category) as required by new SDK
        if hasattr(m, 'category') and m.category in ['Economics', 'Politics']:
            ticker = m.ticker
            title = m.title
            
            # Get Price (Handle potential None values)
            kalshi_price = (m.yes_bid or 0) / 100.0
            
            if kalshi_price == 0: continue

            # Polymarket Check
            search_query = " ".join(title.split(" ")[:3])
            poly_price, poly_title = get_polymarket_price(search_query)

            if poly_price:
                edge = poly_price - kalshi_price
                if abs(edge) > 0.01:
                    found_opportunities += 1
                    color = "\033[92m" if edge > 0 else "\033[91m" 
                    reset = "\033[0m"
                    print(f"{title[:38]:<40} | {int(kalshi_price*100)}¢ | {int(poly_price*100)}¢ | {color}{edge*100:+.1f}%{reset}")

    if found_opportunities == 0:
        print("\nNo arbitrage opportunities >1% found right now.")

if __name__ == "__main__":
    main()