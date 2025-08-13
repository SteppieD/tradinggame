#!/usr/bin/env python3

# Calculate exact cash balance
initial = 1000.00
trades = [
    (26, 10.7845),  # CHPT
    (82, 3.6271),   # EVGO
    (97, 4.05)      # FCEL
]
fees = 6.95 * 3  # 3 trades

total_spent = sum(qty * price for qty, price in trades) + fees
cash_remaining = initial - total_spent

print(f'Initial balance: ${initial:.2f}')
print(f'CHPT: 26 × $10.7845 = ${26 * 10.7845:.2f}')
print(f'EVGO: 82 × $3.6271 = ${82 * 3.6271:.2f}')
print(f'FCEL: 97 × $4.05 = ${97 * 4.05:.2f}')
print(f'Total spent on shares: ${sum(qty * price for qty, price in trades):.2f}')
print(f'Total fees (3 × $6.95): ${fees:.2f}')
print(f'Total spent: ${total_spent:.2f}')
print(f'Cash remaining: ${cash_remaining:.2f}')