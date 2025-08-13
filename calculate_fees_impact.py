#!/usr/bin/env python3

"""
Calculate Trading Fees Impact on Portfolio Performance
CIBC charges $6.95 per trade
"""

import json
from datetime import datetime

def calculate_fees_impact():
    """Calculate total fees and their impact on returns"""
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Load latest prices
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # CIBC fee per trade
    CIBC_FEE = 6.95
    
    # Count trades from portfolio (each position = 1 buy trade)
    trades = []
    
    # Initial purchases (3 positions)
    trades.append({"date": "2025-08-12", "symbol": "CHPT", "type": "BUY", "fee": CIBC_FEE})
    trades.append({"date": "2025-08-12", "symbol": "EVGO", "type": "BUY", "fee": CIBC_FEE})
    trades.append({"date": "2025-08-12", "symbol": "FCEL", "type": "BUY", "fee": CIBC_FEE})
    
    # Daily stop orders (if executed, would incur fees)
    # Note: Stop orders that don't execute don't incur fees
    
    total_fees = len(trades) * CIBC_FEE
    
    # Calculate current portfolio value
    positions_value = 0
    total_cost = 0
    
    for pos in portfolio['positions']:
        if pos['symbol'] in prices:
            current_price = prices[pos['symbol']]['price']
            positions_value += pos['quantity'] * current_price
            total_cost += pos['quantity'] * pos['entry_price']
    
    # Portfolio calculations
    gross_portfolio_value = portfolio['cash_balance'] + positions_value
    net_portfolio_value = gross_portfolio_value  # Fees already deducted from cash when trades were made
    
    # P&L calculations
    gross_pnl = positions_value - total_cost
    gross_pnl_pct = (gross_pnl / total_cost) * 100
    
    # Actual return (fees already paid from initial $1000)
    actual_investment = 1000.00
    net_return = net_portfolio_value - actual_investment
    net_return_pct = (net_return / actual_investment) * 100
    
    # What return would be without fees
    theoretical_value = gross_portfolio_value + total_fees
    theoretical_return = theoretical_value - actual_investment
    theoretical_return_pct = (theoretical_return / actual_investment) * 100
    
    # Impact of fees
    fee_impact_on_return = theoretical_return_pct - net_return_pct
    fee_as_pct_of_profit = (total_fees / gross_pnl * 100) if gross_pnl > 0 else 0
    
    results = {
        "fees_summary": {
            "total_trades": len(trades),
            "fee_per_trade": CIBC_FEE,
            "total_fees_paid": total_fees,
            "fees_as_pct_of_investment": (total_fees / actual_investment) * 100
        },
        "portfolio_performance": {
            "gross_pnl": gross_pnl,
            "gross_pnl_pct": gross_pnl_pct,
            "net_portfolio_value": net_portfolio_value,
            "net_return": net_return,
            "net_return_pct": net_return_pct
        },
        "fee_impact": {
            "theoretical_return_without_fees": theoretical_return,
            "theoretical_return_pct_without_fees": theoretical_return_pct,
            "return_lost_to_fees_pct": fee_impact_on_return,
            "fees_as_pct_of_gross_profit": fee_as_pct_of_profit
        },
        "trades": trades,
        "last_updated": datetime.now().isoformat()
    }
    
    # Save fee analysis
    with open('data/fee_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("=" * 60)
    print("💰 TRADING FEES IMPACT ANALYSIS")
    print("=" * 60)
    print(f"\n📊 Fees Paid:")
    print(f"  Total Trades: {len(trades)}")
    print(f"  Fee per Trade: ${CIBC_FEE}")
    print(f"  Total Fees: ${total_fees:.2f}")
    print(f"  Fees as % of Investment: {(total_fees / actual_investment) * 100:.2f}%")
    
    print(f"\n📈 Portfolio Performance:")
    print(f"  Gross P&L: ${gross_pnl:.2f} ({gross_pnl_pct:.2f}%)")
    print(f"  Net Portfolio Value: ${net_portfolio_value:.2f}")
    print(f"  Net Return: ${net_return:.2f} ({net_return_pct:.2f}%)")
    
    print(f"\n⚠️  Fee Impact:")
    print(f"  Return WITHOUT fees would be: {theoretical_return_pct:.2f}%")
    print(f"  Return WITH fees: {net_return_pct:.2f}%")
    print(f"  Return lost to fees: -{fee_impact_on_return:.2f}%")
    
    if gross_pnl > 0:
        print(f"  Fees eating {fee_as_pct_of_profit:.1f}% of your profits!")
    
    print("\n💡 Tips:")
    print("  - Batch trades to minimize fee impact")
    print("  - Larger positions = lower fee % impact")
    print("  - Avoid frequent small trades")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    calculate_fees_impact()