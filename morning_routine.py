#!/usr/bin/env python3

"""
Morning Trading Routine - Execute at 6:30 AM PST
Generates exact CIBC stop orders for the day
"""

import json
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from smart_stops import get_stop_recommendations

def morning_routine():
    """Generate morning trading plan and stop orders"""
    
    print("=" * 70)
    print("☕ GOOD MORNING - TRADING ROUTINE")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print("\n")
    
    # Load portfolio and prices
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    positions = [p for p in portfolio['positions'] if p['symbol'] in ['CHPT', 'EVGO', 'FCEL']]
    
    print("📋 MORNING CHECKLIST:")
    print("-" * 50)
    print("✓ 1. Check pre-market prices")
    print("✓ 2. Review overnight news")
    print("✓ 3. Set stop-loss orders (below)")
    print("✓ 4. Monitor first 30 minutes for volatility")
    print("\n")
    
    # Get stop recommendations
    stop_recommendations = get_stop_recommendations(positions, prices)
    
    print("🛡️ TODAY'S STOP-LOSS ORDERS:")
    print("-" * 50)
    print("⚠️  IMPORTANT: These expire at market close!")
    print("    Set these IMMEDIATELY at market open\n")
    
    for rec in stop_recommendations:
        symbol = rec['symbol']
        current = rec['current_price']
        stop = rec['stop_price']
        limit = rec['limit_price']
        qty = rec['quantity']
        pnl_pct = rec['pnl_percent']
        
        # Calculate CIBC parameters
        trigger_delta = round(current - stop, 2)
        limit_offset = round(stop - limit, 2)
        
        # Determine urgency
        if pnl_pct < 0:
            urgency = "🔴 URGENT - Protect Capital"
        elif pnl_pct < 5:
            urgency = "🟡 IMPORTANT - Lock in Gains"
        else:
            urgency = "🟢 PROFITABLE - Trail Winners"
        
        print(f"\n{symbol} - {urgency}")
        print(f"  Current Price: ${current:.2f}")
        print(f"  Position: {qty} shares")
        print(f"  P&L: {pnl_pct:+.2f}%")
        print(f"  ")
        print(f"  📱 CIBC SETTINGS:")
        print(f"     Order Type: TRAILING STOP LIMIT")
        print(f"     Duration: DAY")
        print(f"     Trigger Delta: ${trigger_delta:.2f}")
        print(f"     Limit Offset: ${limit_offset:.2f}")
        print(f"  ")
        print(f"  This will:")
        print(f"     - Trigger at: ${stop:.2f}")
        print(f"     - Sell with limit: ${limit:.2f}")
        print("-" * 30)
    
    # Market analysis
    print("\n📊 MARKET CONDITIONS:")
    print("-" * 50)
    
    spy_price = prices.get('SPY', {}).get('price', 0)
    iwm_price = prices.get('IWM', {}).get('price', 0)
    
    print(f"SPY: ${spy_price:.2f}")
    print(f"IWM: ${iwm_price:.2f}")
    
    # Risk assessment
    total_value = portfolio['cash_balance']
    for pos in positions:
        if pos['symbol'] in prices:
            total_value += pos['quantity'] * prices[pos['symbol']]['price']
    
    at_risk = total_value - portfolio['cash_balance']
    risk_pct = (at_risk / total_value) * 100
    
    print(f"\nPortfolio Value: ${total_value:.2f}")
    print(f"Cash Available: ${portfolio['cash_balance']:.2f}")
    print(f"At Risk: ${at_risk:.2f} ({risk_pct:.1f}% of portfolio)")
    
    # Action items
    print("\n" + "=" * 70)
    print("📌 ACTION ITEMS:")
    print("=" * 70)
    print("1. ⏰ SET STOP ORDERS IMMEDIATELY (6:30 AM PST)")
    print("2. 📱 Use CIBC Investor's Edge app")
    print("3. 🔄 Orders expire at 4:00 PM ET - must reset daily")
    print("4. 📊 Check dashboard throughout the day")
    print("5. 💡 If stops trigger, wait for next setup")
    print("\n✅ Good luck today! Stick to the plan.")
    print("=" * 70)
    
    # Save morning plan
    morning_plan = {
        'date': datetime.now().isoformat(),
        'stop_orders': stop_recommendations,
        'portfolio_value': total_value,
        'at_risk': at_risk,
        'risk_percent': risk_pct
    }
    
    with open('data/morning_plan.json', 'w') as f:
        json.dump(morning_plan, f, indent=2)
    
    return morning_plan

if __name__ == "__main__":
    morning_routine()