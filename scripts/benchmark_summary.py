#!/usr/bin/env python3

"""
Benchmark Summary
Show current benchmark comparison and performance
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from benchmark_tracker import BenchmarkTracker
from portfolio_tracker import PortfolioTracker

def main():
    print("📊 Benchmark Performance Summary")
    print("=" * 50)
    
    # Initialize trackers
    benchmark_tracker = BenchmarkTracker()
    portfolio_tracker = PortfolioTracker()
    
    # Get current portfolio data
    portfolio_data = portfolio_tracker.portfolio
    
    # Calculate total investment amount (buy trades only)
    total_invested = 0
    try:
        executions_path = Path(__file__).parent.parent / "data" / "executions"
        for execution_file in executions_path.glob("*_executions.json"):
            import json
            with open(execution_file, 'r') as f:
                execution_data = json.load(f)
                for trade in execution_data.get('trades', []):
                    if trade['action'].upper() == 'BUY':
                        total_invested += trade.get('actual_cost', trade['total_value'])
    except Exception as e:
        print(f"Note: Could not calculate total invested from executions: {e}")
        total_invested = portfolio_data['starting_balance'] - portfolio_data['cash_balance']
    
    print(f"Total Amount Invested: ${total_invested:.2f}")
    print(f"Current Portfolio Value: ${portfolio_data.get('total_value', portfolio_data['cash_balance']):.2f}")
    
    # Show benchmark comparison
    benchmark_tracker.print_benchmark_comparison(
        portfolio_data.get('total_value', portfolio_data['cash_balance']),
        total_invested
    )
    
    # Show current prices
    print("\n💰 Current Market Prices:")
    current_prices = benchmark_tracker.get_current_prices()
    print(f"  IWM: ${current_prices['IWM']:.2f}")
    print(f"  SPY: ${current_prices['SPY']:.2f}")
    
    print("\n📈 Next time you record a trade, benchmark prices will be automatically captured!")

if __name__ == "__main__":
    main()