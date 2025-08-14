#!/usr/bin/env python3

"""
Get current prices for TDUP and FUBO
"""

import requests
import json
import time
from datetime import datetime

def get_new_stock_prices():
    """Get current prices for new positions"""
    
    API_KEY = 'YHZ4C9KFT5ZFZB21'
    
    print("Fetching TDUP and FUBO prices...")
    print()
    
    symbols = ['TDUP', 'FUBO']
    prices = {}
    
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        
        if 'Global Quote' in data:
            quote = data['Global Quote']
            price = float(quote['05. price'])
            change = float(quote['09. change']) if quote['09. change'] else 0
            change_pct = quote['10. change percent'].replace('%', '') if quote['10. change percent'] else '0'
            
            prices[symbol] = {
                'price': price,
                'change': change,
                'change_percent': change_pct
            }
            
            print(f"{symbol}: ${price:.2f} ({change_pct}%)")
        
        # Rate limit
        if symbol != symbols[-1]:
            print("Rate limiting: waiting 12 seconds...")
            time.sleep(12)
    
    return prices

if __name__ == "__main__":
    prices = get_new_stock_prices()
    print()
    print("Prices fetched successfully!")