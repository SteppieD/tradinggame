#!/usr/bin/env python3

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

class PerformanceVisualizer:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "reports"
        self.charts_path = self.reports_path / "charts"
        self.charts_path.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def load_trade_history(self):
        """Load trade history from CSV"""
        history_path = self.base_path / "data" / "trades_history.csv"
        if history_path.exists():
            return pd.read_csv(history_path)
        return pd.DataFrame()
    
    def load_portfolio(self):
        """Load current portfolio"""
        portfolio_path = self.base_path / "data" / "portfolio.json"
        with open(portfolio_path, 'r') as f:
            return json.load(f)
    
    def plot_portfolio_value(self, save=True):
        """Plot portfolio value over time"""
        df = self.load_trade_history()
        if df.empty:
            print("No trade history to plot")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Plot cash balance over time
        ax.plot(df['date'], df['cash_balance'], label='Cash Balance', linewidth=2)
        
        # Add starting balance reference line
        portfolio = self.load_portfolio()
        ax.axhline(y=portfolio['starting_balance'], color='gray', 
                   linestyle='--', label='Starting Balance', alpha=0.5)
        
        # Format
        ax.set_title('Portfolio Value Over Time', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Value ($)', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        
        if save:
            chart_path = self.charts_path / 'portfolio_value.png'
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            print(f"Chart saved to {chart_path}")
        
        plt.show()
        return fig
    
    def plot_win_loss_distribution(self, save=True):
        """Plot distribution of wins and losses"""
        df = self.load_trade_history()
        if df.empty:
            print("No trade history to plot")
            return
        
        # Filter for sells only (completed trades)
        sells = df[df['order_type'] == 'SELL']
        if sells.empty:
            print("No completed trades yet")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Win/Loss pie chart
        wins = len(sells[sells['pnl'] > 0])
        losses = len(sells[sells['pnl'] < 0])
        
        if wins + losses > 0:
            colors = ['#2ecc71', '#e74c3c']
            ax1.pie([wins, losses], labels=['Wins', 'Losses'], 
                   autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('Win/Loss Ratio', fontsize=14, fontweight='bold')
        
        # P&L distribution histogram
        if len(sells) > 0:
            ax2.hist(sells['pnl'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
            ax2.set_title('P&L Distribution', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Profit/Loss ($)', fontsize=12)
            ax2.set_ylabel('Frequency', fontsize=12)
            
            # Add statistics
            mean_pnl = sells['pnl'].mean()
            ax2.axvline(x=mean_pnl, color='green', linestyle='-', 
                       label=f'Avg: ${mean_pnl:.2f}', alpha=0.7)
            ax2.legend()
        
        plt.tight_layout()
        
        if save:
            chart_path = self.charts_path / 'win_loss_distribution.png'
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            print(f"Chart saved to {chart_path}")
        
        plt.show()
        return fig
    
    def plot_positions_performance(self, save=True):
        """Plot current positions performance"""
        portfolio = self.load_portfolio()
        positions = portfolio.get('positions', [])
        
        if not positions:
            print("No current positions to plot")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data
        symbols = []
        pnl_percents = []
        colors = []
        
        for pos in positions:
            symbols.append(pos['symbol'])
            pnl_pct = pos.get('unrealized_pnl_percent', 0)
            pnl_percents.append(pnl_pct)
            colors.append('#2ecc71' if pnl_pct >= 0 else '#e74c3c')
        
        # Create bar chart
        bars = ax.bar(symbols, pnl_percents, color=colors, alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar, pct in zip(bars, pnl_percents):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{pct:+.1f}%', ha='center', va='bottom' if height >= 0 else 'top')
        
        # Format
        ax.set_title('Current Positions Performance', fontsize=16, fontweight='bold')
        ax.set_xlabel('Symbol', fontsize=12)
        ax.set_ylabel('Unrealized P&L (%)', fontsize=12)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            chart_path = self.charts_path / 'positions_performance.png'
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            print(f"Chart saved to {chart_path}")
        
        plt.show()
        return fig
    
    def plot_daily_returns(self, save=True):
        """Plot daily returns"""
        df = self.load_trade_history()
        if df.empty or len(df) < 2:
            print("Not enough data for daily returns")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate daily returns
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df['daily_return'] = df['cash_balance'].pct_change() * 100
        
        # Plot
        positive = df['daily_return'] >= 0
        ax.bar(df.loc[positive, 'date'], df.loc[positive, 'daily_return'], 
               color='#2ecc71', alpha=0.7, label='Positive')
        ax.bar(df.loc[~positive, 'date'], df.loc[~positive, 'daily_return'], 
               color='#e74c3c', alpha=0.7, label='Negative')
        
        # Format
        ax.set_title('Daily Returns', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Return (%)', fontsize=12)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            chart_path = self.charts_path / 'daily_returns.png'
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            print(f"Chart saved to {chart_path}")
        
        plt.show()
        return fig
    
    def generate_performance_report(self):
        """Generate comprehensive performance report with all charts"""
        print("📊 Generating Performance Report...")
        
        portfolio = self.load_portfolio()
        
        # Create summary statistics
        stats = {
            'date': str(datetime.now().date()),
            'total_value': portfolio.get('total_value', portfolio['cash_balance']),
            'cash_balance': portfolio['cash_balance'],
            'starting_balance': portfolio['starting_balance'],
            'total_pnl': portfolio.get('total_pnl', 0),
            'total_pnl_percent': portfolio.get('total_pnl_percent', 0),
            'positions_count': len(portfolio['positions'])
        }
        
        # Calculate additional metrics from trade history
        df = self.load_trade_history()
        if not df.empty:
            sells = df[df['order_type'] == 'SELL']
            if not sells.empty:
                stats['total_trades'] = len(sells)
                stats['winning_trades'] = len(sells[sells['pnl'] > 0])
                stats['losing_trades'] = len(sells[sells['pnl'] < 0])
                stats['win_rate'] = (stats['winning_trades'] / stats['total_trades'] * 100) if stats['total_trades'] > 0 else 0
                stats['avg_win'] = sells[sells['pnl'] > 0]['pnl'].mean() if stats['winning_trades'] > 0 else 0
                stats['avg_loss'] = sells[sells['pnl'] < 0]['pnl'].mean() if stats['losing_trades'] > 0 else 0
                stats['total_realized_pnl'] = sells['pnl'].sum()
        
        # Save statistics
        report_path = self.reports_path / f"performance_report_{datetime.now().date()}.json"
        with open(report_path, 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Generate all charts
        try:
            self.plot_portfolio_value(save=True)
        except Exception as e:
            print(f"Could not generate portfolio value chart: {e}")
        
        try:
            self.plot_positions_performance(save=True)
        except Exception as e:
            print(f"Could not generate positions chart: {e}")
        
        try:
            self.plot_win_loss_distribution(save=True)
        except Exception as e:
            print(f"Could not generate win/loss chart: {e}")
        
        try:
            self.plot_daily_returns(save=True)
        except Exception as e:
            print(f"Could not generate daily returns chart: {e}")
        
        # Print summary
        print("\n📈 Performance Summary")
        print("=" * 40)
        print(f"Total Value: ${stats['total_value']:.2f}")
        print(f"Total P&L: ${stats['total_pnl']:.2f} ({stats['total_pnl_percent']:+.1f}%)")
        print(f"Cash Balance: ${stats['cash_balance']:.2f}")
        print(f"Active Positions: {stats['positions_count']}")
        
        if 'win_rate' in stats:
            print(f"\nWin Rate: {stats['win_rate']:.1f}%")
            print(f"Avg Win: ${stats['avg_win']:.2f}")
            print(f"Avg Loss: ${stats['avg_loss']:.2f}")
        
        print(f"\nReport saved to {report_path}")
        print(f"Charts saved to {self.charts_path}")
        
        return stats

if __name__ == "__main__":
    visualizer = PerformanceVisualizer()
    visualizer.generate_performance_report()