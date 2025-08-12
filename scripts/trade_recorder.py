#!/usr/bin/env python3

"""
Trade Recording System
Records actual trade executions with exact prices, quantities, and timestamps
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd
from portfolio_tracker import PortfolioTracker
from benchmark_tracker import BenchmarkTracker

class TradeRecorder:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.executions_path = self.base_path / "data" / "executions"
        self.executions_path.mkdir(parents=True, exist_ok=True)
        self.portfolio = PortfolioTracker()
        self.benchmark_tracker = BenchmarkTracker()
        
    def record_trade(self, trade_data):
        """Record a single trade execution"""
        # Validate required fields
        required_fields = ['symbol', 'action', 'quantity', 'price', 'time']
        for field in required_fields:
            if field not in trade_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Add additional metadata
        trade_data['recorded_at'] = datetime.now().isoformat()
        trade_data['date'] = trade_data.get('date', str(datetime.now().date()))
        trade_data['total_value'] = trade_data['quantity'] * trade_data['price']
        
        # Calculate commission if not provided
        if 'commission' not in trade_data:
            trade_data['commission'] = 0  # Free trading assumed
        
        # Calculate actual cost/proceeds
        if trade_data['action'].upper() == 'BUY':
            trade_data['actual_cost'] = trade_data['total_value'] + trade_data['commission']
        else:
            trade_data['actual_proceeds'] = trade_data['total_value'] - trade_data['commission']
        
        # Save to daily execution file
        daily_file = self.executions_path / f"{trade_data['date']}_executions.json"
        
        if daily_file.exists():
            with open(daily_file, 'r') as f:
                executions = json.load(f)
        else:
            executions = {
                'date': trade_data['date'],
                'trades': []
            }
        
        executions['trades'].append(trade_data)
        
        with open(daily_file, 'w') as f:
            json.dump(executions, f, indent=2)
        
        # Update portfolio
        if trade_data['action'].upper() == 'BUY':
            self.portfolio.add_position(
                trade_data['symbol'],
                trade_data['quantity'],
                trade_data['price']
            )
            # Record benchmark prices for buy trades
            try:
                trade_amount = trade_data['actual_cost']
                benchmark_record = self.benchmark_tracker.record_trade_benchmarks(
                    trade_amount, 
                    trade_data['time']
                )
                if benchmark_record:
                    trade_data['benchmark_tracking'] = benchmark_record
            except Exception as e:
                print(f"Warning: Could not record benchmark data: {e}")
                
        elif trade_data['action'].upper() == 'SELL':
            self.portfolio.remove_position(
                trade_data['symbol'],
                trade_data['quantity'],
                trade_data['price']
            )
        
        print(f"✅ Recorded: {trade_data['action']} {trade_data['quantity']} {trade_data['symbol']} @ ${trade_data['price']:.2f}")
        print(f"   Time: {trade_data['time']}")
        print(f"   Total: ${trade_data['total_value']:.2f}")
        
        return trade_data
    
    def record_multiple_trades(self, trades_list):
        """Record multiple trades at once"""
        recorded = []
        for trade in trades_list:
            try:
                recorded.append(self.record_trade(trade))
            except Exception as e:
                print(f"❌ Error recording trade: {e}")
        
        return recorded
    
    def import_from_csv(self, csv_path):
        """Import trades from a CSV file"""
        df = pd.read_csv(csv_path)
        
        # Expected columns: symbol, action, quantity, price, time, date (optional)
        trades = []
        for _, row in df.iterrows():
            trade = {
                'symbol': row['symbol'],
                'action': row['action'],
                'quantity': int(row['quantity']),
                'price': float(row['price']),
                'time': row['time']
            }
            
            if 'date' in row:
                trade['date'] = row['date']
            if 'commission' in row:
                trade['commission'] = float(row['commission'])
            
            trades.append(trade)
        
        return self.record_multiple_trades(trades)
    
    def get_today_executions(self):
        """Get all executions for today"""
        today = str(datetime.now().date())
        daily_file = self.executions_path / f"{today}_executions.json"
        
        if daily_file.exists():
            with open(daily_file, 'r') as f:
                return json.load(f)
        
        return {'date': today, 'trades': []}
    
    def compare_with_orders(self):
        """Compare actual executions with planned orders"""
        today = str(datetime.now().date())
        
        # Load planned orders
        orders_file = self.base_path / "orders" / f"{today}.json"
        if orders_file.exists():
            with open(orders_file, 'r') as f:
                planned = json.load(f)
        else:
            planned = {'orders': []}
        
        # Load actual executions
        executions = self.get_today_executions()
        
        # Compare
        comparison = {
            'date': today,
            'planned_orders': len(planned.get('orders', [])),
            'executed_trades': len(executions['trades']),
            'fills': [],
            'unfilled': [],
            'slippage_analysis': []
        }
        
        # Match executions to orders
        for order in planned.get('orders', []):
            matched = False
            for trade in executions['trades']:
                if (trade['symbol'] == order['symbol'] and 
                    trade['action'].upper() == order['action'].upper()):
                    matched = True
                    
                    # Calculate slippage
                    if 'limit_price' in order:
                        slippage = trade['price'] - order['limit_price']
                        slippage_pct = (slippage / order['limit_price']) * 100
                    else:
                        slippage = trade['price'] - order['price']
                        slippage_pct = (slippage / order['price']) * 100
                    
                    fill_data = {
                        'symbol': trade['symbol'],
                        'planned_qty': order['quantity'],
                        'actual_qty': trade['quantity'],
                        'planned_price': order.get('limit_price', order['price']),
                        'actual_price': trade['price'],
                        'slippage': round(slippage, 3),
                        'slippage_pct': round(slippage_pct, 2),
                        'execution_time': trade['time']
                    }
                    
                    comparison['fills'].append(fill_data)
                    comparison['slippage_analysis'].append({
                        'symbol': trade['symbol'],
                        'slippage_cost': slippage * trade['quantity']
                    })
                    break
            
            if not matched:
                comparison['unfilled'].append({
                    'symbol': order['symbol'],
                    'action': order['action'],
                    'quantity': order['quantity'],
                    'reason': order.get('reason', 'Unknown')
                })
        
        # Calculate totals
        if comparison['slippage_analysis']:
            total_slippage = sum(s['slippage_cost'] for s in comparison['slippage_analysis'])
            comparison['total_slippage_cost'] = round(total_slippage, 2)
        
        # Save comparison
        comparison_file = self.base_path / "reports" / "executions" / f"{today}_comparison.json"
        comparison_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        return comparison
    
    def print_execution_summary(self):
        """Print summary of today's executions"""
        executions = self.get_today_executions()
        comparison = self.compare_with_orders()
        
        print("\n📊 Execution Summary")
        print("=" * 50)
        print(f"Date: {executions['date']}")
        print(f"Executed Trades: {len(executions['trades'])}")
        
        if executions['trades']:
            print("\n✅ Filled Orders:")
            for trade in executions['trades']:
                print(f"  • {trade['action']} {trade['quantity']} {trade['symbol']} @ ${trade['price']:.2f} at {trade['time']}")
        
        if comparison['unfilled']:
            print("\n❌ Unfilled Orders:")
            for order in comparison['unfilled']:
                print(f"  • {order['action']} {order['quantity']} {order['symbol']}")
        
        if comparison.get('total_slippage_cost') is not None:
            print(f"\n💰 Total Slippage Cost: ${comparison['total_slippage_cost']:.2f}")
            
            if comparison['fills']:
                print("\nSlippage Details:")
                for fill in comparison['fills']:
                    if fill['slippage'] != 0:
                        direction = "worse" if fill['slippage'] > 0 else "better"
                        print(f"  • {fill['symbol']}: ${fill['actual_price']:.2f} vs ${fill['planned_price']:.2f} "
                              f"({fill['slippage_pct']:+.2f}% {direction})")
        
        # Portfolio update
        print("\n💼 Portfolio Update:")
        portfolio_data = self.portfolio.portfolio
        print(f"  Cash Balance: ${portfolio_data['cash_balance']:.2f}")
        print(f"  Positions: {len(portfolio_data['positions'])}")
        if portfolio_data.get('total_value'):
            print(f"  Total Value: ${portfolio_data['total_value']:.2f}")
            
        # Show benchmark comparison if we have trades
        try:
            benchmark_data = self.benchmark_tracker.get_current_benchmark_value()
            if benchmark_data:
                total_invested = sum(trade['actual_cost'] for trade in executions['trades'] if trade['action'].upper() == 'BUY')
                self.benchmark_tracker.print_benchmark_comparison(
                    portfolio_data.get('total_value', portfolio_data['cash_balance']),
                    total_invested
                )
        except Exception as e:
            print(f"Warning: Could not display benchmark comparison: {e}")

