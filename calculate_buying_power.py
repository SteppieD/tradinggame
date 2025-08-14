#!/usr/bin/env python3

"""
Calculate Exact Buying Power for New Positions
Based on actual cash and realized gains only
"""

import json
from datetime import datetime

def calculate_buying_power():
    """Calculate what we can actually spend"""
    
    print("=" * 70)
    print("💰 BUYING POWER CALCULATION")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print()
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Initial investment
    initial_investment = 1000.00
    
    # Current cash
    current_cash = portfolio['cash_balance']
    
    # Fees paid so far
    total_fees_paid = 6.95 * 4  # 3 buys + 1 sell
    
    # Calculate what portion of cash is original vs profit
    print("📊 CASH BREAKDOWN:")
    print("-" * 50)
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Fees Paid (4 trades): -${total_fees_paid:.2f}")
    print(f"Current Cash: ${current_cash:.2f}")
    print()
    
    # FCEL trade details
    fcel_entry = 97 * 4.05  # $392.85
    fcel_exit = 97 * 4.26   # $413.22
    fcel_gross_profit = fcel_exit - fcel_entry  # $20.37
    fcel_commission = 6.95
    fcel_net_profit = fcel_gross_profit - fcel_commission  # $13.42
    
    print("🏆 REALIZED GAINS:")
    print("-" * 50)
    print(f"FCEL Sale:")
    print(f"  Gross Profit: ${fcel_gross_profit:.2f}")
    print(f"  Commission: -${fcel_commission:.2f}")
    print(f"  Net Profit: ${fcel_net_profit:.2f}")
    print()
    
    # Calculate position values
    print("📈 CURRENT POSITIONS:")
    print("-" * 50)
    
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    positions_value = 0
    for pos in portfolio['positions']:
        symbol = pos['symbol']
        qty = pos['quantity']
        entry = pos['entry_price']
        current = prices[symbol]['price']
        value = qty * current
        positions_value += value
        print(f"{symbol}: {qty} shares @ ${current:.2f} = ${value:.2f}")
    
    print(f"Total Positions Value: ${positions_value:.2f}")
    print()
    
    # Total portfolio calculation
    total_portfolio = current_cash + positions_value
    net_gain = total_portfolio - initial_investment
    
    print("💼 PORTFOLIO SUMMARY:")
    print("-" * 50)
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Current Portfolio Value: ${total_portfolio:.2f}")
    print(f"Net Gain/Loss: ${net_gain:.2f}")
    print()
    
    # BUYING POWER OPTIONS
    print("=" * 70)
    print("🎯 BUYING POWER OPTIONS:")
    print("=" * 70)
    print()
    
    print("OPTION 1: Use All Available Cash")
    print("-" * 50)
    print(f"  Available: ${current_cash:.2f}")
    print(f"  Less reserves for fees (2 trades): -${6.95 * 2:.2f}")
    print(f"  Buying Power: ${current_cash - 13.90:.2f}")
    print()
    
    print("OPTION 2: Use Only Profits (Conservative)")
    print("-" * 50)
    if net_gain > 0:
        print(f"  Net Profits: ${net_gain:.2f}")
        print(f"  Less future fees: -${6.95 * 2:.2f}")
        usable_profit = max(0, net_gain - 13.90)
        print(f"  Buying Power: ${usable_profit:.2f}")
        print("  ⚠️ This would keep original $1000 intact")
    else:
        print("  No net profits to reinvest")
    print()
    
    print("OPTION 3: Balanced Approach (Recommended)")
    print("-" * 50)
    # Use cash but maintain minimum reserve
    minimum_reserve = 50.00  # Keep some cash for opportunities
    available_for_trading = current_cash - minimum_reserve - 13.90  # Less fees
    print(f"  Current Cash: ${current_cash:.2f}")
    print(f"  Keep Reserve: -${minimum_reserve:.2f}")
    print(f"  Keep for Fees: -${13.90:.2f}")
    print(f"  Buying Power: ${available_for_trading:.2f}")
    print()
    
    # RECOMMENDATION
    print("=" * 70)
    print("📌 RECOMMENDATION:")
    print("=" * 70)
    
    recommended_amount = min(350, current_cash - 13.90)
    
    print(f"\nUse ${recommended_amount:.2f} for new positions:")
    print(f"  • TDUP: ~$175 (about 16-17 shares)")
    print(f"  • FUBO: ~$175 (about 46-47 shares)")
    print(f"  • Keep ${current_cash - recommended_amount:.2f} as reserve")
    print()
    print("WHY THIS AMOUNT?")
    print("  ✓ Maintains diversification")
    print("  ✓ Leaves cash for opportunities")
    print("  ✓ Covers trading fees")
    print("  ✓ Not overextending on new positions")
    print()
    
    print("CURRENT REALITY CHECK:")
    if net_gain > 0:
        print(f"  ✅ You're up ${net_gain:.2f} overall")
        print(f"  ✅ FCEL profit: ${fcel_net_profit:.2f}")
        print(f"  ✅ Can afford new positions with profit alone")
    else:
        print(f"  ⚠️ You're down ${abs(net_gain):.2f} overall")
        print(f"  ✅ But FCEL profit: ${fcel_net_profit:.2f}")
        print(f"  ⚠️ New positions would use original capital")
    
    print("=" * 70)

if __name__ == "__main__":
    calculate_buying_power()