#!/usr/bin/env python3

"""
Check New Stock Opportunities via Alpha Vantage
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from scripts.alpha_vantage_client import AlphaVantageClient
import json
from datetime import datetime

def check_new_stocks():
    """Get quotes for potential new positions"""
    
    client = AlphaVantageClient()
    
    # Stocks to check
    symbols = ['TDUP', 'FUBO']
    
    print("=" * 70)
    print("📊 NEW STOCK ANALYSIS - Via Alpha Vantage")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print()
    
    stock_data = {}
    
    for symbol in symbols:
        print(f"\n🔍 Checking {symbol}...")
        try:
            quote = client.get_quote(symbol)
            if quote:
                price = float(quote.get('price', 0))
                change_pct = quote.get('change_percent', '0%')
                
                stock_data[symbol] = {
                    'price': price,
                    'change_percent': change_pct,
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"   Current Price: ${price:.2f}")
                print(f"   Daily Change: {change_pct}")
                
                # Calculate position sizing
                position_size = 200  # Target per position
                shares = int(position_size / price)
                actual_cost = shares * price
                
                print(f"   With $200 budget:")
                print(f"      Can buy: {shares} shares")
                print(f"      Total cost: ${actual_cost:.2f}")
                print(f"      Plus commission: ${actual_cost + 6.95:.2f}")
                
        except Exception as e:
            print(f"   ❌ Error getting {symbol}: {e}")
    
    # Compare to our existing holdings
    print("\n" + "=" * 50)
    print("📈 COMPARISON TO CURRENT HOLDINGS:")
    print("-" * 50)
    
    # Load our current positions
    with open('data/latest_prices.json', 'r') as f:
        current = json.load(f)
    
    print(f"CHPT: ${current['CHPT']['price']:.2f} ({current['CHPT']['change_percent']}%)")
    print(f"EVGO: ${current['EVGO']['price']:.2f} ({current['EVGO']['change_percent']}%)")
    
    if 'TDUP' in stock_data:
        print(f"TDUP: ${stock_data['TDUP']['price']:.2f} (NEW)")
    if 'FUBO' in stock_data:
        print(f"FUBO: ${stock_data['FUBO']['price']:.2f} (NEW)")
    
    # Portfolio impact
    print("\n" + "=" * 50)
    print("💼 PORTFOLIO IMPACT:")
    print("-" * 50)
    
    cash_available = 414.75
    print(f"Current Cash: ${cash_available:.2f}")
    
    total_cost = 0
    if 'TDUP' in stock_data and 'FUBO' in stock_data:
        tdup_shares = int(200 / stock_data['TDUP']['price'])
        fubo_shares = int(200 / stock_data['FUBO']['price'])
        
        tdup_cost = tdup_shares * stock_data['TDUP']['price'] + 6.95
        fubo_cost = fubo_shares * stock_data['FUBO']['price'] + 6.95
        total_cost = tdup_cost + fubo_cost
        
        print(f"TDUP: {tdup_shares} shares = ${tdup_cost:.2f} (incl. fees)")
        print(f"FUBO: {fubo_shares} shares = ${fubo_cost:.2f} (incl. fees)")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Cash Remaining: ${cash_available - total_cost:.2f}")
    
    print("\n" + "=" * 70)
    print("💡 RECOMMENDATION:")
    print("=" * 70)
    
    if stock_data:
        print("Based on Alpha Vantage real-time data:")
        for symbol, data in stock_data.items():
            print(f"  • {symbol} at ${data['price']:.2f} - Confirm with your research")
    else:
        print("  ⚠️ Could not fetch prices - check Alpha Vantage API")
    
    print("\n📝 Next Steps:")
    print("  1. Review fundamentals one more time")
    print("  2. Check pre-market activity tomorrow")
    print("  3. Place limit orders slightly below current price")
    print("  4. Set stop losses immediately after fills")
    print("=" * 70)
    
    return stock_data

if __name__ == "__main__":
    check_new_stocks()