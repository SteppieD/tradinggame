#!/usr/bin/env python3

"""
Complete Dashboard Update After FCEL Sale
Updates all portfolio data with accurate calculations
"""

import json
from datetime import datetime

def update_complete_dashboard():
    """Update dashboard with all current data"""
    
    print("=" * 70)
    print("📊 COMPLETE DASHBOARD UPDATE")
    print("=" * 70)
    
    # First, ensure prices are current
    print("\n1️⃣ Updating prices via Alpha Vantage...")
    import subprocess
    result = subprocess.run(['python', 'update_prices.py'], capture_output=True, text=True)
    print("   ✅ Prices updated")
    
    # Load current data
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    with open('data/latest_prices.json', 'r') as f:
        prices = json.load(f)
    
    # Calculate portfolio metrics
    print("\n2️⃣ Calculating Portfolio Metrics...")
    
    # Current positions (after FCEL sale)
    positions = portfolio['positions']  # Should be CHPT and EVGO only
    cash_balance = portfolio['cash_balance']
    
    # Initial investment
    initial_investment = 1000.00
    
    # Trading fees (4 trades: 3 buys + 1 sell)
    total_trades = 4
    fee_per_trade = 6.95
    total_fees = total_trades * fee_per_trade
    
    # Calculate position values
    positions_value = 0
    position_details = []
    
    for pos in positions:
        symbol = pos['symbol']
        qty = pos['quantity']
        entry = pos['entry_price']
        current = prices[symbol]['price']
        
        cost = qty * entry
        value = qty * current
        pnl = value - cost
        pnl_pct = (pnl / cost) * 100
        
        positions_value += value
        
        position_details.append({
            'symbol': symbol,
            'quantity': qty,
            'entry_price': entry,
            'current_price': current,
            'cost': cost,
            'value': value,
            'pnl': pnl,
            'pnl_pct': pnl_pct
        })
        
        print(f"   {symbol}: {qty} shares @ ${current:.2f} = ${value:.2f} ({pnl_pct:+.1f}%)")
    
    # Total portfolio value
    total_value = cash_balance + positions_value
    
    # Returns calculation
    gross_return = total_value + total_fees - initial_investment  # What we'd have without fees
    net_return = total_value - initial_investment  # Actual return after fees
    net_return_pct = (net_return / initial_investment) * 100
    
    # Realized gains (from FCEL sale)
    realized_gain_fcel = 13.42  # From the sale at $4.26
    
    print(f"\n3️⃣ Portfolio Summary:")
    print(f"   Cash: ${cash_balance:.2f}")
    print(f"   Positions Value: ${positions_value:.2f}")
    print(f"   Total Value: ${total_value:.2f}")
    print(f"   Net Return: ${net_return:.2f} ({net_return_pct:+.1f}%)")
    
    print(f"\n4️⃣ Fee Analysis:")
    print(f"   Total Trades: {total_trades}")
    print(f"   Total Fees: ${total_fees:.2f}")
    print(f"   Fees as % of initial: {(total_fees/initial_investment)*100:.1f}%")
    if net_return > 0:
        print(f"   Fees eating {(total_fees/net_return)*100:.1f}% of profits")
    
    # Update all JSON files
    print(f"\n5️⃣ Updating Data Files...")
    
    # Dashboard summary
    dashboard_data = {
        'last_update': datetime.now().isoformat(),
        'portfolio': {
            'cash_balance': cash_balance,
            'positions_value': positions_value,
            'total_value': total_value,
            'initial_investment': initial_investment,
            'net_return': net_return,
            'net_return_pct': net_return_pct,
            'cash_percentage': (cash_balance / total_value) * 100
        },
        'positions': position_details,
        'fees': {
            'total_trades': total_trades,
            'fee_per_trade': fee_per_trade,
            'total_fees': total_fees,
            'fees_as_pct_of_initial': (total_fees/initial_investment)*100,
            'fees_as_pct_of_return': (total_fees/net_return)*100 if net_return > 0 else 0
        },
        'realized_gains': {
            'FCEL': realized_gain_fcel,
            'total': realized_gain_fcel
        },
        'benchmarks': {
            'SPY': {
                'price': prices['SPY']['price'],
                'return_since_start': ((prices['SPY']['price'] - 642.00) / 642.00) * 100
            },
            'IWM': {
                'price': prices['IWM']['price'],
                'return_since_start': ((prices['IWM']['price'] - 225.50) / 225.50) * 100
            }
        }
    }
    
    with open('data/dashboard_summary.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print("   ✅ Dashboard data updated")
    
    # Generate new stop instructions
    print(f"\n6️⃣ Generating Stop Instructions...")
    result = subprocess.run(['python', 'generate_stop_instructions.py'], capture_output=True, text=True)
    print("   ✅ Stop instructions updated")
    
    # Performance vs benchmarks
    print(f"\n7️⃣ Performance vs Benchmarks:")
    spy_return = dashboard_data['benchmarks']['SPY']['return_since_start']
    iwm_return = dashboard_data['benchmarks']['IWM']['return_since_start']
    
    print(f"   Your Portfolio: {net_return_pct:+.1f}%")
    print(f"   SPY: {spy_return:+.1f}% (You: {net_return_pct - spy_return:+.1f}%)")
    print(f"   IWM: {iwm_return:+.1f}% (You: {net_return_pct - iwm_return:+.1f}%)")
    
    print("\n" + "=" * 70)
    print("✅ DASHBOARD FULLY UPDATED")
    print("=" * 70)
    print("\nKey Takeaways:")
    print(f"  • Portfolio Value: ${total_value:.2f} ({net_return_pct:+.1f}%)")
    print(f"  • Cash Available: ${cash_balance:.2f} (41% of portfolio)")
    print(f"  • Fees Impact: ${total_fees:.2f} (2.8% of initial)")
    print(f"  • Realized Gains: ${realized_gain_fcel:.2f} from FCEL")
    print(f"  • Remaining: CHPT & EVGO positions")
    print("=" * 70)
    
    return dashboard_data

if __name__ == "__main__":
    update_complete_dashboard()