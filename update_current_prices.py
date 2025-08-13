#!/usr/bin/env python3

"""
Update Current Stock Prices
Based on web search results for August 13, 2025
"""

import json
from datetime import datetime

def update_prices():
    """Update latest prices based on web search"""
    
    # Current prices from web search (Aug 13, 2025)
    current_prices = {
        'CHPT': 10.90,  # Up from $10.50 close
        'EVGO': 3.49,   # As of Aug 6 close (most recent data)
        'FCEL': 6.08,   # Current trading price
        'SPY': 642.69,  # Current price
        'IWM': 229.80   # Current price up 1.32%
    }
    
    # Load portfolio for calculations
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Update prices file
    prices_data = {}
    for symbol, price in current_prices.items():
        prices_data[symbol] = {
            'price': price,
            'change': 0,  # Would need historical data
            'change_percent': '0',
            'timestamp': datetime.now().isoformat()
        }
    
    # Save updated prices
    with open('data/latest_prices.json', 'w') as f:
        json.dump(prices_data, f, indent=2)
    
    # Calculate portfolio performance
    print("=" * 60)
    print("📊 PORTFOLIO UPDATE - August 13, 2025")
    print("=" * 60)
    
    total_value = portfolio['cash_balance']
    total_cost = 0
    total_pnl = 0
    
    print("\n📈 Position Details:")
    print("-" * 40)
    
    for pos in portfolio['positions']:
        symbol = pos['symbol']
        qty = pos['quantity']
        entry = pos['entry_price']
        current = current_prices.get(symbol, entry)
        
        cost = qty * entry
        value = qty * current
        pnl = value - cost
        pnl_pct = (pnl / cost) * 100
        
        total_cost += cost
        total_value += value
        total_pnl += pnl
        
        emoji = "🚀" if pnl_pct >= 10 else "⭐" if pnl_pct >= 5 else "📍" if pnl_pct >= 0 else "⚠️"
        
        print(f"{emoji} {symbol}:")
        print(f"   Entry: ${entry:.4f} × {qty} = ${cost:.2f}")
        print(f"   Current: ${current:.2f} × {qty} = ${value:.2f}")
        print(f"   P&L: ${pnl:.2f} ({pnl_pct:+.2f}%)")
    
    print("\n💰 Portfolio Summary:")
    print("-" * 40)
    print(f"Initial Investment: $1,000.00")
    print(f"Total Position Cost: ${total_cost:.2f}")
    print(f"Cash Balance: ${portfolio['cash_balance']:.2f}")
    print(f"Portfolio Value: ${total_value:.2f}")
    print(f"Total P&L: ${total_pnl:.2f} ({(total_pnl/total_cost)*100:+.2f}%)")
    print(f"Net Return: ${total_value - 1000:.2f} ({((total_value - 1000)/1000)*100:+.2f}%)")
    
    # Fee impact
    fees = 20.85  # 3 trades at $6.95 each
    print(f"\n⚠️ Fees Impact: -${fees:.2f}")
    print(f"   Fees as % of profit: {(fees/total_pnl)*100:.1f}%")
    
    # Benchmark comparison
    spy_return = ((642.69 - 642.00) / 642.00) * 100  # From Aug 12
    iwm_return = ((229.80 - 225.50) / 225.50) * 100  # From Aug 12
    portfolio_return = ((total_value - 1000) / 1000) * 100
    
    print(f"\n📊 vs Benchmarks (since Aug 12):")
    print(f"   Portfolio: {portfolio_return:+.2f}%")
    print(f"   SPY: {spy_return:+.2f}% (Outperforming by {portfolio_return - spy_return:+.2f}%)")
    print(f"   IWM: {iwm_return:+.2f}% (Outperforming by {portfolio_return - iwm_return:+.2f}%)")
    
    print("=" * 60)
    
    return current_prices

if __name__ == "__main__":
    update_prices()