#!/usr/bin/env python3

"""
Trade Parser - Paste your trades in natural language and it will parse them
Supports various formats from brokers
"""

import re
import json
from datetime import datetime
from pathlib import Path
from trade_recorder import TradeRecorder
from benchmark_tracker import BenchmarkTracker

class TradeParser:
    def __init__(self):
        self.recorder = TradeRecorder()
        self.benchmark_tracker = BenchmarkTracker()
        self.base_path = Path(__file__).parent.parent
        
    def parse_trades_from_text(self, text):
        """Parse trades from pasted text in various formats"""
        trades = []
        lines = text.strip().split('\n')
        
        for line in lines:
            if not line.strip():
                continue
                
            # Try different parsing patterns
            trade = None
            
            # Pattern 1: "BUY 50 AAPL @ 150.25" or "BOUGHT 50 AAPL at $150.25"
            pattern1 = r'(?:BUY|BOUGHT|SELL|SOLD)\s+(\d+)\s+([A-Z]+)\s+(?:@|at)\s*\$?(\d+\.?\d*)'
            match1 = re.search(pattern1, line, re.IGNORECASE)
            
            # Pattern 2: "AAPL 50 shares bought at 150.25"
            pattern2 = r'([A-Z]+)\s+(\d+)\s+shares?\s+(?:bought|sold)\s+at\s*\$?(\d+\.?\d*)'
            match2 = re.search(pattern2, line, re.IGNORECASE)
            
            # Pattern 3: "50 AAPL 150.25 BUY" (quantity symbol price action)
            pattern3 = r'(\d+)\s+([A-Z]+)\s+\$?(\d+\.?\d*)\s+(BUY|SELL)'
            match3 = re.search(pattern3, line, re.IGNORECASE)
            
            # Pattern 4: Copy from broker "Filled Buy 50 AAPL @ $150.25 at 09:35 AM"
            pattern4 = r'(?:Filled\s+)?(Buy|Sell)\s+(\d+)\s+([A-Z]+)\s+@\s*\$?(\d+\.?\d*)(?:\s+at\s+(\d{1,2}:\d{2}\s*(?:AM|PM)))?'
            match4 = re.search(pattern4, line, re.IGNORECASE)
            
            # Pattern 5: Simple format "AAPL BUY 50 150.25"
            pattern5 = r'([A-Z]+)\s+(BUY|SELL)\s+(\d+)\s+\$?(\d+\.?\d*)'
            match5 = re.search(pattern5, line, re.IGNORECASE)
            
            if match1:
                action = 'BUY' if 'BUY' in line.upper() else 'SELL'
                trade = {
                    'symbol': match1.group(2).upper(),
                    'action': action,
                    'quantity': int(match1.group(1)),
                    'price': float(match1.group(3))
                }
                
            elif match2:
                action = 'BUY' if 'bought' in line.lower() else 'SELL'
                trade = {
                    'symbol': match2.group(1).upper(),
                    'action': action,
                    'quantity': int(match2.group(2)),
                    'price': float(match2.group(3))
                }
                
            elif match3:
                trade = {
                    'symbol': match3.group(2).upper(),
                    'action': match3.group(4).upper(),
                    'quantity': int(match3.group(1)),
                    'price': float(match3.group(3))
                }
                
            elif match4:
                trade = {
                    'symbol': match4.group(3).upper(),
                    'action': match4.group(1).upper(),
                    'quantity': int(match4.group(2)),
                    'price': float(match4.group(4))
                }
                if match4.group(5):
                    trade['time'] = match4.group(5)
                    
            elif match5:
                trade = {
                    'symbol': match5.group(1).upper(),
                    'action': match5.group(2).upper(),
                    'quantity': int(match5.group(3)),
                    'price': float(match5.group(4))
                }
            
            # Try to extract time if not already found
            if trade and 'time' not in trade:
                time_pattern = r'(\d{1,2}:\d{2}\s*(?:AM|PM))'
                time_match = re.search(time_pattern, line, re.IGNORECASE)
                if time_match:
                    trade['time'] = time_match.group(1)
                else:
                    # Default to market hours
                    trade['time'] = '09:30 AM'
            
            if trade:
                trades.append(trade)
                print(f"✓ Parsed: {trade['action']} {trade['quantity']} {trade['symbol']} @ ${trade['price']:.2f}")
            else:
                print(f"⚠️  Could not parse: {line}")
        
        return trades
    
    def process_pasted_trades(self, text):
        """Process pasted trades and update portfolio"""
        print("\n📋 Parsing Pasted Trades")
        print("=" * 50)
        
        trades = self.parse_trades_from_text(text)
        
        if not trades:
            print("❌ No trades could be parsed from the text")
            return []
        
        print(f"\n✅ Found {len(trades)} trades to record")
        
        # Record all trades
        recorded = []
        for trade in trades:
            try:
                self.recorder.record_trade(trade)
                recorded.append(trade)
            except Exception as e:
                print(f"❌ Error recording trade: {e}")
        
        # Show summary
        if recorded:
            print(f"\n📊 Successfully recorded {len(recorded)} trades")
            self.recorder.print_execution_summary()
            
            # Show benchmark comparison
            try:
                total_buy_amount = sum(trade['quantity'] * trade['price'] for trade in recorded if trade['action'].upper() == 'BUY')
                if total_buy_amount > 0:
                    print("\n📊 Benchmark comparison will be updated automatically with each trade")
            except Exception as e:
                print(f"Note: Benchmark tracking available in trade summary")
        
        return recorded
    
    def save_parsed_trades(self, trades):
        """Save parsed trades to file"""
        output_path = self.base_path / "data" / "parsed_trades.json"
        
        with open(output_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'trades': trades
            }, f, indent=2)
        
        return output_path

# Function to be called directly from Claude Code
def parse_and_record_trades(trades_text):
    """
    Main function to call from Claude Code
    Just pass the pasted text and it handles everything
    """
    parser = TradeParser()
    return parser.process_pasted_trades(trades_text)

if __name__ == "__main__":
    print("📝 Paste your trades below (press Enter twice when done):")
    print("Supported formats:")
    print("  - BUY 50 AAPL @ 150.25")
    print("  - Bought 50 shares AAPL at $150.25")
    print("  - AAPL 50 shares bought at 150.25")
    print("  - Filled Buy 50 AAPL @ $150.25 at 09:35 AM")
    print("=" * 50)
    
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            if lines:  # If we have some lines and hit empty line
                break
            # If no lines yet, continue waiting
    
    if lines:
        text = '\n'.join(lines)
        parser = TradeParser()
        parser.process_pasted_trades(text)