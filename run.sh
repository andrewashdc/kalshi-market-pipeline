#!/bin/bash

# 1. Create a virtual environment named 'venv' if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate the environment
source venv/bin/activate

# 3. Install libraries explicitly into THIS environment
echo "Installing dependencies..."
pip install kalshi-python requests

# 4. Run the Sniper
echo "Launching Sniper..."
./venv/bin/python sniper.py