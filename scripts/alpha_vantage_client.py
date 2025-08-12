#!/usr/bin/env python3

"""
Alpha Vantage API Client
Provides real-time and historical market data
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import time

class AlphaVantageClient:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        
        # Load environment variables
        load_dotenv(self.base_path / '.env')
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'EP1KVY5VZXBHMOZ8')
        
        self.base_url = 'https://www.alphavantage.co/query'
        self.cache_path = self.base_path / 'data' / 'cache' / 'alphavantage'
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting (5 calls per minute for free tier)
        self.last_call_time = 0
        self.min_call_interval = 12  # seconds between calls
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_call_interval:
            sleep_time = self.min_call_interval - time_since_last_call
            print(f"Rate limiting: waiting {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
    
    def _make_request(self, params):
        """Make API request with caching"""
        params['apikey'] = self.api_key
        
        # Create cache key
        cache_key = '_'.join([f"{k}_{v}" for k, v in sorted(params.items()) if k != 'apikey'])
        cache_file = self.cache_path / f"{cache_key}_{datetime.now().date()}.json"
        
        # Check cache (24 hour cache for most data)
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # Rate limit
        self._rate_limit()
        
        # Make request
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                print(f"API Error: {data['Error Message']}")
                return None
            elif 'Note' in data:
                print(f"API Note: {data['Note']}")
                return None
            
            # Cache successful response
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return data
        else:
            print(f"Request failed with status {response.status_code}")
            return None
    
    def get_quote(self, symbol):
        """Get real-time quote for a symbol"""
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        
        data = self._make_request(params)
        
        if data and 'Global Quote' in data:
            quote = data['Global Quote']
            return {
                'symbol': quote.get('01. symbol'),
                'price': float(quote.get('05. price', 0)),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day'),
                'previous_close': float(quote.get('08. previous close', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': quote.get('10. change percent', '0%').rstrip('%')
            }
        
        return None
    
    def get_intraday(self, symbol, interval='5min'):
        """Get intraday data"""
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': 'compact'
        }
        
        data = self._make_request(params)
        
        if data:
            time_series_key = f'Time Series ({interval})'
            if time_series_key in data:
                return self._parse_time_series(data[time_series_key])
        
        return None
    
    def get_daily(self, symbol, outputsize='compact'):
        """Get daily price data"""
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize  # 'compact' = 100 days, 'full' = 20+ years
        }
        
        data = self._make_request(params)
        
        if data and 'Time Series (Daily)' in data:
            return self._parse_time_series(data['Time Series (Daily)'])
        
        return None
    
    def get_technical_indicator(self, symbol, indicator='RSI', interval='daily', time_period=14):
        """Get technical indicators"""
        params = {
            'function': indicator,
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        
        if data:
            # Find the technical analysis key
            for key in data.keys():
                if 'Technical Analysis' in key:
                    return self._parse_technical_data(data[key])
        
        return None
    
    def get_sma(self, symbol, interval='daily', time_period=20):
        """Get Simple Moving Average"""
        return self.get_technical_indicator(symbol, 'SMA', interval, time_period)
    
    def get_ema(self, symbol, interval='daily', time_period=20):
        """Get Exponential Moving Average"""
        return self.get_technical_indicator(symbol, 'EMA', interval, time_period)
    
    def get_rsi(self, symbol, interval='daily', time_period=14):
        """Get Relative Strength Index"""
        return self.get_technical_indicator(symbol, 'RSI', interval, time_period)
    
    def get_macd(self, symbol, interval='daily'):
        """Get MACD"""
        params = {
            'function': 'MACD',
            'symbol': symbol,
            'interval': interval,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        
        if data and 'Technical Analysis: MACD' in data:
            return self._parse_technical_data(data['Technical Analysis: MACD'])
        
        return None
    
    def get_bbands(self, symbol, interval='daily', time_period=20):
        """Get Bollinger Bands"""
        params = {
            'function': 'BBANDS',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        
        if data and 'Technical Analysis: BBANDS' in data:
            return self._parse_technical_data(data['Technical Analysis: BBANDS'])
        
        return None
    
    def get_company_overview(self, symbol):
        """Get company fundamental data"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        
        data = self._make_request(params)
        
        if data and 'Symbol' in data:
            return {
                'symbol': data.get('Symbol'),
                'name': data.get('Name'),
                'description': data.get('Description'),
                'sector': data.get('Sector'),
                'industry': data.get('Industry'),
                'market_cap': int(data.get('MarketCapitalization', 0)),
                'pe_ratio': float(data.get('PERatio', 0) or 0),
                'peg_ratio': float(data.get('PEGRatio', 0) or 0),
                'book_value': float(data.get('BookValue', 0) or 0),
                'dividend_yield': float(data.get('DividendYield', 0) or 0),
                'eps': float(data.get('EPS', 0) or 0),
                'revenue_per_share': float(data.get('RevenuePerShareTTM', 0) or 0),
                'profit_margin': float(data.get('ProfitMargin', 0) or 0),
                '52_week_high': float(data.get('52WeekHigh', 0) or 0),
                '52_week_low': float(data.get('52WeekLow', 0) or 0),
                '50_day_ma': float(data.get('50DayMovingAverage', 0) or 0),
                '200_day_ma': float(data.get('200DayMovingAverage', 0) or 0),
                'shares_outstanding': int(data.get('SharesOutstanding', 0) or 0),
                'shares_float': int(data.get('SharesFloat', 0) or 0),
                'analyst_target': float(data.get('AnalystTargetPrice', 0) or 0)
            }
        
        return None
    
    def get_earnings(self, symbol):
        """Get earnings data"""
        params = {
            'function': 'EARNINGS',
            'symbol': symbol
        }
        
        data = self._make_request(params)
        
        if data:
            return {
                'annual_earnings': data.get('annualEarnings', []),
                'quarterly_earnings': data.get('quarterlyEarnings', [])
            }
        
        return None
    
    def get_news_sentiment(self, tickers=None, topics=None):
        """Get news and sentiment data"""
        params = {
            'function': 'NEWS_SENTIMENT'
        }
        
        if tickers:
            params['tickers'] = tickers
        if topics:
            params['topics'] = topics
        
        data = self._make_request(params)
        
        if data and 'feed' in data:
            news_items = []
            for item in data['feed'][:10]:  # Limit to 10 items
                news_items.append({
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'time_published': item.get('time_published'),
                    'summary': item.get('summary'),
                    'overall_sentiment_score': item.get('overall_sentiment_score'),
                    'overall_sentiment_label': item.get('overall_sentiment_label'),
                    'ticker_sentiment': item.get('ticker_sentiment', [])
                })
            
            return news_items
        
        return None
    
    def _parse_time_series(self, time_series):
        """Parse time series data"""
        parsed = []
        for date, values in sorted(time_series.items(), reverse=True)[:20]:  # Last 20 entries
            parsed.append({
                'date': date,
                'open': float(values.get('1. open', 0)),
                'high': float(values.get('2. high', 0)),
                'low': float(values.get('3. low', 0)),
                'close': float(values.get('4. close', 0)),
                'volume': int(values.get('5. volume', 0))
            })
        
        return parsed
    
    def _parse_technical_data(self, technical_data):
        """Parse technical indicator data"""
        parsed = []
        for date, values in sorted(technical_data.items(), reverse=True)[:20]:  # Last 20 entries
            entry = {'date': date}
            for key, value in values.items():
                entry[key] = float(value)
            parsed.append(entry)
        
        return parsed
    
    def get_market_movers(self):
        """Get top gainers and losers"""
        # Note: This requires a premium API key
        # For free tier, we'll return None
        print("Market movers requires premium API key")
        return None
    
    def analyze_symbol(self, symbol):
        """Comprehensive analysis of a symbol"""
        print(f"\nAnalyzing {symbol} with Alpha Vantage...")
        
        analysis = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat()
        }
        
        # Get quote
        quote = self.get_quote(symbol)
        if quote:
            analysis['quote'] = quote
            print(f"Current Price: ${quote['price']:.2f}")
            print(f"Change: {quote['change']:.2f} ({quote['change_percent']}%)")
        
        # Get company overview
        overview = self.get_company_overview(symbol)
        if overview:
            analysis['fundamentals'] = overview
            print(f"Market Cap: ${overview['market_cap']:,}")
            print(f"P/E Ratio: {overview['pe_ratio']}")
            print(f"52W Range: ${overview['52_week_low']:.2f} - ${overview['52_week_high']:.2f}")
        
        # Get technical indicators
        rsi = self.get_rsi(symbol)
        if rsi and len(rsi) > 0:
            analysis['rsi'] = rsi[0]['RSI']
            print(f"RSI: {rsi[0]['RSI']:.2f}")
        
        # Get news sentiment
        news = self.get_news_sentiment(symbol)
        if news:
            analysis['news'] = news[:3]  # Top 3 news items
            if news:
                avg_sentiment = sum(float(n['overall_sentiment_score']) for n in news if n['overall_sentiment_score']) / len(news)
                print(f"News Sentiment: {avg_sentiment:.3f}")
        
        return analysis

if __name__ == "__main__":
    client = AlphaVantageClient()
    
    # Test with a symbol
    test_symbol = 'AAPL'
    
    print(f"Testing Alpha Vantage API with {test_symbol}")
    print("=" * 50)
    
    # Get quote
    quote = client.get_quote(test_symbol)
    if quote:
        print(f"\nQuote: ${quote['price']:.2f} ({quote['change_percent']}%)")
    
    # Get company overview
    overview = client.get_company_overview(test_symbol)
    if overview:
        print(f"Company: {overview['name']}")
        print(f"Sector: {overview['sector']}")
        print(f"Market Cap: ${overview['market_cap']:,}")
    
    # Full analysis
    analysis = client.analyze_symbol(test_symbol)
    
    print("\nFull analysis saved to cache")