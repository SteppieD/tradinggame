#!/usr/bin/env python3

"""
API Call Manager
Manages and optimizes Alpha Vantage API usage (25 calls/day limit)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import time

class APIManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.usage_file = self.base_path / "data" / "api_usage.json"
        self.usage_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Alpha Vantage limits
        self.daily_limit = 25
        self.calls_per_minute = 5
        
        # Priority levels for different call types
        self.priorities = {
            'quote': 1,           # Real-time quotes - highest priority
            'news_sentiment': 2,  # News sentiment
            'technical': 3,       # Technical indicators
            'overview': 4,        # Company overview
            'earnings': 5,        # Earnings data
            'intraday': 6,        # Intraday data - lowest priority
        }
        
        self.load_usage()
    
    def load_usage(self):
        """Load API usage history"""
        if self.usage_file.exists():
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        else:
            self.usage = {
                'date': str(datetime.now().date()),
                'calls': [],
                'total_calls': 0
            }
    
    def save_usage(self):
        """Save API usage history"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)
    
    def reset_if_new_day(self):
        """Reset usage counter if it's a new day"""
        today = str(datetime.now().date())
        if self.usage['date'] != today:
            self.usage = {
                'date': today,
                'calls': [],
                'total_calls': 0
            }
            self.save_usage()
            return True
        return False
    
    def can_make_call(self, call_type='general', symbol=None):
        """Check if we can make an API call"""
        self.reset_if_new_day()
        
        # Check daily limit
        if self.usage['total_calls'] >= self.daily_limit:
            print(f"⚠️ Daily API limit reached ({self.daily_limit} calls)")
            return False
        
        # Check if we've already made this call today (caching)
        if symbol:
            for call in self.usage['calls']:
                if call.get('symbol') == symbol and call.get('type') == call_type:
                    time_since = datetime.now() - datetime.fromisoformat(call['timestamp'])
                    if time_since < timedelta(hours=1):  # 1 hour cache
                        print(f"📦 Using cached data for {symbol} {call_type}")
                        return False
        
        return True
    
    def record_call(self, call_type='general', symbol=None):
        """Record an API call"""
        self.reset_if_new_day()
        
        call_record = {
            'timestamp': datetime.now().isoformat(),
            'type': call_type,
            'symbol': symbol
        }
        
        self.usage['calls'].append(call_record)
        self.usage['total_calls'] += 1
        self.save_usage()
        
        print(f"📊 API call {self.usage['total_calls']}/{self.daily_limit}: {call_type} {symbol or ''}")
    
    def get_remaining_calls(self):
        """Get number of remaining API calls for today"""
        self.reset_if_new_day()
        return self.daily_limit - self.usage['total_calls']
    
    def get_priority_symbols(self, symbols, max_symbols=5):
        """Prioritize which symbols to fetch based on importance"""
        # For now, just take the first max_symbols
        # Could be enhanced with volume, volatility, or position size
        return symbols[:max_symbols]
    
    def optimize_daily_calls(self):
        """Plan optimal API usage for the day"""
        remaining = self.get_remaining_calls()
        
        if remaining <= 0:
            return {
                'quotes': [],
                'news': [],
                'technical': [],
                'overview': []
            }
        
        # Allocate calls by priority
        allocation = {
            'quotes': min(10, remaining // 2),      # 50% for real-time quotes
            'news': min(5, remaining // 4),         # 25% for news
            'technical': min(5, remaining // 5),    # 20% for technical
            'overview': max(0, remaining - 20)      # Remainder for overview
        }
        
        print(f"\n📋 Optimal API Allocation (Remaining: {remaining} calls)")
        print("=" * 40)
        for call_type, count in allocation.items():
            print(f"{call_type}: {count} calls")
        
        return allocation
    
    def get_usage_summary(self):
        """Get usage summary for display"""
        self.reset_if_new_day()
        
        summary = {
            'date': self.usage['date'],
            'calls_used': self.usage['total_calls'],
            'calls_remaining': self.get_remaining_calls(),
            'percentage_used': (self.usage['total_calls'] / self.daily_limit) * 100,
            'recent_calls': self.usage['calls'][-5:] if self.usage['calls'] else []
        }
        
        return summary
    
    def smart_fetch_strategy(self, symbols):
        """Determine smart fetching strategy for multiple symbols"""
        remaining = self.get_remaining_calls()
        
        if remaining <= 5:
            # Conservative mode - only critical updates
            print("⚠️ Low API calls remaining - fetching only critical data")
            return {
                'fetch_quotes': symbols[:2],  # Only top 2 symbols
                'fetch_news': [],
                'fetch_technical': [],
                'skip_reason': 'Low API quota'
            }
        elif remaining <= 15:
            # Balanced mode
            print("⚖️ Balanced API usage mode")
            return {
                'fetch_quotes': symbols[:5],
                'fetch_news': symbols[:2],
                'fetch_technical': symbols[:3],
                'skip_reason': None
            }
        else:
            # Full mode
            print("✅ Full API usage available")
            return {
                'fetch_quotes': symbols[:10],
                'fetch_news': symbols[:5],
                'fetch_technical': symbols[:5],
                'skip_reason': None
            }

class AlphaVantageOptimized:
    """Wrapper for Alpha Vantage client with API management"""
    
    def __init__(self, alpha_vantage_client):
        self.client = alpha_vantage_client
        self.api_manager = APIManager()
    
    def get_quote(self, symbol):
        """Get quote with API management"""
        if self.api_manager.can_make_call('quote', symbol):
            self.api_manager.record_call('quote', symbol)
            return self.client.get_quote(symbol)
        return None
    
    def get_news_sentiment(self, symbol):
        """Get news with API management"""
        if self.api_manager.can_make_call('news_sentiment', symbol):
            self.api_manager.record_call('news_sentiment', symbol)
            return self.client.get_news_sentiment(symbol)
        return None
    
    def get_technical_indicator(self, symbol, indicator='RSI'):
        """Get technical indicator with API management"""
        if self.api_manager.can_make_call('technical', symbol):
            self.api_manager.record_call('technical', symbol)
            return self.client.get_technical_indicator(symbol, indicator)
        return None
    
    def batch_analyze(self, symbols):
        """Analyze multiple symbols with optimal API usage"""
        strategy = self.api_manager.smart_fetch_strategy(symbols)
        results = {}
        
        # Fetch quotes
        for symbol in strategy['fetch_quotes']:
            quote = self.get_quote(symbol)
            if quote:
                results[symbol] = {'quote': quote}
        
        # Fetch news
        for symbol in strategy['fetch_news']:
            news = self.get_news_sentiment(symbol)
            if news and symbol in results:
                results[symbol]['news'] = news
        
        # Fetch technical
        for symbol in strategy['fetch_technical']:
            tech = self.get_technical_indicator(symbol)
            if tech and symbol in results:
                results[symbol]['technical'] = tech
        
        return results
    
    def get_status(self):
        """Get API usage status"""
        return self.api_manager.get_usage_summary()

if __name__ == "__main__":
    # Test the API manager
    manager = APIManager()
    
    print("API Usage Manager Test")
    print("=" * 50)
    
    # Show current status
    summary = manager.get_usage_summary()
    print(f"\n📊 Current Status:")
    print(f"Date: {summary['date']}")
    print(f"Calls Used: {summary['calls_used']}/{manager.daily_limit}")
    print(f"Calls Remaining: {summary['calls_remaining']}")
    print(f"Usage: {summary['percentage_used']:.1f}%")
    
    # Show optimal allocation
    allocation = manager.optimize_daily_calls()
    
    # Test smart fetch strategy
    test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMD', 'INTC']
    strategy = manager.smart_fetch_strategy(test_symbols)
    
    print(f"\n📈 Smart Fetch Strategy for {len(test_symbols)} symbols:")
    print(f"Quotes: {strategy['fetch_quotes']}")
    print(f"News: {strategy['fetch_news']}")
    print(f"Technical: {strategy['fetch_technical']}")
    if strategy['skip_reason']:
        print(f"Reason: {strategy['skip_reason']}")