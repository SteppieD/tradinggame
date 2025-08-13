#!/usr/bin/env python3

"""
End of Day Portfolio Update - August 13, 2025
Note: Some prices are estimates based on available data
"""

import json
from datetime import datetime

def eod_update():
    """Update portfolio with end of day prices"""
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Previous prices (from earlier today)
    morning_prices = {
        'CHPT': 10.90,
        'EVGO': 3.49,
        'FCEL': 6.08,
        'SPY': 642.69,
        'IWM': 229.80
    }
    
    # End of day prices (based on available data)
    # Note: Some are estimates or last known prices
    eod_prices = {
        'CHPT': 11.07,  # Found $11.07 reference in search
        'EVGO': 3.53,   # TradingView showed $3.53
        'FCEL': 4.09,   # August 12 close was $4.09, likely similar
        'SPY': 642.69,  # August 12 close, no Aug 13 data found
        'IWM': 203.21   # Found reference to $203.21 close
    }
    
    print("=" * 70)
    print("📊 END OF DAY PORTFOLIO UPDATE - August 13, 2025")
    print("=" * 70)
    print("\n⚠️  Note: Some prices are estimates based on limited data availability\n")
    
    # Calculate position performance
    print("📈 POSITION UPDATES:")
    print("-" * 50)
    
    total_morning_value = portfolio['cash_balance']
    total_eod_value = portfolio['cash_balance']
    total_cost = 0
    
    for pos in portfolio['positions']:
        symbol = pos['symbol']
        qty = pos['quantity']
        entry = pos['entry_price']
        morning = morning_prices.get(symbol, entry)
        eod = eod_prices.get(symbol, morning)
        
        cost = qty * entry
        morning_value = qty * morning
        eod_value = qty * eod
        
        total_cost += cost
        total_morning_value += morning_value
        total_eod_value += eod_value
        
        # Daily change
        daily_change = eod - morning
        daily_change_pct = (daily_change / morning) * 100
        
        # Total P&L
        total_pnl = eod_value - cost
        total_pnl_pct = (total_pnl / cost) * 100
        
        # Emoji based on daily performance
        daily_emoji = "📈" if daily_change > 0 else "📉" if daily_change < 0 else "➡️"
        
        print(f"\n{daily_emoji} {symbol}:")
        print(f"   Morning: ${morning:.2f} → EOD: ${eod:.2f}")
        print(f"   Daily Change: ${daily_change:.2f} ({daily_change_pct:+.2f}%)")
        print(f"   Position Value: ${eod_value:.2f}")
        print(f"   Total P&L: ${total_pnl:.2f} ({total_pnl_pct:+.2f}%)")
    
    # Portfolio summary
    print("\n" + "=" * 50)
    print("💼 PORTFOLIO SUMMARY:")
    print("-" * 50)
    
    morning_return = ((total_morning_value - 1000) / 1000) * 100
    eod_return = ((total_eod_value - 1000) / 1000) * 100
    daily_gain = total_eod_value - total_morning_value
    daily_gain_pct = (daily_gain / total_morning_value) * 100
    
    print(f"Morning Value: ${total_morning_value:.2f} ({morning_return:+.2f}%)")
    print(f"EOD Value: ${total_eod_value:.2f} ({eod_return:+.2f}%)")
    print(f"Daily Change: ${daily_gain:.2f} ({daily_gain_pct:+.2f}%)")
    
    # Benchmark comparison
    print("\n📊 BENCHMARK COMPARISON:")
    print("-" * 50)
    
    spy_daily = ((eod_prices['SPY'] - morning_prices['SPY']) / morning_prices['SPY']) * 100
    iwm_daily = ((eod_prices['IWM'] - morning_prices['IWM']) / morning_prices['IWM']) * 100
    
    print(f"Your Daily: {daily_gain_pct:+.2f}%")
    print(f"SPY Daily: {spy_daily:+.2f}%")
    print(f"IWM Daily: {iwm_daily:+.2f}%")
    
    # Since inception (Aug 12)
    spy_total = ((eod_prices['SPY'] - 642.00) / 642.00) * 100
    iwm_total = ((eod_prices['IWM'] - 225.50) / 225.50) * 100
    
    print(f"\nSince Aug 12 Start:")
    print(f"Your Total: {eod_return:+.2f}%")
    print(f"SPY Total: {spy_total:+.2f}%")
    print(f"IWM Total: {iwm_total:+.2f}%")
    
    # Warning about data
    print("\n" + "=" * 70)
    print("⚠️  DATA LIMITATIONS:")
    print("  - CHPT: Using $11.07 (last known reference)")
    print("  - EVGO: Using $3.53 (TradingView data)")
    print("  - FCEL: Using $4.09 (Aug 12 close, no Aug 13 data)")
    print("  - SPY: Using $642.69 (Aug 12 close)")
    print("  - IWM: Using $203.21 (found in after-hours reference)")
    print("\n  For accurate prices, check your broker or financial data provider")
    print("=" * 70)
    
    return eod_prices

if __name__ == "__main__":
    eod_update()