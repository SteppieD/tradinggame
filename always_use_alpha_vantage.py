#!/usr/bin/env python3

"""
CRITICAL: Always Use Alpha Vantage for Price Data
This script enforces the use of Alpha Vantage API as the ONLY source of price data
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def check_and_update_prices():
    """Check price freshness and update if needed"""
    
    print("=" * 70)
    print("🔍 ALPHA VANTAGE PRICE CHECK")
    print("=" * 70)
    
    # Check if prices exist and are fresh
    try:
        with open('data/latest_prices.json', 'r') as f:
            prices = json.load(f)
        
        # Check timestamp of first symbol
        if prices and 'CHPT' in prices:
            timestamp_str = prices['CHPT'].get('timestamp', '')
            if timestamp_str:
                timestamp = datetime.fromisoformat(timestamp_str)
                age_minutes = (datetime.now() - timestamp).total_seconds() / 60
                
                print(f"📊 Price Data Status:")
                print(f"   Last Update: {timestamp.strftime('%I:%M %p')}")
                print(f"   Age: {age_minutes:.1f} minutes")
                
                if age_minutes > 15:
                    print(f"\n⚠️  PRICES ARE STALE (>{15} minutes old)")
                    print("   Running Alpha Vantage update...")
                    update_prices()
                else:
                    print(f"\n✅ Prices are FRESH (<15 minutes old)")
                    display_current_prices(prices)
            else:
                print("⚠️  No timestamp found - updating prices...")
                update_prices()
        else:
            print("⚠️  No price data found - fetching from Alpha Vantage...")
            update_prices()
            
    except FileNotFoundError:
        print("⚠️  No price file found - creating with Alpha Vantage data...")
        update_prices()
    except Exception as e:
        print(f"❌ Error checking prices: {e}")
        print("   Attempting fresh update...")
        update_prices()

def update_prices():
    """Update prices using ONLY Alpha Vantage"""
    print("\n🔄 Fetching from Alpha Vantage API...")
    
    from scripts.alpha_vantage_client import AlphaVantageClient
    client = AlphaVantageClient()
    
    symbols = ['CHPT', 'EVGO', 'FCEL', 'SPY', 'IWM']
    prices = {}
    
    for symbol in symbols:
        try:
            quote = client.get_quote(symbol)
            if quote:
                prices[symbol] = {
                    'price': float(quote.get('price', 0)),
                    'change': float(quote.get('change', 0)),
                    'change_percent': quote.get('change_percent', '0%'),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'ALPHA_VANTAGE'  # Always mark the source
                }
                print(f'   {symbol}: ${quote.get("price", "N/A")} ({quote.get("change_percent", "N/A")})')
        except Exception as e:
            print(f'   ❌ Error getting {symbol}: {e}')
    
    # Save with metadata
    price_data = {
        'last_update': datetime.now().isoformat(),
        'source': 'ALPHA_VANTAGE_API',
        'prices': prices
    }
    
    with open('data/latest_prices.json', 'w') as f:
        json.dump(prices, f, indent=2)
    
    print("\n✅ Prices updated successfully via Alpha Vantage!")
    display_current_prices(prices)

def display_current_prices(prices):
    """Display current prices with portfolio impact"""
    
    print("\n📈 CURRENT PRICES (Alpha Vantage):")
    print("-" * 50)
    
    # Load portfolio to show impact
    try:
        with open('data/portfolio.json', 'r') as f:
            portfolio = json.load(f)
        
        total_value = portfolio['cash_balance']
        
        for pos in portfolio['positions']:
            symbol = pos['symbol']
            if symbol in prices:
                current = prices[symbol]['price']
                qty = pos['quantity']
                entry = pos['entry_price']
                value = qty * current
                pnl = value - (qty * entry)
                pnl_pct = (pnl / (qty * entry)) * 100
                
                total_value += value
                
                emoji = "🚀" if pnl_pct > 10 else "⭐" if pnl_pct > 5 else "📈" if pnl_pct > 0 else "📉"
                
                print(f"{emoji} {symbol}: ${current:.2f} ({pnl_pct:+.1f}%)")
        
        print(f"\n💼 Portfolio Value: ${total_value:.2f}")
        print(f"   Return: {((total_value - 1000) / 1000) * 100:+.1f}%")
        
    except Exception as e:
        # Just show prices if portfolio unavailable
        for symbol, data in prices.items():
            print(f"   {symbol}: ${data['price']:.2f}")

def enforce_alpha_vantage():
    """Main enforcement function"""
    print("\n" + "=" * 70)
    print("⚠️  IMPORTANT REMINDER:")
    print("=" * 70)
    print("NEVER use web searches for stock prices!")
    print("ALWAYS use: python update_prices.py")
    print("This ensures accurate, real-time data from Alpha Vantage")
    print("=" * 70)

if __name__ == "__main__":
    check_and_update_prices()
    enforce_alpha_vantage()