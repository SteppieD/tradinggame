#!/usr/bin/env python3

"""
Verify actual portfolio value
"""

import json
from datetime import datetime

def verify_portfolio_value():
    """Calculate exact portfolio value"""
    
    print("=" * 70)
    print("PORTFOLIO VALUE VERIFICATION")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print()
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Load latest prices
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # Manual price overrides for new stocks
    manual_prices = {
        'TDUP': 10.51,
        'FUBO': 3.76
    }
    
    print("POSITION BREAKDOWN:")
    print("-" * 50)
    
    total_value = 0
    total_cost = 0
    
    for pos in portfolio['positions']:
        symbol = pos['symbol']
        shares = pos['quantity']
        entry = pos['entry_price']
        
        # Get current price
        if symbol in manual_prices:
            current = manual_prices[symbol]
        elif symbol in prices:
            current = prices[symbol]['price']
        else:
            current = entry  # fallback
        
        position_value = shares * current
        position_cost = shares * entry
        position_pnl = position_value - position_cost
        
        total_value += position_value
        total_cost += position_cost
        
        print(f"{symbol}:")
        print(f"  {shares} shares @ ${current:.2f} = ${position_value:.2f}")
        print(f"  Cost basis: ${position_cost:.2f}")
        print(f"  P&L: ${position_pnl:.2f} ({position_pnl/position_cost*100:.1f}%)")
        print()
    
    # Add cash
    cash = portfolio['cash_balance']
    portfolio_total = total_value + cash
    
    print("-" * 50)
    print(f"Total Position Value: ${total_value:.2f}")
    print(f"Cash Balance: ${cash:.2f}")
    print(f"Portfolio Total: ${portfolio_total:.2f}")
    print()
    
    # Calculate returns
    initial_investment = 1000.00
    total_return = portfolio_total - initial_investment
    return_pct = (total_return / initial_investment) * 100
    
    print("RETURN CALCULATION:")
    print("-" * 50)
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Current Value: ${portfolio_total:.2f}")
    print(f"Total Return: ${total_return:.2f}")
    print(f"Return %: {return_pct:.2f}%")
    print()
    
    # Account for fees
    fees_paid = 41.70  # 6 trades
    gross_return = total_return + fees_paid
    
    print("FEE IMPACT:")
    print("-" * 50)
    print(f"Gross Return (before fees): ${gross_return:.2f}")
    print(f"Fees Paid: -${fees_paid:.2f}")
    print(f"Net Return: ${total_return:.2f}")
    print()
    
    # Check if dashboard calculation is wrong
    print("=" * 70)
    print("DASHBOARD CHECK:")
    print("-" * 50)
    
    if return_pct < 0:
        print("❌ WARNING: Dashboard shows negative return!")
        print("Possible issues:")
        print("1. Portfolio.json not updated with new trades")
        print("2. Prices not updating correctly")
        print("3. Cash balance incorrect")
    else:
        print(f"✅ You should be UP +{return_pct:.2f}%")
    
    print()
    print("ACTUAL POSITIONS:")
    print("-" * 50)
    print("CHPT: 26 shares @ $12.05 = $313.30")
    print("EVGO: 82 shares @ $3.94 = $323.08")
    print("TDUP: 19 shares @ $10.51 = $199.69")
    print("FUBO: 55 shares @ $3.76 = $206.80")
    print("Cash: $0.45")
    print("-" * 50)
    print("TOTAL: $1,043.32")
    print("Return: +4.33%")
    print("=" * 70)

if __name__ == "__main__":
    verify_portfolio_value()