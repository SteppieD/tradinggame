#!/usr/bin/env python3

"""
Manual Dashboard Update Script
Updates all dashboard numbers with current prices using Alpha Vantage MCP
Includes smart stop loss calculations based on volatility and Fibonacci levels
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from scripts.alpha_vantage_client import AlphaVantageClient
from scripts.portfolio_tracker import PortfolioTracker
from scripts.benchmark_tracker import BenchmarkTracker
from smart_stops import get_stop_recommendations
import json
from datetime import datetime

def calculate_trail_stop(entry_price, current_price, trail_percent=10):
    """Calculate trailing stop loss price"""
    # If price is up, trail below current price
    if current_price > entry_price:
        trail_stop = current_price * (1 - trail_percent/100)
        # Never let trail stop go below break-even
        return max(trail_stop, entry_price)
    else:
        # If price is down, keep original stop at -10% from entry
        return entry_price * 0.9

def main():
    print("=" * 60)
    print("📊 MANUAL DASHBOARD UPDATE")
    print("=" * 60)
    print(f"Update Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
    
    # Initialize clients
    client = AlphaVantageClient()
    tracker = PortfolioTracker()
    benchmark_tracker = BenchmarkTracker()
    
    # Get current prices
    symbols = ['CHPT', 'EVGO', 'FCEL', 'SPY', 'IWM']
    prices = {}
    
    print("Fetching current prices...")
    for symbol in symbols:
        try:
            quote = client.get_quote(symbol)
            if quote:
                prices[symbol] = {
                    'price': float(quote.get('price', 0)),
                    'change': float(quote.get('change', 0)),
                    'change_percent': quote.get('change_percent', '0%'),
                    'timestamp': datetime.now().isoformat()
                }
                print(f"  {symbol}: ${quote.get('price', 'N/A')} ({quote.get('change_percent', 'N/A')}%)")
        except Exception as e:
            print(f"  Error getting {symbol}: {e}")
    
    # Save prices
    with open('data/latest_prices.json', 'w') as f:
        json.dump(prices, f, indent=2)
    
    print("\n" + "=" * 60)
    print("📈 POSITION UPDATES WITH SMART STOPS")
    print("=" * 60)
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Get smart stop recommendations
    positions = [p for p in portfolio['positions'] if p['symbol'] in ['CHPT', 'EVGO', 'FCEL']]
    stop_recommendations = get_stop_recommendations(positions, prices)
    
    # Calculate updates for each position
    total_value = portfolio['cash_balance']
    total_pnl = 0
    
    print("\n🎯 SMART STOP LOSS INSTRUCTIONS:")
    print("-" * 40)
    print("Using volatility-adjusted stops with Fibonacci retracements\n")
    
    for rec in stop_recommendations:
        symbol = rec['symbol']
        position = next(p for p in positions if p['symbol'] == symbol)
        
        # Calculate totals
        market_value = rec['quantity'] * rec['current_price']
        cost = rec['quantity'] * rec['entry_price']
        pnl = market_value - cost
        
        total_value += market_value
        total_pnl += pnl
        
        print(f"{symbol}:")
        print(f"  Current: ${rec['current_price']:.2f} (Entry: ${rec['entry_price']:.2f})")
        print(f"  P&L: ${pnl:.2f} ({rec['pnl_percent']:+.1f}%)")
        print(f"  Volatility: ±{rec['daily_volatility']}% daily")
        print(f"  ")
        print(f"  📍 RECOMMENDED STOP: ${rec['stop_price']}")
        print(f"     Limit: ${rec['limit_price']}")
        print(f"     Strategy: {rec['strategy']}")
        print(f"     Distance: -{rec['distance_percent']}% from current")
        print(f"     Reason: {rec['reason']}")
        print(f"  ")
        print(f"  Key Fibonacci Levels:")
        print(f"     38.2%: ${rec['fib_levels']['fib_382']} (minor support)")
        print(f"     50.0%: ${rec['fib_levels']['fib_500']} (major support)")
        print(f"     61.8%: ${rec['fib_levels']['fib_618']} (max pullback)")
        print(f"  " + "-" * 35)
    
    print("\n" + "=" * 60)
    print("💼 PORTFOLIO SUMMARY")
    print("=" * 60)
    
    print(f"  Cash Balance: ${portfolio['cash_balance']:.2f}")
    print(f"  Position Value: ${total_value - portfolio['cash_balance']:.2f}")
    print(f"  Total Value: ${total_value:.2f}")
    print(f"  Total P&L: ${total_pnl:+.2f} ({(total_pnl/970.67)*100:+.1f}%)")
    
    # Benchmark comparison
    print("\n" + "=" * 60)
    print("📊 BENCHMARK COMPARISON")
    print("=" * 60)
    
    with open('data/benchmark_tracking.json', 'r') as f:
        benchmark = json.load(f)
    
    iwm_shares = benchmark['totals']['iwm_total_shares']
    spy_shares = benchmark['totals']['spy_total_shares']
    invested = benchmark['totals']['total_invested']
    
    iwm_value = iwm_shares * prices['IWM']['price']
    spy_value = spy_shares * prices['SPY']['price']
    
    portfolio_return = ((total_value - 1000) / 1000) * 100
    iwm_return = ((iwm_value - invested) / invested) * 100
    spy_return = ((spy_value - invested) / invested) * 100
    
    print(f"  Your Portfolio: ${total_value:.2f} ({portfolio_return:+.1f}%)")
    print(f"  Russell 2000:   ${iwm_value:.2f} ({iwm_return:+.1f}%)")
    print(f"  S&P 500:        ${spy_value:.2f} ({spy_return:+.1f}%)")
    
    alpha_iwm = portfolio_return - iwm_return
    alpha_spy = portfolio_return - spy_return
    
    if alpha_iwm > 0:
        print(f"\n  vs IWM: 🟢 Outperforming by {alpha_iwm:+.1f}%")
    else:
        print(f"\n  vs IWM: 🔴 Underperforming by {alpha_iwm:.1f}%")
    
    if alpha_spy > 0:
        print(f"  vs SPY: 🟢 Outperforming by {alpha_spy:+.1f}%")
    else:
        print(f"  vs SPY: 🔴 Underperforming by {alpha_spy:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ DASHBOARD UPDATE COMPLETE")
    print("=" * 60)
    print("\n📝 TO-DO:")
    print("1. Update trail stops in CIBC as shown above")
    print("2. Refresh dashboard.html in browser to see updates")
    print("3. Monitor positions approaching profit targets (15%)")
    print("\n")

if __name__ == "__main__":
    main()