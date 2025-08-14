#!/usr/bin/env python3

"""
Check Current Order Status
Shows what orders need to be placed in the morning
"""

from datetime import datetime
import json

def check_order_status():
    """Check current status of orders and what needs to be done"""
    
    print("=" * 70)
    print("📋 ORDER STATUS CHECK")
    print("=" * 70)
    print(f"Current Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p PST')}")
    print()
    
    print("🚨 CRITICAL MORNING ACTIONS (6:30 AM PST):")
    print("-" * 50)
    print()
    
    print("1️⃣ STOP-LOSS ORDERS (Must Set Daily):")
    print()
    print("   CHPT - Trailing Stop-Limit:")
    print("     • Trigger Delta: $0.18")
    print("     • Limit Offset: $0.06")
    print("     • Current Stop: ~$10.90")
    print("     • P&L: +2.7%")
    print()
    print("   EVGO - Trailing Stop-Limit:")
    print("     • Trigger Delta: $0.08")
    print("     • Limit Offset: $0.02")
    print("     • Current Stop: ~$3.68")
    print("     • P&L: +3.7%")
    print()
    
    print("2️⃣ NEW BUY ORDERS (Cannot Place Until Market Opens):")
    print()
    print("   TDUP - Limit Buy Order:")
    print("     • Limit Price: $10.40")
    print("     • Quantity: 15 shares")
    print("     • Total Cost: $162.95")
    print("     • If fills, set stop at $9.57")
    print()
    print("   FUBO - Limit Buy Order:")
    print("     • Limit Price: $3.70")
    print("     • Quantity: 44 shares")
    print("     • Total Cost: $169.75")
    print("     • If fills, set stop at $3.33")
    print()
    
    print("=" * 70)
    print("⏰ TIMING REMINDER:")
    print("=" * 70)
    print()
    print("❌ CANNOT place orders now - CIBC requires market hours")
    print("✅ MUST wake at 6:25 AM PST")
    print("✅ Place all 4 orders at 6:30 AM sharp")
    print()
    
    print("SEQUENCE:")
    print("1. Run: python update_prices.py")
    print("2. Set CHPT & EVGO trailing stops")
    print("3. Place TDUP & FUBO limit buys")
    print("4. If buys fill, set stops immediately")
    print()
    
    # Check if we have fresh prices
    try:
        with open('data/latest_prices.json', 'r') as f:
            prices = json.load(f)
            if 'CHPT' in prices and 'timestamp' in prices['CHPT']:
                ts = datetime.fromisoformat(prices['CHPT']['timestamp'])
                age = datetime.now() - ts
                if age.total_seconds() > 900:  # 15 minutes
                    print("⚠️  PRICES ARE STALE - Update in morning!")
                else:
                    print("✅ Prices are fresh")
    except:
        print("⚠️  No price data - Run update_prices.py in morning")
    
    print("=" * 70)

if __name__ == "__main__":
    check_order_status()