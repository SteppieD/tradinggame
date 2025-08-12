#!/usr/bin/env python3

"""
Benchmark Tracker
Automatically tracks IWM and SPY prices when trades are recorded
Maintains running comparison of investment performance vs benchmarks
"""

import json
import yfinance as yf
from datetime import datetime
from pathlib import Path
import time

class BenchmarkTracker:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.tracking_file = self.base_path / "data" / "benchmark_tracking.json"
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Benchmark symbols
        self.benchmarks = ['IWM', 'SPY']
        
        # Initialize tracking file if it doesn't exist
        if not self.tracking_file.exists():
            self._initialize_tracking_file()
    
    def _initialize_tracking_file(self):
        """Initialize empty tracking file"""
        initial_data = {
            "trades": [],
            "totals": {
                "total_invested": 0.0,
                "iwm_total_shares": 0.0,
                "spy_total_shares": 0.0
            }
        }
        
        with open(self.tracking_file, 'w') as f:
            json.dump(initial_data, f, indent=2)
    
    def get_current_prices(self):
        """Fetch current prices for IWM and SPY"""
        prices = {}
        
        for symbol in self.benchmarks:
            try:
                ticker = yf.Ticker(symbol)
                # Get the most recent price
                hist = ticker.history(period="1d", interval="1m")
                
                if not hist.empty:
                    prices[symbol] = float(hist['Close'].iloc[-1])
                else:
                    # Fallback to daily data
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        prices[symbol] = float(hist['Close'].iloc[-1])
                    else:
                        print(f"Warning: Could not fetch price for {symbol}")
                        prices[symbol] = 0.0
                        
                # Small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error fetching {symbol} price: {e}")
                prices[symbol] = 0.0
        
        return prices
    
    def record_trade_benchmarks(self, trade_amount, trade_time=None):
        """Record benchmark prices when a trade is made"""
        if trade_time is None:
            trade_time = datetime.now().strftime("%I:%M %p")
        
        # Get current benchmark prices
        prices = self.get_current_prices()
        
        if not prices['IWM'] or not prices['SPY']:
            print("Warning: Could not fetch benchmark prices")
            return None
        
        # Calculate shares that could be bought
        iwm_shares = trade_amount / prices['IWM'] if prices['IWM'] > 0 else 0
        spy_shares = trade_amount / prices['SPY'] if prices['SPY'] > 0 else 0
        
        # Create trade record
        trade_record = {
            "date": str(datetime.now().date()),
            "time": trade_time,
            "amount_invested": round(trade_amount, 2),
            "iwm_price": round(prices['IWM'], 2),
            "spy_price": round(prices['SPY'], 2),
            "iwm_shares_bought": round(iwm_shares, 6),
            "spy_shares_bought": round(spy_shares, 6)
        }
        
        # Load existing data
        with open(self.tracking_file, 'r') as f:
            data = json.load(f)
        
        # Add new trade
        data['trades'].append(trade_record)
        
        # Update totals
        data['totals']['total_invested'] = round(data['totals']['total_invested'] + trade_amount, 2)
        data['totals']['iwm_total_shares'] = round(data['totals']['iwm_total_shares'] + iwm_shares, 6)
        data['totals']['spy_total_shares'] = round(data['totals']['spy_total_shares'] + spy_shares, 6)
        
        # Save updated data
        with open(self.tracking_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📊 Benchmark tracking updated:")
        print(f"   IWM @ ${prices['IWM']:.2f} - {iwm_shares:.3f} shares")
        print(f"   SPY @ ${prices['SPY']:.2f} - {spy_shares:.3f} shares")
        
        return trade_record
    
    def get_current_benchmark_value(self):
        """Calculate current value of benchmark investments"""
        # Load tracking data
        with open(self.tracking_file, 'r') as f:
            data = json.load(f)
        
        if not data['trades']:
            return None
        
        # Get current prices
        current_prices = self.get_current_prices()
        
        if not current_prices['IWM'] or not current_prices['SPY']:
            print("Warning: Could not fetch current benchmark prices")
            return None
        
        # Calculate current values
        iwm_current_value = data['totals']['iwm_total_shares'] * current_prices['IWM']
        spy_current_value = data['totals']['spy_total_shares'] * current_prices['SPY']
        total_invested = data['totals']['total_invested']
        
        # Calculate returns
        iwm_return = iwm_current_value - total_invested
        spy_return = spy_current_value - total_invested
        iwm_return_pct = (iwm_return / total_invested * 100) if total_invested > 0 else 0
        spy_return_pct = (spy_return / total_invested * 100) if total_invested > 0 else 0
        
        return {
            'total_invested': total_invested,
            'iwm': {
                'current_price': current_prices['IWM'],
                'total_shares': data['totals']['iwm_total_shares'],
                'current_value': round(iwm_current_value, 2),
                'return_amount': round(iwm_return, 2),
                'return_percent': round(iwm_return_pct, 2)
            },
            'spy': {
                'current_price': current_prices['SPY'],
                'total_shares': data['totals']['spy_total_shares'],
                'current_value': round(spy_current_value, 2),
                'return_amount': round(spy_return, 2),
                'return_percent': round(spy_return_pct, 2)
            }
        }
    
    def print_benchmark_comparison(self, portfolio_value=None, portfolio_invested=None):
        """Print comparison of portfolio vs benchmarks"""
        benchmark_data = self.get_current_benchmark_value()
        
        if not benchmark_data:
            print("No benchmark data available")
            return
        
        print("\n📊 Benchmark Comparison")
        print("=" * 50)
        print(f"Total Invested: ${benchmark_data['total_invested']:.2f}")
        print()
        
        print(f"IWM (Russell 2000):")
        print(f"  Current Price: ${benchmark_data['iwm']['current_price']:.2f}")
        print(f"  Total Shares: {benchmark_data['iwm']['total_shares']:.3f}")
        print(f"  Current Value: ${benchmark_data['iwm']['current_value']:.2f}")
        print(f"  Return: ${benchmark_data['iwm']['return_amount']:+.2f} ({benchmark_data['iwm']['return_percent']:+.1f}%)")
        print()
        
        print(f"SPY (S&P 500):")
        print(f"  Current Price: ${benchmark_data['spy']['current_price']:.2f}")
        print(f"  Total Shares: {benchmark_data['spy']['total_shares']:.3f}")
        print(f"  Current Value: ${benchmark_data['spy']['current_value']:.2f}")
        print(f"  Return: ${benchmark_data['spy']['return_amount']:+.2f} ({benchmark_data['spy']['return_percent']:+.1f}%)")
        
        # If portfolio data is provided, show comparison
        if portfolio_value is not None and portfolio_invested is not None:
            portfolio_return = portfolio_value - portfolio_invested
            portfolio_return_pct = (portfolio_return / portfolio_invested * 100) if portfolio_invested > 0 else 0
            
            print("\n💼 Your Portfolio:")
            print(f"  Current Value: ${portfolio_value:.2f}")
            print(f"  Return: ${portfolio_return:+.2f} ({portfolio_return_pct:+.1f}%)")
            
            print("\n🎯 Alpha (Outperformance):")
            iwm_alpha = portfolio_return_pct - benchmark_data['iwm']['return_percent']
            spy_alpha = portfolio_return_pct - benchmark_data['spy']['return_percent']
            print(f"  vs IWM: {iwm_alpha:+.1f}%")
            print(f"  vs SPY: {spy_alpha:+.1f}%")
    
    def get_tracking_data(self):
        """Get all tracking data"""
        with open(self.tracking_file, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    tracker = BenchmarkTracker()
    
    # Test the tracker
    print("Testing Benchmark Tracker")
    print("=" * 30)
    
    # Get current prices
    prices = tracker.get_current_prices()
    print(f"Current IWM: ${prices['IWM']:.2f}")
    print(f"Current SPY: ${prices['SPY']:.2f}")
    
    # Show current benchmark values if any trades exist
    current_values = tracker.get_current_benchmark_value()
    if current_values:
        tracker.print_benchmark_comparison()
    else:
        print("\nNo trades recorded yet")