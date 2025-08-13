#!/usr/bin/env python3

"""
Process FCEL Sale - August 13, 2025
Sold 97 shares at $4.26
"""

import json
from datetime import datetime

def process_fcel_sale():
    """Update portfolio after FCEL sale"""
    
    # Sale details
    SYMBOL = 'FCEL'
    QUANTITY = 97
    SALE_PRICE = 4.26
    COMMISSION = 6.95
    
    # Load portfolio
    with open('data/portfolio.json', 'r') as f:
        portfolio = json.load(f)
    
    # Find FCEL position
    fcel_position = next((p for p in portfolio['positions'] if p['symbol'] == SYMBOL), None)
    
    if not fcel_position:
        print("ERROR: FCEL position not found!")
        return
    
    # Calculate profit/loss
    entry_price = fcel_position['entry_price']
    entry_cost = QUANTITY * entry_price
    sale_proceeds_gross = QUANTITY * SALE_PRICE
    sale_proceeds_net = sale_proceeds_gross - COMMISSION
    
    realized_pnl = sale_proceeds_net - entry_cost
    realized_pnl_pct = (realized_pnl / entry_cost) * 100
    
    print("=" * 70)
    print("💰 FCEL SALE EXECUTED")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print()
    print("📊 TRANSACTION DETAILS:")
    print("-" * 50)
    print(f"Symbol: {SYMBOL}")
    print(f"Quantity: {QUANTITY} shares")
    print(f"Sale Price: ${SALE_PRICE:.2f}")
    print(f"Gross Proceeds: ${sale_proceeds_gross:.2f}")
    print(f"Commission: -${COMMISSION:.2f}")
    print(f"Net Proceeds: ${sale_proceeds_net:.2f}")
    print()
    print("💵 PROFIT CALCULATION:")
    print("-" * 50)
    print(f"Entry Price: ${entry_price:.4f}")
    print(f"Entry Cost: ${entry_cost:.2f}")
    print(f"Sale Price: ${SALE_PRICE:.2f}")
    print(f"Realized P&L: ${realized_pnl:.2f} ({realized_pnl_pct:+.2f}%)")
    
    # Update portfolio
    # Remove FCEL from positions
    portfolio['positions'] = [p for p in portfolio['positions'] if p['symbol'] != SYMBOL]
    
    # Update cash balance
    old_cash = portfolio['cash_balance']
    new_cash = old_cash + sale_proceeds_net
    portfolio['cash_balance'] = new_cash
    
    print()
    print("💼 PORTFOLIO UPDATE:")
    print("-" * 50)
    print(f"Previous Cash: ${old_cash:.2f}")
    print(f"Sale Proceeds: +${sale_proceeds_net:.2f}")
    print(f"New Cash Balance: ${new_cash:.2f}")
    
    # Calculate remaining portfolio value
    remaining_value = new_cash
    for pos in portfolio['positions']:
        print(f"\nRemaining Position: {pos['symbol']}")
        print(f"  Quantity: {pos['quantity']} shares")
        print(f"  Entry: ${pos['entry_price']:.4f}")
    
    # Save updated portfolio
    portfolio['last_updated'] = datetime.now().isoformat()
    
    with open('data/portfolio.json', 'w') as f:
        json.dump(portfolio, f, indent=2)
    
    # Add to trades history
    trade_record = {
        'date': datetime.now().isoformat(),
        'symbol': SYMBOL,
        'action': 'SELL',
        'quantity': QUANTITY,
        'price': SALE_PRICE,
        'commission': COMMISSION,
        'proceeds': sale_proceeds_net,
        'realized_pnl': realized_pnl,
        'realized_pnl_pct': realized_pnl_pct
    }
    
    # Append to trades history CSV
    with open('data/trades_history.csv', 'a') as f:
        f.write(f"\n{trade_record['date']},{SYMBOL},{QUANTITY},{SALE_PRICE},SELL,{sale_proceeds_net},{realized_pnl},{new_cash}")
    
    print()
    print("=" * 70)
    print("📈 PERFORMANCE SUMMARY:")
    print("=" * 70)
    
    # Calculate total portfolio performance
    initial_investment = 1000.00
    
    # Total fees paid (3 buys + 1 sell = 4 trades)
    total_fees = 6.95 * 4
    
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Current Cash: ${new_cash:.2f}")
    print(f"Realized P&L (FCEL): ${realized_pnl:.2f} ({realized_pnl_pct:+.2f}%)")
    print(f"Total Fees Paid: ${total_fees:.2f}")
    print()
    print("🎯 NEXT STEPS:")
    print("-" * 50)
    print("1. Update stop-loss orders for remaining positions (CHPT, EVGO)")
    print("2. Cash available for new opportunities: ${:.2f}".format(new_cash))
    print("3. Consider waiting for market pullback before re-entering")
    print()
    print("✅ Sale processed successfully!")
    print("=" * 70)
    
    # Save sale summary
    sale_summary = {
        'date': datetime.now().isoformat(),
        'symbol': SYMBOL,
        'quantity': QUANTITY,
        'sale_price': SALE_PRICE,
        'entry_price': entry_price,
        'realized_pnl': realized_pnl,
        'realized_pnl_pct': realized_pnl_pct,
        'commission': COMMISSION,
        'net_proceeds': sale_proceeds_net,
        'new_cash_balance': new_cash
    }
    
    with open('data/fcel_sale_summary.json', 'w') as f:
        json.dump(sale_summary, f, indent=2)
    
    return sale_summary

if __name__ == "__main__":
    process_fcel_sale()