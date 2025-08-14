#!/usr/bin/env python3

"""
RBLX Put Spread - Exact Details for Order Entry
Current pricing and dates for the trade
"""

from datetime import datetime, timedelta

def put_spread_order_details():
    """Exact details for RBLX put spread order"""
    
    print("=" * 70)
    print("📋 RBLX PUT SPREAD - EXACT ORDER DETAILS")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print()
    
    # RBLX current data
    current_price = 126.78
    
    print("📊 CURRENT RBLX STATUS:")
    print("-" * 50)
    print(f"Stock Price: ${current_price:.2f}")
    print(f"Day Change: -$2.77 (-2.12%)")
    print("Volume: 7.7M (elevated)")
    print()
    
    print("=" * 70)
    print("📅 EXPIRATION DATE:")
    print("=" * 70)
    print()
    print("SEPTEMBER 19, 2025 (Monthly expiration)")
    print(f"Days to expiration: 36")
    print("This is the standard monthly option")
    print()
    
    print("=" * 70)
    print("💰 ESTIMATED PRICING (Based on current IV):")
    print("=" * 70)
    print()
    
    print("$125 PUT (September 19, 2025):")
    print("-" * 50)
    print("Estimated Ask: $4.10 - $4.30")
    print("Estimated Bid: $3.90 - $4.10")
    print("Mid Price: ~$4.10")
    print("Cost for 2 contracts: ~$820")
    print()
    
    print("$115 PUT (September 19, 2025):")
    print("-" * 50)
    print("Estimated Ask: $1.60 - $1.80")
    print("Estimated Bid: $1.40 - $1.60")
    print("Mid Price: ~$1.60")
    print("Credit for 2 contracts: ~$320")
    print()
    
    print("NET DEBIT FOR SPREAD:")
    print("-" * 50)
    print("Buy 2x $125 Put: -$820")
    print("Sell 2x $115 Put: +$320")
    print("TOTAL COST: ~$500")
    print()
    
    print("=" * 70)
    print("📝 HOW TO PLACE THE ORDER:")
    print("=" * 70)
    print()
    
    print("STEP 1: Check current prices")
    print("-" * 50)
    print("• Go to your broker's option chain")
    print("• Select RBLX")
    print("• Choose September 19, 2025 expiration")
    print("• Look at $125 and $115 puts")
    print()
    
    print("STEP 2: Enter as a SPREAD order")
    print("-" * 50)
    print("Order Type: Vertical Put Spread")
    print("Quantity: 2")
    print("Buy: $125 Put")
    print("Sell: $115 Put")
    print("Expiration: September 19, 2025")
    print("Net Debit Limit: $2.50 per spread")
    print()
    
    print("STEP 3: Order entry format")
    print("-" * 50)
    print("Most brokers will show it as:")
    print("'Buy 2 RBLX SEP19'25 125/115 Put Spread'")
    print("or")
    print("'Buy 2 RBLX 09/19/25 125P/115P Vertical'")
    print()
    
    print("=" * 70)
    print("⚠️ IMPORTANT PRICING NOTES:")
    print("=" * 70)
    print()
    print("• Prices will vary based on current IV")
    print("• If spread costs more than $2.75, wait")
    print("• If spread costs less than $2.25, good deal")
    print("• Don't chase if market moves against you")
    print()
    
    print("ACCEPTABLE PRICE RANGE:")
    print("• Best case: $2.25 debit ($450 total)")
    print("• Target: $2.50 debit ($500 total)")
    print("• Max pay: $2.75 debit ($550 total)")
    print()
    
    print("=" * 70)
    print("🎯 FINAL ORDER INSTRUCTIONS:")
    print("=" * 70)
    print()
    print("EXACT ORDER TO PLACE:")
    print("-" * 50)
    print("Action: BUY TO OPEN")
    print("Quantity: 2 spreads")
    print("Type: Vertical Put Spread")
    print()
    print("Long Leg: Buy 2x RBLX Sep 19 '25 $125 Put")
    print("Short Leg: Sell 2x RBLX Sep 19 '25 $115 Put")
    print()
    print("Order Type: LIMIT")
    print("Limit Price: $2.50 debit (per spread)")
    print("Total Cost: $500")
    print("Duration: Day (or GTC if you prefer)")
    print()
    
    print("=" * 70)
    print("📱 WHAT YOU'LL SEE IN YOUR ACCOUNT:")
    print("=" * 70)
    print()
    print("After fill:")
    print("• Position: +2 RBLX Sep125P")
    print("• Position: -2 RBLX Sep115P")
    print("• Cash debit: $500")
    print("• Max profit: $1,500 (at RBLX $115 or below)")
    print("• Max loss: $500 (at RBLX $125 or above)")
    print("• Break-even: RBLX at $122.50")
    print()
    
    print("=" * 70)
    print("✅ READY TO TRADE:")
    print("=" * 70)
    print()
    print("You need:")
    print("• $500 cash in account")
    print("• Options trading approval")
    print("• Spread trading enabled")
    print()
    print("The trade:")
    print("• Risks $500 maximum")
    print("• Makes $1,500 maximum")
    print("• 3:1 reward to risk")
    print("• Expires September 19, 2025")
    print("=" * 70)

if __name__ == "__main__":
    put_spread_order_details()