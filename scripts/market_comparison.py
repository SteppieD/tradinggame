#!/usr/bin/env python3

"""
Market Comparison Tracker
Compares portfolio performance to S&P 500 (SPY) and Russell 2000 (IWM)
"""

import json
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

class MarketComparison:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.portfolio_path = self.base_path / "data" / "portfolio.json"
        self.history_path = self.base_path / "data" / "performance_history.json"
        
        # ETFs for comparison
        self.benchmarks = {
            'SPY': 'S&P 500',
            'IWM': 'Russell 2000'
        }
        
    def load_portfolio(self):
        """Load current portfolio"""
        with open(self.portfolio_path, 'r') as f:
            return json.load(f)
    
    def get_benchmark_performance(self, start_date=None):
        """Get benchmark ETF performance"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        
        benchmark_data = {}
        
        for symbol, name in self.benchmarks.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start_date)
            
            if not hist.empty:
                # Calculate returns
                start_price = hist['Close'].iloc[0]
                current_price = hist['Close'].iloc[-1]
                total_return = ((current_price / start_price) - 1) * 100
                
                # Daily returns for chart
                daily_prices = hist['Close'].values
                daily_returns = [(price / start_price - 1) * 100 for price in daily_prices]
                
                benchmark_data[symbol] = {
                    'name': name,
                    'start_price': start_price,
                    'current_price': current_price,
                    'total_return': total_return,
                    'daily_returns': daily_returns,
                    'dates': hist.index.tolist()
                }
        
        return benchmark_data
    
    def calculate_portfolio_returns(self):
        """Calculate portfolio returns for comparison"""
        portfolio = self.load_portfolio()
        
        # Load history if exists
        if self.history_path.exists():
            with open(self.history_path, 'r') as f:
                history = json.load(f)
        else:
            history = {
                'dates': [],
                'values': [],
                'daily_returns': []
            }
        
        # Add current value
        current_date = str(datetime.now().date())
        current_value = portfolio.get('total_value', portfolio['cash_balance'])
        starting_value = portfolio['starting_balance']
        
        # Append today's data if not already there
        if not history['dates'] or history['dates'][-1] != current_date:
            history['dates'].append(current_date)
            history['values'].append(current_value)
            
            # Calculate return
            daily_return = ((current_value / starting_value) - 1) * 100
            history['daily_returns'].append(daily_return)
            
            # Save history
            with open(self.history_path, 'w') as f:
                json.dump(history, f, indent=2)
        
        return history
    
    def create_comparison_chart(self, save_path=None):
        """Create comparison chart of portfolio vs benchmarks"""
        # Get data
        portfolio_data = self.calculate_portfolio_returns()
        benchmark_data = self.get_benchmark_performance()
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.patch.set_facecolor('#0f0f0f')
        
        # Dark theme colors
        ax1.set_facecolor('#1a1a1a')
        ax2.set_facecolor('#1a1a1a')
        
        # Color scheme
        colors = {
            'portfolio': '#00ff41',  # Bright green
            'SPY': '#00b4d8',        # Cyan
            'IWM': '#f77f00'         # Orange
        }
        
        # Plot cumulative returns
        ax1.set_title('Portfolio vs Market Performance', color='white', fontsize=16, pad=20)
        ax1.set_ylabel('Cumulative Return (%)', color='white')
        ax1.grid(True, alpha=0.2, color='gray')
        ax1.tick_params(colors='white')
        
        # Plot portfolio
        if portfolio_data['daily_returns']:
            ax1.plot(range(len(portfolio_data['daily_returns'])), 
                    portfolio_data['daily_returns'], 
                    label='Your Portfolio', 
                    color=colors['portfolio'], 
                    linewidth=2.5)
            
            # Add current value annotation
            current_return = portfolio_data['daily_returns'][-1]
            ax1.annotate(f'{current_return:+.1f}%', 
                        xy=(len(portfolio_data['daily_returns'])-1, current_return),
                        xytext=(5, 0), textcoords='offset points',
                        color=colors['portfolio'], fontweight='bold')
        
        # Plot benchmarks
        for symbol, data in benchmark_data.items():
            ax1.plot(range(len(data['daily_returns'])), 
                    data['daily_returns'], 
                    label=data['name'], 
                    color=colors[symbol], 
                    linewidth=2, 
                    alpha=0.8)
            
            # Add annotation
            ax1.annotate(f'{data["total_return"]:+.1f}%', 
                        xy=(len(data['daily_returns'])-1, data['total_return']),
                        xytext=(5, 0), textcoords='offset points',
                        color=colors[symbol])
        
        ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax1.legend(loc='upper left', facecolor='#2a2a2a', edgecolor='gray', labelcolor='white')
        
        # Bar chart comparing returns
        ax2.set_title('Return Comparison', color='white', fontsize=14, pad=20)
        ax2.set_ylabel('Total Return (%)', color='white')
        ax2.grid(True, alpha=0.2, color='gray', axis='y')
        ax2.tick_params(colors='white')
        
        # Prepare data for bar chart
        labels = ['Portfolio', 'S&P 500', 'Russell 2000']
        returns = []
        bar_colors = []
        
        if portfolio_data['daily_returns']:
            returns.append(portfolio_data['daily_returns'][-1])
            bar_colors.append(colors['portfolio'])
        else:
            returns.append(0)
            bar_colors.append(colors['portfolio'])
        
        for symbol in ['SPY', 'IWM']:
            if symbol in benchmark_data:
                returns.append(benchmark_data[symbol]['total_return'])
                bar_colors.append(colors[symbol])
            else:
                returns.append(0)
                bar_colors.append(colors[symbol])
        
        bars = ax2.bar(labels, returns, color=bar_colors, alpha=0.8, edgecolor='white', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, returns):
            height = bar.get_height()
            color = 'white' if abs(height) > 0.1 else 'gray'
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:+.1f}%', ha='center', va='bottom' if height >= 0 else 'top',
                    color=color, fontweight='bold')
        
        ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        
        # Add performance summary
        portfolio_return = portfolio_data['daily_returns'][-1] if portfolio_data['daily_returns'] else 0
        spy_return = benchmark_data.get('SPY', {}).get('total_return', 0)
        iwm_return = benchmark_data.get('IWM', {}).get('total_return', 0)
        
        # Alpha calculation
        spy_alpha = portfolio_return - spy_return
        iwm_alpha = portfolio_return - iwm_return
        
        summary_text = f"Alpha vs S&P: {spy_alpha:+.1f}%  |  Alpha vs Russell: {iwm_alpha:+.1f}%"
        fig.text(0.5, 0.02, summary_text, ha='center', color='white', fontsize=12, 
                bbox=dict(boxstyle='round', facecolor='#2a2a2a', alpha=0.8))
        
        plt.tight_layout()
        
        # Save chart
        if not save_path:
            save_path = self.base_path / "reports" / "charts" / "market_comparison.png"
            save_path.parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(save_path, dpi=100, facecolor='#0f0f0f', edgecolor='none')
        print(f"Chart saved to {save_path}")
        
        # Also save as embedded HTML
        html_path = self.base_path / "market_comparison.html"
        self.create_html_chart(html_path, portfolio_data, benchmark_data)
        
        return fig
    
    def create_html_chart(self, output_path, portfolio_data, benchmark_data):
        """Create standalone HTML with embedded chart"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Market Comparison</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            background-color: #0f0f0f;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #00ff41;
        }}
        #chart {{
            width: 100%;
            height: 500px;
        }}
        .summary {{
            text-align: center;
            margin: 20px;
            padding: 15px;
            background: #1a1a1a;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <h1>Portfolio vs Market Performance</h1>
    <div id="chart"></div>
    <div class="summary">
        <h2>Performance Summary</h2>
        <p>Portfolio Return: {portfolio_data['daily_returns'][-1] if portfolio_data['daily_returns'] else 0:.1f}%</p>
        <p>S&P 500 Return: {benchmark_data.get('SPY', {}).get('total_return', 0):.1f}%</p>
        <p>Russell 2000 Return: {benchmark_data.get('IWM', {}).get('total_return', 0):.1f}%</p>
    </div>
    
    <script>
        var portfolioTrace = {{
            x: {list(range(len(portfolio_data['daily_returns'])))},
            y: {portfolio_data['daily_returns']},
            type: 'scatter',
            name: 'Portfolio',
            line: {{color: '#00ff41', width: 3}}
        }};
        
        var spyTrace = {{
            x: {list(range(len(benchmark_data.get('SPY', {}).get('daily_returns', []))))},
            y: {benchmark_data.get('SPY', {}).get('daily_returns', [])},
            type: 'scatter',
            name: 'S&P 500',
            line: {{color: '#00b4d8', width: 2}}
        }};
        
        var iwmTrace = {{
            x: {list(range(len(benchmark_data.get('IWM', {}).get('daily_returns', []))))},
            y: {benchmark_data.get('IWM', {}).get('daily_returns', [])},
            type: 'scatter',
            name: 'Russell 2000',
            line: {{color: '#f77f00', width: 2}}
        }};
        
        var data = [portfolioTrace, spyTrace, iwmTrace];
        
        var layout = {{
            title: 'Cumulative Returns',
            xaxis: {{title: 'Days', color: 'white'}},
            yaxis: {{title: 'Return (%)', color: 'white'}},
            plot_bgcolor: '#1a1a1a',
            paper_bgcolor: '#0f0f0f',
            font: {{color: 'white'}},
            showlegend: true,
            legend: {{x: 0, y: 1}}
        }};
        
        Plotly.newPlot('chart', data, layout);
    </script>
</body>
</html>
"""
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"Interactive chart saved to {output_path}")
    
    def run(self):
        """Generate comparison report"""
        print("Generating market comparison...")
        self.create_comparison_chart()
        
        # Print summary
        portfolio_data = self.calculate_portfolio_returns()
        benchmark_data = self.get_benchmark_performance()
        
        print("\n📊 Performance Summary")
        print("=" * 40)
        
        if portfolio_data['daily_returns']:
            print(f"Portfolio: {portfolio_data['daily_returns'][-1]:+.1f}%")
        
        for symbol, data in benchmark_data.items():
            print(f"{data['name']}: {data['total_return']:+.1f}%")
        
        return benchmark_data

if __name__ == "__main__":
    comparison = MarketComparison()
    comparison.run()