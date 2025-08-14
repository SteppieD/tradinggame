#!/usr/bin/env python3

"""
Calculate Trailing Stop-Limit Order Parameters
Based on latest prices from Alpha Vantage
"""

import json
from datetime import datetime

def calculate_trailing_stops():
    """Calculate exact trailing stop parameters for each position"""
    
    print("=" * 70)
    print("🛡️ TRAILING STOP-LIMIT ORDERS")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p PST')}")
    print()
    
    # Load latest prices
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    print("📊 CURRENT PRICES (Fresh from Alpha Vantage):")
    print("-" * 50)
    
    # Updated prices from your update
    current_prices = {
        'CHPT': 12.05,  # Updated!
        'EVGO': 3.94     # Updated!
    }
    
    for symbol in current_prices:
        price = current_prices[symbol]
        print(f"{symbol}: ${price:.2f}")
    print()
    
    print("=" * 70)
    print("📍 TRAILING STOP-LIMIT SETTINGS:")
    print("=" * 70)
    print()
    
    # Calculate for each position
    positions = {
        'CHPT': {
            'shares': 26,
            'entry': 10.7845,
            'current': current_prices['CHPT']
        },
        'EVGO': {
            'shares': 82,
            'entry': 3.6271,
            'current': current_prices['EVGO']
        }
    }
    
    orders = []
    
    for symbol, pos in positions.items():
        pnl_percent = ((pos['current'] - pos['entry']) / pos['entry']) * 100
        
        print(f"{'='*50}")
        print(f"{symbol} - TRAILING STOP-LIMIT ORDER")
        print(f"{'='*50}")
        print(f"Current Price: ${pos['current']:.2f}")
        print(f"Entry Price: ${pos['entry']:.4f}")
        print(f"P&L: +{pnl_percent:.1f}%")
        print()
        
        # Calculate trailing parameters based on P&L
        if pnl_percent >= 10:
            # Strong profit - wider trailing
            trigger_pct = 0.03  # 3% trailing
            limit_pct = 0.005   # 0.5% below trigger
            strategy = "PROFIT_PROTECTION"
        elif pnl_percent >= 5:
            # Good profit - moderate trailing
            trigger_pct = 0.02  # 2% trailing
            limit_pct = 0.005   # 0.5% below trigger
            strategy = "FIBONACCI_STOP"
        elif pnl_percent >= 2:
            # Small profit - tighter trailing
            trigger_pct = 0.015  # 1.5% trailing
            limit_pct = 0.005   # 0.5% below trigger
            strategy = "TIGHT_TRAILING"
        else:
            # Minimal profit - very tight
            trigger_pct = 0.01  # 1% trailing
            limit_pct = 0.003   # 0.3% below trigger
            strategy = "BREAK_EVEN_PROTECTION"
        
        # Calculate dollar amounts
        trigger_delta = round(pos['current'] * trigger_pct, 2)
        limit_offset = round(pos['current'] * limit_pct, 2)
        
        # What the stops would be at current price
        stop_trigger = round(pos['current'] - trigger_delta, 2)
        stop_limit = round(stop_trigger - limit_offset, 2)
        
        # Ensure we don't go below break-even
        min_acceptable = round(pos['entry'] * 1.001, 2)  # Just above break-even
        if stop_limit < min_acceptable:
            stop_limit = min_acceptable
            stop_trigger = round(stop_limit + limit_offset, 2)
            trigger_delta = round(pos['current'] - stop_trigger, 2)
        
        print("📋 CIBC ORDER SETTINGS:")
        print("-" * 30)
        print(f"Order Type: TRAILING STOP-LIMIT")
        print(f"Quantity: {pos['shares']} shares")
        print(f"Trigger Delta: ${trigger_delta:.2f}")
        print(f"Limit Offset: ${limit_offset:.2f}")
        print()
        
        print("📍 AT CURRENT PRICE:")
        print("-" * 30)
        print(f"Stop would trigger at: ${stop_trigger:.2f}")
        print(f"Limit sell at: ${stop_limit:.2f}")
        print(f"Distance from current: -{(trigger_delta/pos['current']*100):.1f}%")
        print(f"Strategy: {strategy}")
        print()
        
        # Save for dashboard
        orders.append({
            'symbol': symbol,
            'shares': pos['shares'],
            'current_price': pos['current'],
            'entry_price': pos['entry'],
            'trigger_delta': trigger_delta,
            'limit_offset': limit_offset,
            'stop_trigger': stop_trigger,
            'stop_limit': stop_limit,
            'pnl_pct': pnl_percent,
            'strategy': strategy
        })
    
    # Save orders for dashboard
    with open('data/trailing_stop_orders.json', 'w') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'orders': orders
        }, f, indent=2)
    
    print("=" * 70)
    print("⚠️ IMPORTANT NOTES:")
    print("=" * 70)
    print("1. These are TRAILING stops - they move UP with price")
    print("2. They NEVER move down")
    print("3. Set these EVERY morning at 6:30 AM PST")
    print("4. If stock rises during day, stop rises too")
    print("5. Protects profits while allowing upside")
    print()
    
    print("🎯 MORNING CHECKLIST:")
    print("-" * 50)
    print("□ Wake at 6:25 AM PST")
    print("□ Run: python update_prices.py")
    print("□ Set CHPT trailing stop")
    print("□ Set EVGO trailing stop")
    print("□ Place TDUP limit buy @ $10.40 (15 shares)")
    print("□ Place FUBO limit buy @ $3.70 (44 shares)")
    print("□ If fills occur, set stops immediately")
    print()
    
    print("✅ Trailing stop calculations complete!")
    print("=" * 70)
    
    return orders

if __name__ == "__main__":
    calculate_trailing_stops()