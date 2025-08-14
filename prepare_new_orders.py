#!/usr/bin/env python3

"""
Prepare New Buy Orders - Option 1 ($350 Total)
Calculate exact shares and limit prices
"""

import json
from datetime import datetime

def prepare_orders():
    """Calculate exact order details for new positions"""
    
    print("=" * 70)
    print("📋 NEW BUY ORDERS - OPTION 1")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print("Budget: $350 total ($175 each position)")
    print()
    
    # Current prices from Alpha Vantage
    tdup_current = 10.51
    fubo_current = 3.77
    
    # Commission per trade
    commission = 6.95
    
    # Calculate for TDUP
    tdup_budget = 175.00
    tdup_available = tdup_budget - commission
    tdup_shares = int(tdup_available / tdup_current)
    tdup_limit = round(tdup_current - 0.11, 2)  # Slightly below current
    tdup_cost = (tdup_shares * tdup_limit) + commission
    
    print("1️⃣ TDUP (ThredUp Inc.)")
    print("-" * 50)
    print(f"Current Price: ${tdup_current:.2f}")
    print(f"Limit Order: ${tdup_limit:.2f}")
    print(f"Shares: {tdup_shares}")
    print(f"Order Cost: ${tdup_shares * tdup_limit:.2f}")
    print(f"With Commission: ${tdup_cost:.2f}")
    print(f"Strategy: Recent earnings beat, secondhand market leader")
    print()
    
    # Calculate for FUBO
    fubo_budget = 175.00
    fubo_available = fubo_budget - commission
    fubo_shares = int(fubo_available / fubo_current)
    fubo_limit = round(fubo_current - 0.07, 2)  # Slightly below current
    fubo_cost = (fubo_shares * fubo_limit) + commission
    
    print("2️⃣ FUBO (fuboTV Inc.)")
    print("-" * 50)
    print(f"Current Price: ${fubo_current:.2f}")
    print(f"Limit Order: ${fubo_limit:.2f}")
    print(f"Shares: {fubo_shares}")
    print(f"Order Cost: ${fubo_shares * fubo_limit:.2f}")
    print(f"With Commission: ${fubo_cost:.2f}")
    print(f"Strategy: First EBITDA positive, streaming consolidation play")
    print()
    
    # Total investment
    total_investment = tdup_cost + fubo_cost
    
    print("=" * 50)
    print("💰 TOTAL INVESTMENT:")
    print("-" * 50)
    print(f"TDUP: ${tdup_cost:.2f}")
    print(f"FUBO: ${fubo_cost:.2f}")
    print(f"Total: ${total_investment:.2f}")
    print()
    
    # Cash remaining
    current_cash = 414.75
    cash_after = current_cash - total_investment
    
    print("📊 CASH POSITION:")
    print("-" * 50)
    print(f"Current Cash: ${current_cash:.2f}")
    print(f"Investment: -${total_investment:.2f}")
    print(f"Remaining: ${cash_after:.2f}")
    print()
    
    # Stop loss planning
    print("🛡️ STOP LOSS PLAN (If Orders Fill):")
    print("-" * 50)
    
    tdup_stop = round(tdup_limit * 0.92, 2)  # 8% stop
    fubo_stop = round(fubo_limit * 0.90, 2)  # 10% stop (more volatile)
    
    print(f"TDUP Stop: ${tdup_stop:.2f} (-8% from entry)")
    print(f"FUBO Stop: ${fubo_stop:.2f} (-10% from entry)")
    print("Set these IMMEDIATELY after fills!")
    print()
    
    # Save order details
    orders = {
        "generated": datetime.now().isoformat(),
        "budget": 350.00,
        "orders": [
            {
                "symbol": "TDUP",
                "current_price": tdup_current,
                "limit_price": tdup_limit,
                "shares": tdup_shares,
                "order_cost": tdup_shares * tdup_limit,
                "total_with_commission": tdup_cost,
                "stop_loss": tdup_stop,
                "target": 13.00
            },
            {
                "symbol": "FUBO",
                "current_price": fubo_current,
                "limit_price": fubo_limit,
                "shares": fubo_shares,
                "order_cost": fubo_shares * fubo_limit,
                "total_with_commission": fubo_cost,
                "stop_loss": fubo_stop,
                "target": 5.00
            }
        ],
        "total_investment": total_investment,
        "cash_remaining": cash_after
    }
    
    with open('data/pending_orders.json', 'w') as f:
        json.dump(orders, f, indent=2)
    
    print("=" * 70)
    print("📱 CIBC ORDER INSTRUCTIONS:")
    print("=" * 70)
    print("\nTomorrow Morning at 6:30 AM PST:")
    print()
    print("1. TDUP - BUY LIMIT ORDER")
    print(f"   Quantity: {tdup_shares} shares")
    print(f"   Limit Price: ${tdup_limit:.2f}")
    print(f"   Duration: DAY")
    print()
    print("2. FUBO - BUY LIMIT ORDER")
    print(f"   Quantity: {fubo_shares} shares")
    print(f"   Limit Price: ${fubo_limit:.2f}")
    print(f"   Duration: DAY")
    print()
    print("3. IF ORDERS FILL:")
    print(f"   Set TDUP stop at ${tdup_stop:.2f}")
    print(f"   Set FUBO stop at ${fubo_stop:.2f}")
    print()
    print("✅ Orders prepared and saved!")
    print("=" * 70)
    
    return orders

if __name__ == "__main__":
    prepare_orders()