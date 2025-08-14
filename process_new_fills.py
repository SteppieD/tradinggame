#!/usr/bin/env python3

"""
Process New Order Fills - TDUP and FUBO
Update portfolio with actual execution prices
"""

import json
from datetime import datetime

def process_new_fills():
    """Process the filled orders for TDUP and FUBO"""
    
    print("=" * 70)
    print("🎉 ORDER FILLS CONFIRMED!")
    print("=" * 70)
    print(f"Processing Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p PST')}")
    print()
    
    # Actual fills from user
    fills = [
        {
            'symbol': 'TDUP',
            'shares': 19,
            'price': 10.45,
            'time': 'Aug 14 9:25am',
            'commission': 6.95
        },
        {
            'symbol': 'FUBO',
            'shares': 55,
            'price': 3.67,
            'time': 'Aug 14 9:34am',
            'commission': 6.95
        }
    ]
    
    print("✅ EXECUTED TRADES:")
    print("-" * 50)
    
    total_invested = 0
    
    for fill in fills:
        cost = fill['shares'] * fill['price']
        total_with_fee = cost + fill['commission']
        total_invested += total_with_fee
        
        print(f"\n{fill['symbol']}:")
        print(f"  Shares: {fill['shares']}")
        print(f"  Fill Price: ${fill['price']:.2f}")
        print(f"  Order Cost: ${cost:.2f}")
        print(f"  Commission: ${fill['commission']:.2f}")
        print(f"  Total Cost: ${total_with_fee:.2f}")
        print(f"  Executed: {fill['time']}")
    
    print()
    print("-" * 50)
    print(f"TOTAL INVESTED: ${total_invested:.2f}")
    print()
    
    # Load current portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Calculate cash after purchases
    cash_before = portfolio['cash_balance']
    cash_after = cash_before - total_invested
    
    print("💰 CASH UPDATE:")
    print("-" * 50)
    print(f"Cash Before: ${cash_before:.2f}")
    print(f"Investment: -${total_invested:.2f}")
    print(f"Cash After: ${cash_after:.2f}")
    print()
    
    # Add new positions to portfolio
    new_positions = [
        {
            'symbol': 'TDUP',
            'quantity': 19,
            'entry_price': 10.45,
            'entry_date': '2025-08-14',
            'entry_time': '09:25:00'
        },
        {
            'symbol': 'FUBO',
            'quantity': 55,
            'entry_price': 3.67,
            'entry_date': '2025-08-14',
            'entry_time': '09:34:00'
        }
    ]
    
    # Update portfolio
    portfolio['positions'].extend(new_positions)
    portfolio['cash_balance'] = cash_after
    portfolio['last_updated'] = datetime.now().isoformat()
    
    # Save updated portfolio
    with open('data/portfolio.json', 'w') as f:
        json.dump(portfolio, f, indent=2)
    
    print("📊 UPDATED PORTFOLIO:")
    print("-" * 50)
    print("Active Positions:")
    for pos in portfolio['positions']:
        print(f"  {pos['symbol']}: {pos['quantity']} shares @ ${pos['entry_price']:.4f}")
    print(f"\nCash Balance: ${portfolio['cash_balance']:.2f}")
    print()
    
    # Calculate stop losses
    print("=" * 70)
    print("🛡️ SET THESE STOP LOSSES IMMEDIATELY:")
    print("=" * 70)
    print()
    
    stops = {
        'TDUP': {
            'entry': 10.45,
            'stop_percent': 0.08,  # 8% stop
            'shares': 19
        },
        'FUBO': {
            'entry': 3.67,
            'stop_percent': 0.10,  # 10% stop (more volatile)
            'shares': 55
        }
    }
    
    for symbol, data in stops.items():
        stop_price = round(data['entry'] * (1 - data['stop_percent']), 2)
        risk = (data['entry'] - stop_price) * data['shares']
        
        print(f"{symbol} STOP-LOSS ORDER:")
        print(f"  Type: Stop-Limit")
        print(f"  Quantity: {data['shares']} shares")
        print(f"  Stop Price: ${stop_price:.2f}")
        print(f"  Limit Price: ${stop_price - 0.02:.2f}")
        print(f"  Risk: ${risk:.2f} (-{data['stop_percent']*100:.0f}%)")
        print()
    
    print("=" * 70)
    print("📈 POSITION TARGETS:")
    print("=" * 70)
    print()
    
    targets = {
        'TDUP': {'target': 13.00, 'entry': 10.45},
        'FUBO': {'target': 5.00, 'entry': 3.67}
    }
    
    for symbol, data in targets.items():
        upside = ((data['target'] - data['entry']) / data['entry']) * 100
        print(f"{symbol}:")
        print(f"  Entry: ${data['entry']:.2f}")
        print(f"  Target: ${data['target']:.2f}")
        print(f"  Upside: +{upside:.1f}%")
        print()
    
    print("=" * 70)
    print("✅ NEXT STEPS:")
    print("=" * 70)
    print("1. ⚠️ SET STOP LOSSES NOW for TDUP and FUBO")
    print("2. Update/tighten stops for CHPT and EVGO after 7:00 AM")
    print("3. Monitor all positions throughout the day")
    print("4. Dashboard will auto-update with new positions")
    print()
    
    print("🎯 Portfolio now has 4 positions: CHPT, EVGO, TDUP, FUBO")
    print("=" * 70)

if __name__ == "__main__":
    process_new_fills()