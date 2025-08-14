#!/usr/bin/env python3

"""
Calculate Exact Stop Orders Based on Current Prices
Ready to place at 7:00 AM PST (10:00 AM EST)
"""

from datetime import datetime

def calculate_exact_stops():
    """Calculate exact stop parameters based on current prices"""
    
    print("=" * 70)
    print("🎯 EXACT STOP ORDERS TO PLACE NOW")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print("Market has been open for 37 minutes - volatility settling")
    print()
    
    # Current prices from Alpha Vantage
    positions = {
        'CHPT': {
            'shares': 26,
            'entry': 10.7845,
            'current': 12.05,
            'pnl_pct': 11.7
        },
        'EVGO': {
            'shares': 82,
            'entry': 3.6271,
            'current': 3.94,
            'pnl_pct': 8.6
        },
        'TDUP': {
            'shares': 19,
            'entry': 10.45,
            'current': 10.51,
            'pnl_pct': 0.6
        },
        'FUBO': {
            'shares': 55,
            'entry': 3.67,
            'current': 3.76,
            'pnl_pct': 2.5
        }
    }
    
    print("📊 CURRENT PRICES & P&L:")
    print("-" * 50)
    for symbol, data in positions.items():
        print(f"{symbol}: ${data['current']:.2f} ({'+' if data['pnl_pct'] >= 0 else ''}{data['pnl_pct']:.1f}% from entry)")
    print()
    
    print("=" * 70)
    print("📝 STOP ORDERS TO PLACE NOW:")
    print("=" * 70)
    print()
    
    # Calculate stops based on strategy
    orders = []
    
    # CHPT - Profitable, use trailing
    print("1️⃣ CHPT - TRAILING STOP-LIMIT")
    print("-" * 50)
    chpt_trigger = 0.30  # Tightened after morning
    chpt_limit_offset = 0.05
    print(f"Order Type: Trailing Stop-Limit")
    print(f"Quantity: 26 shares")
    print(f"Trigger Delta: ${chpt_trigger:.2f}")
    print(f"Limit Offset: ${chpt_limit_offset:.2f}")
    print(f"Current Stop Level: ${12.05 - chpt_trigger:.2f}")
    print(f"Would sell at: ${12.05 - chpt_trigger - chpt_limit_offset:.2f}")
    print()
    
    # EVGO - Profitable, use trailing  
    print("2️⃣ EVGO - TRAILING STOP-LIMIT")
    print("-" * 50)
    evgo_trigger = 0.08  # Tightened after morning
    evgo_limit_offset = 0.02
    print(f"Order Type: Trailing Stop-Limit")
    print(f"Quantity: 82 shares")
    print(f"Trigger Delta: ${evgo_trigger:.2f}")
    print(f"Limit Offset: ${evgo_limit_offset:.2f}")
    print(f"Current Stop Level: ${3.94 - evgo_trigger:.2f}")
    print(f"Would sell at: ${3.94 - evgo_trigger - evgo_limit_offset:.2f}")
    print()
    
    # TDUP - Small gain, use fixed for now
    print("3️⃣ TDUP - STOP-LIMIT (FIXED)")
    print("-" * 50)
    tdup_stop = round(10.45 * 0.92, 2)  # 8% below entry
    tdup_limit = tdup_stop - 0.02
    print(f"Order Type: Stop-Limit")
    print(f"Quantity: 19 shares")
    print(f"Stop Price: ${tdup_stop:.2f}")
    print(f"Limit Price: ${tdup_limit:.2f}")
    print(f"Risk from entry: -8%")
    print(f"Note: Convert to trailing when it hits +3%")
    print()
    
    # FUBO - Small gain, use wider fixed due to volatility
    print("4️⃣ FUBO - STOP-LIMIT (FIXED)")
    print("-" * 50)
    fubo_stop = round(3.67 * 0.88, 2)  # 12% below entry (wider for volatility)
    fubo_limit = fubo_stop - 0.02
    print(f"Order Type: Stop-Limit")
    print(f"Quantity: 55 shares")
    print(f"Stop Price: ${fubo_stop:.2f}")
    print(f"Limit Price: ${fubo_limit:.2f}")
    print(f"Risk from entry: -12%")
    print(f"Note: Wider stop due to high volatility")
    print()
    
    # Portfolio summary
    print("=" * 70)
    print("💼 PORTFOLIO SUMMARY:")
    print("=" * 70)
    
    total_value = sum(pos['shares'] * pos['current'] for pos in positions.values())
    print(f"Total Position Value: ${total_value:.2f}")
    print(f"Cash: $0.45")
    print(f"Total Portfolio: ${total_value + 0.45:.2f}")
    
    # Calculate total risk
    print()
    print("📊 RISK ANALYSIS:")
    print("-" * 50)
    
    risks = {
        'CHPT': 26 * chpt_trigger,
        'EVGO': 82 * evgo_trigger,
        'TDUP': 19 * (10.45 - tdup_stop),
        'FUBO': 55 * (3.67 - fubo_stop)
    }
    
    total_risk = sum(risks.values())
    
    for symbol, risk in risks.items():
        print(f"{symbol} Risk: ${risk:.2f}")
    
    print(f"Total Risk if all stops hit: ${total_risk:.2f}")
    print(f"Risk as % of portfolio: {(total_risk/total_value)*100:.1f}%")
    print()
    
    print("=" * 70)
    print("✅ ACTION ITEMS:")
    print("=" * 70)
    print("1. Place all 4 stop orders NOW")
    print("2. CHPT & EVGO: Use trailing stops")
    print("3. TDUP & FUBO: Use fixed stops")
    print("4. Monitor TDUP/FUBO - convert to trailing at +3%")
    print("5. All stops are GTC (Good Till Cancelled)")
    print()
    
    print("🎯 STRATEGY NOTES:")
    print("-" * 50)
    print("• Morning volatility has settled (37 min after open)")
    print("• TDUP showing small gain (+0.6%) - good entry")
    print("• FUBO showing gain (+2.5%) - almost ready for trailing")
    print("• CHPT & EVGO strong (+11.7% and +8.6%)")
    print("• Total portfolio up ~5% from initial $1000")
    print("=" * 70)

if __name__ == "__main__":
    calculate_exact_stops()