def interactive_input():
    """Interactive trade input"""
    print("\n📝 Trade Entry System")
    print("=" * 50)
    
    trades = []
    
    while True:
        print("\nEnter trade details (or 'done' to finish):")
        
        symbol = input("Symbol (e.g., AAPL): ").strip().upper()
        if symbol.lower() == 'done':
            break
        
        action = input("Action (BUY/SELL): ").strip().upper()
        if action not in ['BUY', 'SELL']:
            print("❌ Invalid action. Must be BUY or SELL")
            continue
        
        try:
            quantity = int(input("Quantity: "))
            price = float(input("Price per share: $"))
            time = input("Execution time (e.g., 09:35 AM): ").strip()
            
            commission = input("Commission (press Enter for $0): ").strip()
            commission = float(commission) if commission else 0
            
            trade = {
                'symbol': symbol,
                'action': action,
                'quantity': quantity,
                'price': price,
                'time': time,
                'commission': commission
            }
            
            trades.append(trade)
            print(f"✅ Added: {action} {quantity} {symbol} @ ${price:.2f}")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            continue
    
    return trades

def main():
    recorder = TradeRecorder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'add':
            # Quick add: python trade_recorder.py add SYMBOL ACTION QTY PRICE TIME
            if len(sys.argv) >= 7:
                trade = {
                    'symbol': sys.argv[2].upper(),
                    'action': sys.argv[3].upper(),
                    'quantity': int(sys.argv[4]),
                    'price': float(sys.argv[5]),
                    'time': sys.argv[6]
                }
                
                if len(sys.argv) > 7:
                    trade['commission'] = float(sys.argv[7])
                
                recorder.record_trade(trade)
                recorder.print_execution_summary()
            else:
                print("Usage: python trade_recorder.py add SYMBOL ACTION QTY PRICE TIME [COMMISSION]")
                print("Example: python trade_recorder.py add SNDL BUY 49 2.01 '09:35 AM'")
        
        elif command == 'import':
            # Import from CSV
            if len(sys.argv) > 2:
                csv_path = sys.argv[2]
                recorder.import_from_csv(csv_path)
                recorder.print_execution_summary()
            else:
                print("Usage: python trade_recorder.py import path/to/trades.csv")
        
        elif command == 'summary':
            # Show summary
            recorder.print_execution_summary()
        
        elif command == 'compare':
            # Compare with orders
            comparison = recorder.compare_with_orders()
            print(json.dumps(comparison, indent=2))
        
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  add      - Add a single trade")
            print("  import   - Import trades from CSV")
            print("  summary  - Show today's execution summary")
            print("  compare  - Compare executions with planned orders")
    
    else:
        # Interactive mode
        print("🔄 Interactive Trade Entry")
        trades = interactive_input()
        
        if trades:
            print(f"\n Recording {len(trades)} trades...")
            recorder.record_multiple_trades(trades)
            recorder.print_execution_summary()
        else:
            print("No trades entered.")

if __name__ == "__main__":
    main()