import os
import sys
sys.path.append('scripts')
from alpha_vantage_client import AlphaVantageClient
import json
from datetime import datetime
import yfinance as yf

client = AlphaVantageClient()

# Analyze our three target stocks
stocks = ['SNDL', 'ACB', 'OUST']
analysis_results = {}

print("=" * 60)
print("DEEP MARKET RESEARCH FOR FIRST TRADES")
print("=" * 60)

for symbol in stocks:
    print(f'\n📊 Analyzing {symbol}...')
    print("-" * 40)
    
    # Get yfinance data for real-time info
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    # Get sentiment if available
    sentiment = client.get_news_sentiment(symbol)
    if sentiment:
        print(f'📰 News Sentiment:')
        if isinstance(sentiment, list) and len(sentiment) > 0:
            # Handle list format
            print(f'  Recent Articles: {len(sentiment)}')
            for article in sentiment[:2]:  # Show first 2 articles
                if isinstance(article, dict):
                    print(f'    • {article.get("title", "N/A")[:70]}')
                    print(f'      Sentiment: {article.get("overall_sentiment_score", "N/A")}')
        elif isinstance(sentiment, dict):
            # Handle dict format
            print(f'  Overall Score: {sentiment.get("overall_score", "N/A")}')
            print(f'  Sentiment Label: {sentiment.get("overall_label", "N/A")}')
            if 'articles' in sentiment:
                print(f'  Recent Articles: {len(sentiment["articles"])}')
                for article in sentiment['articles'][:2]:
                    print(f'    • {article.get("title", "N/A")[:70]}')
                    print(f'      Sentiment: {article.get("sentiment_score", "N/A")}')
    else:
        print(f'📰 News Sentiment: Limited data available')
    
    # Get quote data
    quote = client.get_quote(symbol)
    if quote:
        print(f'\n💹 Quote Data:')
        print(f'  Price: ${quote.get("price", "N/A")}')
        print(f'  Change: {quote.get("change_percent", "N/A")}')
        print(f'  Volume: {quote.get("volume", "N/A"):,}' if quote.get("volume") else '  Volume: N/A')
    
    # Get company fundamentals from yfinance
    print(f'\n🏢 Company Info ({symbol}):')
    print(f'  Sector: {info.get("sector", "N/A")}')
    print(f'  Industry: {info.get("industry", "N/A")}')
    print(f'  Market Cap: ${info.get("marketCap", 0):,}')
    print(f'  52W High: ${info.get("fiftyTwoWeekHigh", "N/A")}')
    print(f'  52W Low: ${info.get("fiftyTwoWeekLow", "N/A")}')
    
    # Get recent price action
    hist = ticker.history(period="1mo")
    if not hist.empty:
        recent_volatility = (hist['High'] - hist['Low']).mean() / hist['Close'].mean() * 100
        print(f'  Recent Volatility: {recent_volatility:.2f}%')
    
    analysis_results[symbol] = {
        'sentiment': sentiment,
        'quote': quote,
        'info': {
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'marketCap': info.get('marketCap'),
            '52wHigh': info.get('fiftyTwoWeekHigh'),
            '52wLow': info.get('fiftyTwoWeekLow')
        },
        'timestamp': datetime.now().isoformat()
    }

# Save analysis
with open('data/research_analysis.json', 'w') as f:
    json.dump(analysis_results, f, indent=2, default=str)

print('\n' + '=' * 60)
print('FINAL TRADE RECOMMENDATIONS')
print('=' * 60)

# Load our screening results for technical signals
with open('data/screening_results.json', 'r') as f:
    screening = json.load(f)

recommendations = []

for stock in screening['results'][:3]:  # Top 3 from screening
    symbol = stock['symbol']
    
    print(f'\n🎯 {symbol}:')
    
    # Technical signals
    tech_signal = stock['technical_signal']
    tech_confidence = stock['technical_confidence']
    
    # Price action
    week_change = stock['week_change']
    volume_spike = stock['volume_spike']
    
    # Support/Resistance
    fib_support = stock['fibonacci_support']['price']
    fib_resistance = stock['fibonacci_resistance']['price']
    current_price = stock['price']
    
    # Risk assessment
    risk_reward = (fib_resistance - current_price) / (current_price - fib_support) if current_price > fib_support else 0
    
    print(f'  Technical: {tech_signal} (Confidence: {tech_confidence}%)')
    print(f'  Momentum: +{week_change:.1f}% week, Volume spike: {volume_spike:.0f}%')
    print(f'  Support: ${fib_support:.2f} | Current: ${current_price:.2f} | Resistance: ${fib_resistance:.2f}')
    print(f'  Risk/Reward Ratio: {risk_reward:.2f}')
    
    # Decision logic
    if symbol == 'SNDL':
        print(f'  ⚠️ WARNING: Despite momentum, technical signal is STRONG_SELL')
        print(f'  📉 Cannabis sector volatility, overleveraged retail interest')
        print(f'  ❌ RECOMMENDATION: SKIP - Wait for pullback to $1.82 support')
        recommendations.append({'symbol': symbol, 'action': 'SKIP', 'reason': 'Technical divergence'})
    elif symbol == 'ACB':
        print(f'  ⚠️ CAUTION: Neutral technical signal despite volume')
        print(f'  📊 Cannabis sector following SNDL momentum')
        print(f'  ⏸️ RECOMMENDATION: WAIT - Monitor for break above $5.34')
        recommendations.append({'symbol': symbol, 'action': 'WAIT', 'reason': 'Neutral technicals'})
    elif symbol == 'OUST':
        print(f'  ✅ STRONG: STRONG_BUY signal with good momentum')
        print(f'  🚀 LiDAR technology sector strength')
        print(f'  ✅ RECOMMENDATION: BUY - Target $32.95, Stop at $27.48')
        recommendations.append({'symbol': symbol, 'action': 'BUY', 'reason': 'Strong technicals + sector'})

print('\n' + '=' * 60)
print('ALTERNATIVE PICKS FROM SCREENING')
print('=' * 60)

# Look at other strong candidates
alternatives = ['CHPT', 'EVGO', 'FCEL']
for symbol in alternatives:
    for stock in screening['results']:
        if stock['symbol'] == symbol:
            print(f'\n💡 {symbol} ({stock["sector"]}):')
            print(f'  Signal: {stock["technical_signal"]} | Price: ${stock["price"]}')
            print(f'  Week Change: {stock["week_change"]:.1f}%')
            print(f'  Support: ${stock["fibonacci_support"]["price"]:.2f}')
            if stock['technical_signal'] in ['STRONG_BUY', 'BUY']:
                print(f'  ✅ Good alternative candidate')

print('\n' + '=' * 60)
print('CAPITAL ALLOCATION STRATEGY')
print('=' * 60)
print('\nWith $1,000 starting capital:')
print('1. OUST: $300 (3 shares @ ~$28) - High conviction')
print('2. CHPT: $200 (18 shares @ ~$11) - EV infrastructure play')
print('3. EVGO: $200 (56 shares @ ~$3.56) - EV charging network')
print('4. FCEL: $100 (24 shares @ ~$4.07) - Clean energy')
print('5. Cash Reserve: $200 - For opportunities/averaging down')
print('\nThis provides diversification across clean tech sectors')
print('while avoiding overheated cannabis stocks.')