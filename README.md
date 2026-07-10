# Kalshi Quantitative Trading System
A low-latency algorithmic execution engine for prediction market arbitrage.

## Overview
This Python-based trading pipeline interfaces with the Kalshi REST API to continuously scan event contracts, evaluate statistical thresholds, and execute "sniper" trades in real-time based on underlying S&P 500 movements.

## Architecture
* `scanner.py`: Ingests and sanitizes real-time market data.
* `sniper.py`: Evaluates data against mathematical thresholds and triggers execution.
* `config.py` / `.env`: Manages secure API authentication and environment variables.

## Setup & Execution
1. Clone the repository and navigate to the project directory.
2. Run `source run.sh` to initialize the virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Execute the scanner: `python scanner.py`