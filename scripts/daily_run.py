#!/usr/bin/env python3

"""
Main orchestrator script that runs all daily trading operations
Run this script each trading day to:
1. Screen for opportunities
2. Check congressional trades
3. Generate orders
4. Update portfolio
5. Create reports
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Import all our modules
from stock_screener import SmallCapScreener
from congressional_tracker import CongressionalTracker
from order_generator import OrderGenerator
from portfolio_tracker import PortfolioTracker
from performance_visualizer import PerformanceVisualizer
from daily_analysis import DailyTradingAnalysis

class TradingOrchestrator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.today = datetime.now().date()
        self.log_path = self.base_path / "logs"
        self.log_path.mkdir(exist_ok=True)
        
        # Initialize all components
        self.screener = SmallCapScreener()
        self.congress_tracker = CongressionalTracker()
        self.order_gen = OrderGenerator()
        self.portfolio = PortfolioTracker()
        self.visualizer = PerformanceVisualizer()
        self.analyzer = DailyTradingAnalysis()
    
    def log_message(self, message, level="INFO"):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # Write to log file
        log_file = self.log_path / f"{self.today}_trading.log"
        with open(log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def morning_routine(self):
        """Pre-market morning routine"""
        self.log_message("=" * 50)
        self.log_message("🌅 STARTING MORNING ROUTINE")
        self.log_message("=" * 50)
        
        # 1. Update portfolio values
        self.log_message("Updating portfolio values...")
        self.portfolio.update_portfolio_values()
        
        # 2. Screen for opportunities
        self.log_message("Screening for small-cap opportunities...")
        screening_results = self.screener.run()
        self.log_message(f"Found {len(screening_results)} opportunities")
        
        # 3. Check congressional trades
        self.log_message("Checking congressional trading activity...")
        congress_data = self.congress_tracker.run()
        actionable_congress = congress_data.get('actionable', [])
        self.log_message(f"Found {len(actionable_congress)} congressional signals")
        
        # 4. Run analysis
        self.log_message("Running daily analysis...")
        analysis, opportunities = self.analyzer.run()
        
        # 5. Generate orders
        self.log_message("Generating trading orders...")
        orders = self.order_gen.run()
        self.log_message(f"Generated {len(orders)} orders for today")
        
        # Create morning summary
        summary = {
            'date': str(self.today),
            'portfolio_value': self.portfolio.portfolio['total_value'],
            'cash_available': self.portfolio.portfolio['cash_balance'],
            'positions_count': len(self.portfolio.portfolio['positions']),
            'orders_generated': len(orders),
            'opportunities_found': len(screening_results),
            'congressional_signals': len(actionable_congress)
        }
        
        # Save summary
        summary_path = self.base_path / "reports" / "daily" / f"{self.today}_morning.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.log_message("Morning routine complete!")
        return summary
    
    def execute_trades(self, trades_executed):
        """Record executed trades (called after manual execution)"""
        self.log_message("=" * 50)
        self.log_message("📝 RECORDING EXECUTED TRADES")
        self.log_message("=" * 50)
        
        for trade in trades_executed:
            if trade['type'] == 'BUY':
                self.portfolio.add_position(
                    trade['symbol'],
                    trade['quantity'],
                    trade['price']
                )
            elif trade['type'] == 'SELL':
                self.portfolio.remove_position(
                    trade['symbol'],
                    trade['quantity'],
                    trade['price']
                )
            
            self.log_message(f"Recorded: {trade['type']} {trade['quantity']} {trade['symbol']} @ ${trade['price']}")
    
    def end_of_day_routine(self):
        """End of day routine"""
        self.log_message("=" * 50)
        self.log_message("🌆 STARTING END OF DAY ROUTINE")
        self.log_message("=" * 50)
        
        # 1. Update portfolio with closing prices
        self.log_message("Updating portfolio with closing prices...")
        self.portfolio.update_portfolio_values()
        
        # 2. Generate performance report
        self.log_message("Generating performance report...")
        self.portfolio.generate_report()
        
        # 3. Create visualizations
        self.log_message("Creating performance charts...")
        try:
            self.visualizer.generate_performance_report()
        except Exception as e:
            self.log_message(f"Error generating charts: {e}", "WARNING")
        
        # 4. Calculate daily metrics
        metrics = self.portfolio.get_performance_metrics()
        
        # Create EOD summary
        summary = {
            'date': str(self.today),
            'closing_value': self.portfolio.portfolio['total_value'],
            'daily_pnl': self.portfolio.portfolio.get('total_pnl', 0),
            'daily_pnl_percent': self.portfolio.portfolio.get('total_pnl_percent', 0),
            'positions': self.portfolio.portfolio['positions'],
            'metrics': metrics
        }
        
        # Save summary
        summary_path = self.base_path / "reports" / "daily" / f"{self.today}_eod.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.log_message("End of day routine complete!")
        self.log_message(f"Portfolio Value: ${summary['closing_value']:.2f}")
        self.log_message(f"Daily P&L: ${summary['daily_pnl']:.2f} ({summary['daily_pnl_percent']:+.1f}%)")
        
        return summary
    
    def run_command(self, command, args=None):
        """Run specific commands"""
        commands = {
            'morning': self.morning_routine,
            'eod': self.end_of_day_routine,
            'screen': self.screener.run,
            'congress': self.congress_tracker.run,
            'orders': self.order_gen.run,
            'report': self.portfolio.generate_report,
            'charts': self.visualizer.generate_performance_report,
            'analysis': self.analyzer.run
        }
        
        if command in commands:
            self.log_message(f"Running command: {command}")
            return commands[command]()
        else:
            self.log_message(f"Unknown command: {command}", "ERROR")
            print("\nAvailable commands:")
            for cmd in commands:
                print(f"  - {cmd}")
            return None

def main():
    orchestrator = TradingOrchestrator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'trade':
            # Record executed trades
            # Format: python daily_run.py trade BUY SYMBOL QUANTITY PRICE
            if len(sys.argv) == 6:
                trade_type = sys.argv[2]
                symbol = sys.argv[3]
                quantity = int(sys.argv[4])
                price = float(sys.argv[5])
                
                trades = [{
                    'type': trade_type,
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price
                }]
                orchestrator.execute_trades(trades)
            else:
                print("Usage: python daily_run.py trade [BUY|SELL] SYMBOL QUANTITY PRICE")
        else:
            orchestrator.run_command(command)
    else:
        # Default: run morning routine
        print("\n🚀 Claude Trading System - Daily Run")
        print("=" * 50)
        print("\nCommands:")
        print("  morning  - Run morning routine (screening + orders)")
        print("  eod      - Run end-of-day routine (reports + charts)")
        print("  screen   - Run stock screener only")
        print("  congress - Check congressional trades only")
        print("  orders   - Generate orders only")
        print("  report   - Generate performance report")
        print("  charts   - Create performance charts")
        print("  analysis - Run daily analysis")
        print("  trade    - Record executed trade")
        print("\nRunning default morning routine...\n")
        
        orchestrator.morning_routine()

if __name__ == "__main__":
    main()