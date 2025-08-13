#!/usr/bin/env python3

"""
Calculate Stop-Limit Order Details for CIBC
Shows trigger delta and limit offset in both $ and %
"""

import json

def calculate_stop_details():
    """Calculate detailed stop order parameters"""
    
    # Load current prices
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Smart stop recommendations from our calculations
    stop_orders = [
        {
            'symbol': 'CHPT',
            'current': 11.62,
            'stop': 11.30,
            'limit': 11.24
        },
        {
            'symbol': 'EVGO', 
            'current': 4.045,
            'stop': 3.92,
            'limit': 3.90
        },
        {
            'symbol': 'FCEL',
            'current': 4.26,
            'stop': 4.18,
            'limit': 4.16
        }
    ]
    
    print("=" * 70)
    print("📊 STOP-LIMIT ORDER DETAILS FOR CIBC")
    print("=" * 70)
    print("\nTrigger Delta = How far below current price to trigger")
    print("Limit Offset = How far below stop price to set limit\n")
    print("-" * 70)
    
    for order in stop_orders:
        symbol = order['symbol']
        current = order['current']
        stop = order['stop']
        limit = order['limit']
        
        # Calculate trigger delta (current to stop)
        trigger_delta_dollars = current - stop
        trigger_delta_percent = (trigger_delta_dollars / current) * 100
        
        # Calculate limit offset (stop to limit)
        limit_offset_dollars = stop - limit
        limit_offset_percent = (limit_offset_dollars / stop) * 100
        
        # Get position details
        position = next((p for p in portfolio['positions'] if p['symbol'] == symbol), None)
        if position:
            entry = position['entry_price']
            qty = position['quantity']
            pnl_at_stop = (stop - entry) * qty
            pnl_pct_at_stop = ((stop - entry) / entry) * 100
        
        print(f"\n{symbol}:")
        print(f"  Current Price: ${current:.2f}")
        print(f"  Stop Price:    ${stop:.2f}")
        print(f"  Limit Price:   ${limit:.2f}")
        print()
        print(f"  📍 TRIGGER DELTA (Current → Stop):")
        print(f"     Dollar: -${trigger_delta_dollars:.2f}")
        print(f"     Percent: -{trigger_delta_percent:.1f}%")
        print()
        print(f"  📍 LIMIT OFFSET (Stop → Limit):")
        print(f"     Dollar: -${limit_offset_dollars:.2f}")
        print(f"     Percent: -{limit_offset_percent:.1f}%")
        print()
        print(f"  💰 PROFIT LOCKED IN AT STOP:")
        print(f"     P&L: ${pnl_at_stop:.2f}")
        print(f"     Return: {pnl_pct_at_stop:+.1f}%")
        print("  " + "-" * 40)
    
    print("\n" + "=" * 70)
    print("🎯 CIBC STOP-LIMIT ORDER SETUP:")
    print("=" * 70)
    print("\n1. Order Type: STOP LIMIT")
    print("2. Duration: DAY (not GTC)")
    print("3. For each stock, enter:")
    print("   - Stop Price (trigger)")
    print("   - Limit Price (execution)")
    print("\n📝 RECOMMENDED SETTINGS:")
    print("   - Use % if available for consistency")
    print("   - Round to nearest cent for dollar amounts")
    print("   - Set alerts for when stops trigger")
    print("\n")

if __name__ == "__main__":
    calculate_stop_details()