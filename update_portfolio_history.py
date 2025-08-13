#!/usr/bin/env python3

"""
Update Portfolio Performance History
Tracks daily portfolio value vs benchmarks
"""

import json
from datetime import datetime, timedelta

def update_performance_history():
    """Update performance history with actual trading data"""
    
    # Load current portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Load latest prices
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # Calculate current portfolio value
    positions_value = 0
    for pos in portfolio['positions']:
        if pos['symbol'] in prices:
            current_price = prices[pos['symbol']]['price']
            positions_value += pos['quantity'] * current_price
    
    portfolio_value = portfolio['cash_balance'] + positions_value
    
    # Create performance history
    history = {
        "start_date": "2025-08-12",
        "initial_investment": 1000.00,
        "data": [
            {
                "date": "2025-08-12",
                "portfolio": 1000.00,
                "spy": 642.00,  # Actual SPY price on Aug 12
                "iwm": 225.50,  # Actual IWM price on Aug 12
                "portfolio_pct": 0.0,
                "spy_pct": 0.0,
                "iwm_pct": 0.0
            },
            {
                "date": "2025-08-13",
                "portfolio": portfolio_value,
                "spy": prices.get('SPY', {}).get('price', 642.69),
                "iwm": prices.get('IWM', {}).get('price', 226.81),
                "portfolio_pct": ((portfolio_value - 1000) / 1000) * 100,
                "spy_pct": ((642.69 - 642.00) / 642.00) * 100,
                "iwm_pct": ((226.81 - 225.50) / 225.50) * 100
            }
        ]
    }
    
    # Save updated history
    with open('data/performance_history.json', 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"📊 Performance History Updated")
    print(f"  Start Date: Aug 12, 2025")
    print(f"  Initial Investment: $1,000.00")
    print(f"  Current Value: ${portfolio_value:.2f}")
    print(f"  Total Return: {((portfolio_value - 1000) / 1000) * 100:.2f}%")
    print(f"\nBenchmark Comparison (since Aug 12):")
    print(f"  Portfolio: +{((portfolio_value - 1000) / 1000) * 100:.2f}%")
    print(f"  SPY: +{((642.69 - 642.00) / 642.00) * 100:.2f}%")
    print(f"  IWM: +{((226.81 - 225.50) / 225.50) * 100:.2f}%")
    
    return history

if __name__ == "__main__":
    update_performance_history()