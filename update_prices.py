#!/usr/bin/env python3

"""
Update dashboard with latest stock prices
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from scripts.alpha_vantage_client import AlphaVantageClient
import json
from datetime import datetime

def main():
    client = AlphaVantageClient()
    
    # Get quotes for all our stocks
    symbols = ['CHPT', 'EVGO', 'FCEL', 'SPY', 'IWM']
    prices = {}
    
    print("Fetching latest prices...")
    
    for symbol in symbols:
        try:
            quote = client.get_quote(symbol)
            if quote:
                prices[symbol] = {
                    'price': float(quote.get('price', 0)),
                    'change': float(quote.get('change', 0)),
                    'change_percent': quote.get('change_percent', '0%'),
                    'timestamp': datetime.now().isoformat()
                }
                print(f'{symbol}: ${quote.get("price", "N/A")} ({quote.get("change_percent", "N/A")})')
        except Exception as e:
            print(f'Error getting {symbol}: {e}')
    
    # Save to a temp file for dashboard update
    with open('data/latest_prices.json', 'w') as f:
        json.dump(prices, f, indent=2)
    
    print("\nPrices saved to data/latest_prices.json")
    
    # Update portfolio tracker with new prices
    from scripts.portfolio_tracker import PortfolioTracker
    tracker = PortfolioTracker()
    
    # Update current prices for positions
    for position in tracker.portfolio.get('positions', []):
        symbol = position['symbol']
        if symbol in prices:
            current_price = prices[symbol]['price']
            print(f"\nUpdating {symbol} current price to ${current_price:.2f}")
    
    # Calculate portfolio value with new prices
    portfolio_value = tracker.portfolio['cash_balance']
    for position in tracker.portfolio.get('positions', []):
        if position['symbol'] in prices:
            portfolio_value += position['quantity'] * prices[position['symbol']]['price']
    
    print(f"\nUpdated Portfolio Value: ${portfolio_value:.2f}")
    
    # Calculate benchmark comparison
    from scripts.benchmark_tracker import BenchmarkTracker
    benchmark_tracker = BenchmarkTracker()
    
    if 'IWM' in prices and 'SPY' in prices:
        print("\nBenchmark Comparison:")
        print(f"IWM: ${prices['IWM']['price']:.2f} ({prices['IWM']['change_percent']})")
        print(f"SPY: ${prices['SPY']['price']:.2f} ({prices['SPY']['change_percent']})")

if __name__ == "__main__":
    main()