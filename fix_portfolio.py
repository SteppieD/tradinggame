#!/usr/bin/env python3

"""
Fix portfolio data - remove test positions and correct cash balance
"""

import json
from pathlib import Path

def main():
    base_path = Path(__file__).parent
    
    # Load portfolio
    with open(base_path / 'data' / 'portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Keep only real positions (CHPT, EVGO, FCEL)
    real_positions = [p for p in portfolio['positions'] if p['symbol'] in ['CHPT', 'EVGO', 'FCEL']]
    
    # Calculate correct cash balance
    # Starting with $1000, bought:
    # CHPT: 26 @ $10.7845 = $280.40 + $6.95 = $287.35
    # EVGO: 82 @ $3.6271 = $297.42 + $6.95 = $304.37
    # FCEL: 97 @ $4.05 = $392.85 + $6.95 = $399.80
    # Total spent: $991.52
    # Cash remaining: $1000 - $991.52 = $8.48
    
    correct_cash = 8.48
    
    # Update portfolio
    portfolio['positions'] = real_positions
    portfolio['cash_balance'] = correct_cash
    
    # Save corrected portfolio
    with open(base_path / 'data' / 'portfolio.json', 'w') as f:
        json.dump(portfolio, f, indent=2)
    
    print("Portfolio fixed!")
    print(f"Positions: {len(real_positions)}")
    print(f"Cash Balance: ${correct_cash:.2f}")
    
    # Calculate total value with current prices
    with open(base_path / 'data' / 'latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    position_value = sum(p['quantity'] * prices[p['symbol']]['price'] for p in real_positions if p['symbol'] in prices)
    total_value = correct_cash + position_value
    
    print(f"Position Value: ${position_value:.2f}")
    print(f"Total Portfolio Value: ${total_value:.2f}")

if __name__ == "__main__":
    main()