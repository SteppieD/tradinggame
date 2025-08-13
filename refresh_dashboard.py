#!/usr/bin/env python3

"""
Refresh dashboard with latest prices and calculations
"""

import json
from datetime import datetime
from pathlib import Path

def main():
    base_path = Path(__file__).parent
    
    # Load latest prices
    with open(base_path / 'data' / 'latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # Load portfolio
    with open(base_path / 'data' / 'portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Load benchmark tracking
    with open(base_path / 'data' / 'benchmark_tracking.json', 'r') as f:
        benchmark = json.load(f)
    
    # Calculate current portfolio value
    cash = portfolio['cash_balance']
    total_value = cash
    position_value = 0
    
    print("\n📊 PORTFOLIO UPDATE")
    print("=" * 50)
    print(f"Last Update: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print("\n💼 POSITIONS:")
    
    for position in portfolio['positions']:
        symbol = position['symbol']
        if symbol in prices:
            current_price = prices[symbol]['price']
            qty = position['quantity']
            entry = position['entry_price']
            value = qty * current_price
            cost = qty * entry
            pnl = value - cost
            pnl_pct = (pnl / cost) * 100
            
            position_value += value
            total_value += value
            
            status = "🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"
            
            print(f"\n{status} {symbol}:")
            print(f"   Qty: {qty} @ ${entry:.2f}")
            print(f"   Current: ${current_price:.2f} ({prices[symbol]['change_percent']}% today)")
            print(f"   Value: ${value:.2f}")
            print(f"   P&L: ${pnl:.2f} ({pnl_pct:+.1f}%)")
            
            # Check position management levels
            if pnl_pct >= 15:
                print(f"   ⚠️  ACTION: Consider taking profits (+15% target reached)")
            elif pnl_pct >= 10:
                print(f"   📍 Trail stop 5% below current price (${current_price * 0.95:.2f})")
            elif pnl_pct >= 5:
                print(f"   📍 Move stop to break-even (${entry:.2f})")
    
    print(f"\n💰 ACCOUNT SUMMARY:")
    print(f"   Cash: ${cash:.2f}")
    print(f"   Positions: ${position_value:.2f}")
    print(f"   Total Value: ${total_value:.2f}")
    
    # Calculate P&L
    starting = portfolio['starting_balance']
    total_pnl = total_value - starting
    total_pnl_pct = (total_pnl / starting) * 100
    
    print(f"   Total P&L: ${total_pnl:+.2f} ({total_pnl_pct:+.1f}%)")
    
    # Benchmark comparison
    print(f"\n📈 BENCHMARK COMPARISON:")
    
    # Calculate benchmark values
    iwm_shares = benchmark['totals']['iwm_total_shares']
    spy_shares = benchmark['totals']['spy_total_shares']
    
    iwm_value = iwm_shares * prices['IWM']['price']
    spy_value = spy_shares * prices['SPY']['price']
    
    iwm_pnl = iwm_value - benchmark['totals']['total_invested']
    spy_pnl = spy_value - benchmark['totals']['total_invested']
    
    iwm_pnl_pct = (iwm_pnl / benchmark['totals']['total_invested']) * 100
    spy_pnl_pct = (spy_pnl / benchmark['totals']['total_invested']) * 100
    
    print(f"   Your Portfolio: ${total_value:.2f} ({total_pnl_pct:+.1f}%)")
    print(f"   Russell 2000:   ${iwm_value:.2f} ({iwm_pnl_pct:+.1f}%)")
    print(f"   S&P 500:        ${spy_value:.2f} ({spy_pnl_pct:+.1f}%)")
    
    # Calculate alpha
    avg_benchmark = (iwm_pnl_pct + spy_pnl_pct) / 2
    alpha = total_pnl_pct - avg_benchmark
    
    if alpha > 0:
        print(f"\n   🏆 OUTPERFORMING MARKET BY {alpha:+.1f}%!")
    else:
        print(f"\n   📉 Underperforming market by {abs(alpha):.1f}%")
    
    print("\n" + "=" * 50)
    print("Dashboard refreshed! Open dashboard.html to see updates.\n")
    
    # Save summary to file
    summary = {
        'last_update': datetime.now().isoformat(),
        'portfolio_value': total_value,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl_pct,
        'iwm_value': iwm_value,
        'spy_value': spy_value,
        'alpha': alpha,
        'prices': prices
    }
    
    with open(base_path / 'data' / 'dashboard_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()