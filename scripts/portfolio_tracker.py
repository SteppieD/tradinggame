#!/usr/bin/env python3

import json
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

class PortfolioTracker:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.portfolio_path = self.base_path / "data" / "portfolio.json"
        self.history_path = self.base_path / "data" / "trades_history.csv"
        self.load_portfolio()
    
    def load_portfolio(self):
        """Load current portfolio from JSON"""
        with open(self.portfolio_path, 'r') as f:
            self.portfolio = json.load(f)
    
    def save_portfolio(self):
        """Save portfolio to JSON"""
        self.portfolio['last_updated'] = datetime.now().isoformat()
        with open(self.portfolio_path, 'w') as f:
            json.dump(self.portfolio, f, indent=2)
    
    def add_position(self, symbol, quantity, entry_price, order_type="BUY"):
        """Add a new position or update existing one"""
        position = None
        for pos in self.portfolio['positions']:
            if pos['symbol'] == symbol:
                position = pos
                break
        
        if position:
            # Update existing position (averaging)
            total_value = (position['quantity'] * position['entry_price']) + (quantity * entry_price)
            position['quantity'] += quantity
            position['entry_price'] = total_value / position['quantity']
            position['last_updated'] = datetime.now().isoformat()
        else:
            # Add new position
            self.portfolio['positions'].append({
                'symbol': symbol,
                'quantity': quantity,
                'entry_price': entry_price,
                'entry_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'stop_loss': entry_price * 0.9,  # 10% stop loss
                'target_price': entry_price * 1.2  # 20% target
            })
        
        # Update cash balance
        self.portfolio['cash_balance'] -= (quantity * entry_price)
        
        # Log trade
        self.log_trade(symbol, quantity, entry_price, order_type)
        
        self.save_portfolio()
        print(f"✓ Added position: {quantity} {symbol} @ ${entry_price:.2f}")
    
    def remove_position(self, symbol, quantity, exit_price):
        """Remove or reduce a position"""
        position = None
        for i, pos in enumerate(self.portfolio['positions']):
            if pos['symbol'] == symbol:
                position = pos
                pos_index = i
                break
        
        if not position:
            print(f"❌ No position found for {symbol}")
            return
        
        if quantity >= position['quantity']:
            # Close entire position
            actual_quantity = position['quantity']
            self.portfolio['positions'].pop(pos_index)
        else:
            # Reduce position
            actual_quantity = quantity
            position['quantity'] -= quantity
            position['last_updated'] = datetime.now().isoformat()
        
        # Calculate P&L
        pnl = (exit_price - position['entry_price']) * actual_quantity
        pnl_percent = ((exit_price / position['entry_price']) - 1) * 100
        
        # Update cash balance
        self.portfolio['cash_balance'] += (actual_quantity * exit_price)
        
        # Log trade
        self.log_trade(symbol, actual_quantity, exit_price, "SELL", pnl)
        
        self.save_portfolio()
        print(f"✓ Sold {actual_quantity} {symbol} @ ${exit_price:.2f} | P&L: ${pnl:.2f} ({pnl_percent:+.1f}%)")
        
        return pnl, pnl_percent
    
    def log_trade(self, symbol, quantity, price, order_type, pnl=None):
        """Log trade to history CSV"""
        trade = {
            'date': datetime.now().isoformat(),
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'order_type': order_type,
            'value': quantity * price,
            'pnl': pnl if pnl else 0,
            'cash_balance': self.portfolio['cash_balance']
        }
        
        # Create or append to CSV
        df = pd.DataFrame([trade])
        if self.history_path.exists():
            df.to_csv(self.history_path, mode='a', header=False, index=False)
        else:
            df.to_csv(self.history_path, index=False)
    
    def update_portfolio_values(self):
        """Update current values for all positions"""
        total_value = self.portfolio['cash_balance']
        
        for position in self.portfolio['positions']:
            ticker = yf.Ticker(position['symbol'])
            current_price = ticker.info.get('currentPrice', position['entry_price'])
            
            position['current_price'] = current_price
            position['market_value'] = current_price * position['quantity']
            position['unrealized_pnl'] = (current_price - position['entry_price']) * position['quantity']
            position['unrealized_pnl_percent'] = ((current_price / position['entry_price']) - 1) * 100
            
            total_value += position['market_value']
            
            # Check stop loss
            if current_price <= position['stop_loss']:
                print(f"⚠️  STOP LOSS ALERT: {position['symbol']} at ${current_price:.2f} (stop: ${position['stop_loss']:.2f})")
        
        self.portfolio['total_value'] = total_value
        self.portfolio['total_pnl'] = total_value - self.portfolio['starting_balance']
        self.portfolio['total_pnl_percent'] = ((total_value / self.portfolio['starting_balance']) - 1) * 100
        
        self.save_portfolio()
        return total_value
    
    def get_performance_metrics(self):
        """Calculate performance metrics"""
        if not self.history_path.exists():
            return None
        
        trades_df = pd.read_csv(self.history_path)
        
        # Calculate metrics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        
        if total_trades > 0:
            win_rate = (winning_trades / total_trades) * 100
        else:
            win_rate = 0
        
        total_pnl = trades_df['pnl'].sum()
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        # Calculate Sharpe ratio (simplified)
        if len(trades_df) > 1:
            daily_returns = trades_df['pnl'].pct_change().dropna()
            sharpe = (daily_returns.mean() / daily_returns.std()) * (252 ** 0.5) if daily_returns.std() > 0 else 0
        else:
            sharpe = 0
        
        metrics = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'sharpe_ratio': sharpe,
            'current_value': self.portfolio['total_value'],
            'cash_balance': self.portfolio['cash_balance'],
            'positions_count': len(self.portfolio['positions'])
        }
        
        return metrics
    
    def generate_report(self):
        """Generate performance report"""
        self.update_portfolio_values()
        metrics = self.get_performance_metrics()
        
        report_path = self.base_path / "reports" / "daily" / f"{datetime.now().date()}_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            'date': str(datetime.now().date()),
            'generated_at': datetime.now().isoformat(),
            'portfolio': self.portfolio,
            'metrics': metrics
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n📊 Portfolio Summary")
        print("=" * 40)
        print(f"Total Value: ${self.portfolio['total_value']:.2f}")
        print(f"Cash Balance: ${self.portfolio['cash_balance']:.2f}")
        print(f"Total P&L: ${self.portfolio['total_pnl']:.2f} ({self.portfolio['total_pnl_percent']:+.1f}%)")
        print(f"Positions: {len(self.portfolio['positions'])}")
        
        if metrics:
            print(f"\nWin Rate: {metrics['win_rate']:.1f}%")
            print(f"Total Trades: {metrics['total_trades']}")
            print(f"Avg Win: ${metrics['avg_win']:.2f}")
            print(f"Avg Loss: ${metrics['avg_loss']:.2f}")
        
        print("\n📈 Current Positions:")
        for pos in self.portfolio['positions']:
            print(f"  {pos['symbol']}: {pos['quantity']} @ ${pos.get('current_price', pos['entry_price']):.2f} "
                  f"({pos.get('unrealized_pnl_percent', 0):+.1f}%)")
        
        return report

if __name__ == "__main__":
    tracker = PortfolioTracker()
    
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "buy" and len(sys.argv) == 5:
            symbol = sys.argv[2]
            quantity = int(sys.argv[3])
            price = float(sys.argv[4])
            tracker.add_position(symbol, quantity, price)
        
        elif command == "sell" and len(sys.argv) == 5:
            symbol = sys.argv[2]
            quantity = int(sys.argv[3])
            price = float(sys.argv[4])
            tracker.remove_position(symbol, quantity, price)
        
        elif command == "update":
            tracker.update_portfolio_values()
            print("Portfolio values updated")
        
        elif command == "report":
            tracker.generate_report()
        
        else:
            print("Usage:")
            print("  python portfolio_tracker.py buy SYMBOL QUANTITY PRICE")
            print("  python portfolio_tracker.py sell SYMBOL QUANTITY PRICE")
            print("  python portfolio_tracker.py update")
            print("  python portfolio_tracker.py report")
    else:
        # Default: generate report
        tracker.generate_report()