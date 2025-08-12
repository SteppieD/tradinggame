#!/usr/bin/env python3

"""
PASTE YOUR TRADES HERE!
Just copy from your broker and paste between the triple quotes below.
Then run: python PASTE_TRADES_HERE.py
"""

# ============================================
# PASTE YOUR TRADES BETWEEN THE TRIPLE QUOTES
# ============================================

trades = """
PASTE YOUR TRADES HERE
"""

# ============================================
# DON'T MODIFY BELOW THIS LINE
# ============================================

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'scripts'))

from trade_parser import parse_and_record_trades

if __name__ == "__main__":
    if trades.strip() and trades.strip() != "PASTE YOUR TRADES HERE":
        parse_and_record_trades(trades)
    else:
        print("⚠️  Please paste your trades in the 'trades' variable above")
        print("\nExample formats you can paste:")
        print("  BUY 50 AAPL @ 150.25")
        print("  SOLD 25 TSLA at $800.50 at 2:30 PM")
        print("  Filled Buy 100 SNDL @ $2.01 at 09:35 AM")
        print("\nThen run this file again!")