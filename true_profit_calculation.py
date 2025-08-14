#!/usr/bin/env python3

"""
True Profit Calculation - Including ALL Fees
Shows real returns after transaction costs
"""

from datetime import datetime

def calculate_true_profit():
    """Calculate actual profit including all transaction fees"""
    
    print("=" * 70)
    print("💰 TRUE PROFIT CALCULATION - WITH ALL FEES")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print()
    
    # Initial investment
    initial_cash = 1000.00
    
    # All transactions with fees
    transactions = [
        # Initial buys
        {"action": "BUY", "symbol": "CHPT", "shares": 26, "price": 10.7845, "fee": 6.95},
        {"action": "BUY", "symbol": "EVGO", "shares": 82, "price": 3.6271, "fee": 6.95},
        {"action": "BUY", "symbol": "FCEL", "shares": 97, "price": 4.05, "fee": 6.95},
        
        # FCEL sale
        {"action": "SELL", "symbol": "FCEL", "shares": 97, "price": 4.26, "fee": 6.95},
        
        # New buys today
        {"action": "BUY", "symbol": "TDUP", "shares": 19, "price": 10.45, "fee": 6.95},
        {"action": "BUY", "symbol": "FUBO", "shares": 55, "price": 3.67, "fee": 6.95}
    ]
    
    print("📝 ALL TRANSACTIONS:")
    print("-" * 70)
    
    total_fees = 0
    cash_remaining = initial_cash
    
    for t in transactions:
        if t["action"] == "BUY":
            cost = (t["shares"] * t["price"]) + t["fee"]
            cash_remaining -= cost
            total_fees += t["fee"]
            print(f"BUY  {t['symbol']:5} {t['shares']:3} @ ${t['price']:.4f} = ${t['shares'] * t['price']:.2f} + ${t['fee']:.2f} fee = ${cost:.2f}")
        else:  # SELL
            proceeds = (t["shares"] * t["price"]) - t["fee"]
            cash_remaining += proceeds
            total_fees += t["fee"]
            print(f"SELL {t['symbol']:5} {t['shares']:3} @ ${t['price']:.4f} = ${t['shares'] * t['price']:.2f} - ${t['fee']:.2f} fee = ${proceeds:.2f}")
    
    print()
    print(f"Total Fees Paid: ${total_fees:.2f}")
    print(f"Cash Remaining: ${cash_remaining:.2f}")
    print()
    
    # Current positions and values
    current_positions = [
        {"symbol": "CHPT", "shares": 26, "entry": 10.7845, "current": 12.05},
        {"symbol": "EVGO", "shares": 82, "entry": 3.6271, "current": 3.94},
        {"symbol": "TDUP", "shares": 19, "entry": 10.45, "current": 10.51},
        {"symbol": "FUBO", "shares": 55, "entry": 3.67, "current": 3.76}
    ]
    
    print("=" * 70)
    print("📊 CURRENT PORTFOLIO VALUE:")
    print("=" * 70)
    print()
    
    total_current_value = 0
    total_entry_cost = 0
    
    for pos in current_positions:
        entry_cost = pos["shares"] * pos["entry"]
        current_value = pos["shares"] * pos["current"]
        position_pnl = current_value - entry_cost
        
        total_current_value += current_value
        total_entry_cost += entry_cost
        
        print(f"{pos['symbol']:5}: {pos['shares']:3} shares @ ${pos['current']:.2f} = ${current_value:.2f}")
    
    print(f"\nTotal Position Value: ${total_current_value:.2f}")
    print(f"Cash Balance: ${cash_remaining:.2f}")
    print("-" * 50)
    portfolio_value = total_current_value + cash_remaining
    print(f"Total Portfolio Value: ${portfolio_value:.2f}")
    print()
    
    print("=" * 70)
    print("💵 PROFIT CALCULATION:")
    print("=" * 70)
    print()
    
    # Method 1: Simple calculation
    simple_profit = portfolio_value - initial_cash
    simple_return = (simple_profit / initial_cash) * 100
    
    print("METHOD 1: Simple Net Profit")
    print("-" * 50)
    print(f"Starting Cash: ${initial_cash:.2f}")
    print(f"Current Value: ${portfolio_value:.2f}")
    print(f"Net Profit: ${simple_profit:.2f}")
    print(f"Return: {simple_return:.2f}%")
    print()
    
    # Method 2: Showing fee impact
    gross_position_gains = total_current_value - total_entry_cost
    fcel_gain_before_fees = (97 * 4.26) - (97 * 4.05)
    total_gross_gains = gross_position_gains + fcel_gain_before_fees
    
    print("METHOD 2: Gross vs Net")
    print("-" * 50)
    print(f"Gross Gains (before fees): ${total_gross_gains:.2f}")
    print(f"Total Fees Paid: -${total_fees:.2f}")
    print(f"Net Profit (after fees): ${simple_profit:.2f}")
    print(f"Fees ate {(total_fees/total_gross_gains*100):.1f}% of gross profits")
    print()
    
    # Method 3: If you had to sell everything today
    exit_fees = len(current_positions) * 6.95
    if_sold_today = portfolio_value - exit_fees
    if_sold_profit = if_sold_today - initial_cash
    if_sold_return = (if_sold_profit / initial_cash) * 100
    
    print("METHOD 3: If You Sold Everything Now")
    print("-" * 50)
    print(f"Current Portfolio: ${portfolio_value:.2f}")
    print(f"Exit Fees (4 sells): -${exit_fees:.2f}")
    print(f"Net if Liquidated: ${if_sold_today:.2f}")
    print(f"Profit if Liquidated: ${if_sold_profit:.2f}")
    print(f"Return if Liquidated: {if_sold_return:.2f}%")
    print()
    
    print("=" * 70)
    print("✅ ANSWER TO YOUR QUESTION:")
    print("=" * 70)
    print()
    print(f"YES, the +${simple_profit:.2f} ({simple_return:.2f}%) profit")
    print("ALREADY INCLUDES all transaction fees!")
    print()
    print("You've paid $41.70 in fees so far (6 trades)")
    print(f"Your ACTUAL profit after fees is ${simple_profit:.2f}")
    print()
    print("If you sold everything right now:")
    print(f"You'd pay another ${exit_fees:.2f} in fees")
    print(f"And walk away with ${if_sold_profit:.2f} profit ({if_sold_return:.2f}%)")
    print("=" * 70)

if __name__ == "__main__":
    calculate_true_profit()