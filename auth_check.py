import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from kalshi_python import Configuration, KalshiClient
import config

print("Attempting to connect with the new Sync library...")

# 1. Setup Configuration
conf = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")

# Set properties directly from our new secure config
conf.api_key_id = config.KEY_ID
conf.private_key_pem = config.PRIVATE_KEY

# 2. Initialize Client and Test
try:
    client = KalshiClient(conf)
    balance = client.get_balance()
    
    print("SUCCESS! Everything is properly aligned.")
    print(f"Current Balance: ${balance.balance / 100:.2f}")

except Exception as e:
    print(f"Still an issue. Error: {e}")