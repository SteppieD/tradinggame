#!/usr/bin/env python3

"""
RBLX Short Strategy Analysis
If you can short in your account, here's the analysis
"""

import requests
import json
from datetime import datetime

def analyze_rblx_short_strategy():
    """Detailed short analysis for RBLX"""
    
    print("=" * 70)
    print("🔴 ROBLOX SHORT STRATEGY - URGENT ANALYSIS")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print()
    
    # Get current price
    API_KEY = 'YHZ4C9KFT5ZFZB21'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=RBLX&apikey={API_KEY}'
    
    print("Fetching RBLX data...")
    response = requests.get(url)
    data = response.json()
    
    current_price = 126.78  # From previous check
    if 'Global Quote' in data:
        quote = data['Global Quote']
        current_price = float(quote['05. price'])
        volume = int(quote['06. volume']) if quote['06. volume'] else 0
        print(f"Current Price: ${current_price:.2f}")
        print(f"Volume: {volume:,}")
    else:
        print(f"Current Price: ${current_price:.2f} (cached)")
    
    print()
    print("=" * 70)
    print("⚡ SHORT OPPORTUNITY ASSESSMENT:")
    print("=" * 70)
    
    print("\n📊 CURRENT SETUP:")
    print("-" * 50)
    print(f"Entry Price: ${current_price:.2f}")
    print(f"Already down: -2.12% today")
    print("Status: News may not be fully priced in yet")
    print()
    
    print("🎯 SHORT TARGETS & STOPS:")
    print("-" * 50)
    
    # Calculate levels
    stop_loss = round(current_price * 1.05, 2)  # 5% stop
    target1 = round(current_price * 0.90, 2)     # 10% profit
    target2 = round(current_price * 0.80, 2)     # 20% profit
    target3 = round(current_price * 0.70, 2)     # 30% profit
    
    print(f"STOP LOSS: ${stop_loss:.2f} (+5% from entry)")
    print(f"Target 1: ${target1:.2f} (-10% move)")
    print(f"Target 2: ${target2:.2f} (-20% move)")
    print(f"Target 3: ${target3:.2f} (-30% move)")
    print()
    
    print("📈 POSITION SIZING:")
    print("-" * 50)
    
    # With $0.45 cash, need to calculate based on margin or freed capital
    # Assuming you might free up capital or use margin
    max_risk = 100  # Max you're willing to lose
    shares_to_short = int(max_risk / (stop_loss - current_price))
    
    print(f"With $100 risk tolerance:")
    print(f"Shares to short: {shares_to_short}")
    print(f"Capital needed: ${shares_to_short * current_price:.2f}")
    print(f"Max loss if stopped: ${shares_to_short * (stop_loss - current_price):.2f}")
    print(f"Profit at Target 1: ${shares_to_short * (current_price - target1):.2f}")
    print(f"Profit at Target 2: ${shares_to_short * (current_price - target2):.2f}")
    print()
    
    print("=" * 70)
    print("⚠️ RISK FACTORS:")
    print("=" * 70)
    print()
    print("HIGH RISKS:")
    print("• Short squeeze potential (high short interest)")
    print("• News might be unsubstantiated")
    print("• RBLX has strong retail following")
    print("• Requires margin/borrowing costs")
    print("• Unlimited loss potential if wrong")
    print()
    
    print("CATALYSTS FOR SUCCESS:")
    print("• Official lawsuit filing")
    print("• Media coverage expansion")
    print("• Regulatory investigation announcement")
    print("• Major advertisers pulling out")
    print("• User exodus metrics")
    print()
    
    print("=" * 70)
    print("💰 CAPITAL REQUIREMENTS:")
    print("=" * 70)
    print()
    print("YOUR CURRENT SITUATION:")
    print(f"• Cash available: $0.45 (insufficient)")
    print(f"• Portfolio value: $1,043.32")
    print()
    print("OPTIONS TO GET CAPITAL:")
    print("1. Sell one position (not recommended - all are winning)")
    print("2. Use margin if available")
    print("3. Wait for news confirmation before acting")
    print("4. Paper trade it to track the thesis")
    print()
    
    print("=" * 70)
    print("📋 EXECUTION PLAN IF SHORTING:")
    print("=" * 70)
    print()
    print("ENTRY CRITERIA (Need 2 of 3):")
    print("□ News confirmed by major outlet")
    print("□ Stock breaks below $125 support")
    print("□ Volume spike above 2x average")
    print()
    print("POSITION MANAGEMENT:")
    print(f"1. Short {shares_to_short} shares at market")
    print(f"2. Set stop loss at ${stop_loss:.2f}")
    print(f"3. Take 1/3 profit at ${target1:.2f}")
    print(f"4. Take 1/3 profit at ${target2:.2f}")
    print(f"5. Let 1/3 ride to ${target3:.2f}")
    print()
    
    print("=" * 70)
    print("🎯 RECOMMENDATION:")
    print("=" * 70)
    print()
    print("AGGRESSIVE: Short 15-20 shares now")
    print(f"  • Risk: ~${15 * (stop_loss - current_price):.2f}")
    print(f"  • Reward: ~${15 * (current_price - target1):.2f} to ${15 * (current_price - target2):.2f}")
    print()
    print("CONSERVATIVE: Wait for confirmation")
    print("  • Monitor news flow today")
    print("  • Short on break below $125")
    print("  • Or skip if no confirmation by EOD")
    print()
    print("CURRENT ACTION: ")
    print("Given you have only $0.45 cash, you'd need to:")
    print("1. Free up capital by selling a position, OR")
    print("2. Use margin if available, OR")
    print("3. Track it without position for learning")
    print()
    
    print("⚡ IF YOU WANT TO ACT NOW:")
    print("-" * 50)
    print("Consider selling TDUP (smallest position, least profit)")
    print("This would free up ~$200 for the short")
    print("But you'd sacrifice a position with +24% upside")
    print()
    
    print("=" * 70)
    print("✅ FINAL VERDICT:")
    print("=" * 70)
    print("The setup is interesting but you're capital constrained.")
    print("Your current positions are working well (+4.33%).")
    print("Unless you have strong conviction, stay with winners.")
    print("=" * 70)

if __name__ == "__main__":
    analyze_rblx_short_strategy()