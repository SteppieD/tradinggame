#!/usr/bin/env python3

"""
Manually update prices when API is delayed
"""

import json
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from smart_stops import get_stop_recommendations

# Manual price entry (update these with current prices)
MANUAL_PRICES = {
    'CHPT': 11.62,  # User reported current price
    'EVGO': 3.76,   # Keep API price or update if you have current
    'FCEL': 4.09,   # Keep API price or update if you have current
    'SPY': 642.69,
    'IWM': 226.81
}

def main():
    print("=" * 60)
    print("📊 MANUAL PRICE UPDATE")
    print("=" * 60)
    print(f"Update Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
    
    # Create price data in expected format
    prices = {}
    for symbol, price in MANUAL_PRICES.items():
        prices[symbol] = {
            'price': price,
            'change': 0,  # We don't have change data for manual entry
            'change_percent': '0',
            'timestamp': datetime.now().isoformat()
        }
        print(f"  {symbol}: ${price:.2f}")
    
    # Save prices
    with open('data/latest_prices.json', 'w') as f:
        json.dump(prices, f, indent=2)
    
    print("\n" + "=" * 60)
    print("📈 UPDATED POSITION ANALYSIS")
    print("=" * 60)
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Get smart stop recommendations
    positions = [p for p in portfolio['positions'] if p['symbol'] in ['CHPT', 'EVGO', 'FCEL']]
    stop_recommendations = get_stop_recommendations(positions, prices)
    
    total_value = portfolio['cash_balance']
    total_pnl = 0
    
    print("\n🎯 SMART STOP LOSS INSTRUCTIONS:\n")
    
    for rec in stop_recommendations:
        symbol = rec['symbol']
        
        # Calculate totals
        market_value = rec['quantity'] * rec['current_price']
        cost = rec['quantity'] * rec['entry_price']
        pnl = market_value - cost
        
        total_value += market_value
        total_pnl += pnl
        
        print(f"{symbol}:")
        print(f"  Current: ${rec['current_price']:.2f} (Entry: ${rec['entry_price']:.2f})")
        print(f"  P&L: ${pnl:.2f} ({rec['pnl_percent']:+.1f}%)")
        
        # Highlight significant changes
        if symbol == 'CHPT' and rec['pnl_percent'] >= 5:
            print(f"  🚀 NOW ABOVE 5% - ACTION REQUIRED!")
        
        print(f"  📍 STOP: ${rec['stop_price']} (Limit: ${rec['limit_price']})")
        print(f"     Strategy: {rec['strategy']}")
        print(f"     Distance: -{rec['distance_percent']}% from current")
        print()
    
    print("=" * 60)
    print(f"PORTFOLIO TOTAL: ${total_value:.2f}")
    print(f"TOTAL P&L: ${total_pnl:.2f} ({(total_pnl/970.67)*100:+.1f}%)")
    print("=" * 60)
    print("\n✅ Prices updated in data/latest_prices.json")
    print("📝 Now refresh dashboard.html to see updates\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allow command line price updates
        # Usage: python update_prices_manual.py CHPT=11.62 EVGO=3.80 FCEL=4.15
        for arg in sys.argv[1:]:
            if '=' in arg:
                symbol, price = arg.split('=')
                MANUAL_PRICES[symbol] = float(price)
    
    main()