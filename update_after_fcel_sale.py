#!/usr/bin/env python3

"""
Portfolio Update After FCEL Sale
Calculate new positions and tomorrow's strategy
"""

import json
from datetime import datetime

def update_portfolio_status():
    """Update portfolio status after FCEL sale"""
    
    # Load updated portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Current prices (using latest known)
    current_prices = {
        'CHPT': 11.07,  # Last known EOD estimate
        'EVGO': 3.53,   # Last known EOD estimate
        'SPY': 642.69,
        'IWM': 229.80
    }
    
    print("=" * 70)
    print("📊 PORTFOLIO STATUS AFTER FCEL SALE")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print()
    
    # Calculate remaining positions value
    positions_value = 0
    print("📈 REMAINING POSITIONS:")
    print("-" * 50)
    
    for pos in portfolio['positions']:
        symbol = pos['symbol']
        qty = pos['quantity']
        entry = pos['entry_price']
        current = current_prices.get(symbol, entry)
        
        position_value = qty * current
        position_cost = qty * entry
        position_pnl = position_value - position_cost
        position_pnl_pct = (position_pnl / position_cost) * 100
        
        positions_value += position_value
        
        print(f"\n{symbol}:")
        print(f"  Quantity: {qty} shares")
        print(f"  Entry: ${entry:.4f}")
        print(f"  Current: ${current:.2f}")
        print(f"  Value: ${position_value:.2f}")
        print(f"  P&L: ${position_pnl:.2f} ({position_pnl_pct:+.2f}%)")
    
    # Portfolio summary
    total_value = portfolio['cash_balance'] + positions_value
    initial_investment = 1000.00
    total_return = total_value - initial_investment
    total_return_pct = (total_return / initial_investment) * 100
    
    print("\n" + "=" * 50)
    print("💼 PORTFOLIO SUMMARY:")
    print("-" * 50)
    print(f"Cash Available: ${portfolio['cash_balance']:.2f} (41.5% of portfolio)")
    print(f"Positions Value: ${positions_value:.2f}")
    print(f"Total Portfolio: ${total_value:.2f}")
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Total Return: ${total_return:.2f} ({total_return_pct:+.2f}%)")
    
    # Risk analysis
    print("\n📊 RISK ANALYSIS:")
    print("-" * 50)
    cash_percentage = (portfolio['cash_balance'] / total_value) * 100
    invested_percentage = (positions_value / total_value) * 100
    
    print(f"Cash Position: {cash_percentage:.1f}% (${portfolio['cash_balance']:.2f})")
    print(f"Invested: {invested_percentage:.1f}% (${positions_value:.2f})")
    print(f"Positions at Risk: 2 stocks")
    
    # Fee analysis
    total_fees = 6.95 * 4  # 3 buys + 1 sell
    fees_impact = (total_fees / total_return * 100) if total_return > 0 else 0
    
    print(f"\nTotal Fees Paid: ${total_fees:.2f}")
    print(f"Fees as % of Returns: {fees_impact:.1f}%")
    
    # Tomorrow's strategy
    print("\n" + "=" * 70)
    print("🎯 TOMORROW'S STRATEGY:")
    print("=" * 70)
    
    print("\n1️⃣ MORNING STOPS (6:30 AM PST):")
    print("-" * 50)
    
    for pos in portfolio['positions']:
        symbol = pos['symbol']
        current = current_prices.get(symbol, pos['entry_price'])
        
        # Calculate smart stops
        if symbol == 'CHPT':
            # Small profit, protect breakeven
            stop_price = pos['entry_price'] + 0.10  # Just above breakeven
            trigger_delta = round(current - stop_price, 2)
            print(f"CHPT: Trigger Delta ${trigger_delta:.2f} (protect small gain)")
        elif symbol == 'EVGO':
            # Small loss, tight stop
            stop_price = pos['entry_price'] - 0.20  # Limit loss
            trigger_delta = round(current - stop_price, 2)
            print(f"EVGO: Trigger Delta ${trigger_delta:.2f} (limit losses)")
    
    print("\n2️⃣ CASH DEPLOYMENT OPTIONS:")
    print("-" * 50)
    print(f"Available Cash: ${portfolio['cash_balance']:.2f}")
    print("Consider:")
    print("  • Wait for market pullback")
    print("  • Look for oversold EV/clean energy stocks")
    print("  • Keep some cash for averaging down if needed")
    print("  • Maximum position size: ~$200 to maintain diversification")
    
    print("\n3️⃣ MARKET WATCH:")
    print("-" * 50)
    print("Monitor:")
    print("  • EV sector sentiment")
    print("  • Federal EV incentive news")
    print("  • Charging infrastructure announcements")
    print("  • Small-cap momentum (IWM)")
    
    print("\n" + "=" * 70)
    print("📝 KEY TAKEAWAYS:")
    print("=" * 70)
    print("✅ Locked in $13.42 profit from FCEL (+3.42%)")
    print("✅ Reduced risk with 41.5% cash position")
    print("✅ Still up overall despite FCEL not hitting 50% target")
    print("⚠️ EVGO needs watching (currently at small loss)")
    print("💡 Good position to buy dips with cash available")
    print("=" * 70)
    
    # Save summary
    summary = {
        'date': datetime.now().isoformat(),
        'after_fcel_sale': True,
        'cash_balance': portfolio['cash_balance'],
        'positions_value': positions_value,
        'total_value': total_value,
        'total_return': total_return,
        'total_return_pct': total_return_pct,
        'cash_percentage': cash_percentage,
        'remaining_positions': len(portfolio['positions']),
        'realized_gain_fcel': 13.42
    }
    
    with open('data/post_sale_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

if __name__ == "__main__":
    update_portfolio_status()