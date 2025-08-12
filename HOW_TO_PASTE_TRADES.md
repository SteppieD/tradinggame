# 📋 SUPER SIMPLE: Just Paste Your Trades to Claude Code!

## Option 1: Direct to Claude Code (Easiest!)

Just tell me in natural language:

> "I bought 50 shares of AAPL at $150.25 and sold 20 shares of TSLA at $800"

Or paste from your broker:

> "Here are my trades:
> Filled Buy 50 AAPL @ $150.25 at 09:35 AM
> Filled Sell 20 TSLA @ $800.00 at 10:45 AM"

**I'll automatically parse and record them for you!**

## Option 2: Use the PASTE_TRADES_HERE.py File

1. Open `PASTE_TRADES_HERE.py`
2. Paste your trades between the triple quotes
3. Run: `python PASTE_TRADES_HERE.py`

## Option 3: Command Line

```bash
python scripts/trade_parser.py
# Then paste your trades and press Enter twice
```

## Supported Formats (Paste Any of These)

✅ **From Your Broker:**
```
Filled Buy 50 AAPL @ $150.25 at 09:35 AM
Filled Sell 20 TSLA @ $800.00 at 10:45 AM
```

✅ **Simple Format:**
```
BUY 50 AAPL @ 150.25
SELL 20 TSLA at 800
```

✅ **Natural Language:**
```
Bought 50 shares of AAPL at $150.25
Sold 20 TSLA at 800 dollars
```

✅ **Mixed Formats (All Work!):**
```
AAPL 50 shares bought at 150.25
20 TSLA 800 SELL
Buy 100 SNDL @ $2.01
```

## What Happens Automatically

When you paste trades, the system will:
1. ✅ Parse all recognizable trades
2. ✅ Update your portfolio positions
3. ✅ Calculate P&L on any sells
4. ✅ Track slippage vs planned orders
5. ✅ Update the dashboard
6. ✅ Set stop losses (10% below entry)

## Example: Just Tell Claude Code

You: "I executed these trades today:
- Bought 49 SNDL at $2.01 at 9:35 AM
- Bought 19 ACB at $5.21 at 9:30 AM  
- Sold 10 SNDL at $2.05 at 10:30 AM
- Bought 3 OUST at $27.90 at 9:45 AM"

Claude Code: "I'll record all 4 trades and update your dashboard!"

## Current Portfolio Status

After your trades:
- **Cash**: $739.32
- **Positions**: 
  - 39 SNDL @ $2.01
  - 19 ACB @ $5.21
  - 3 OUST @ $27.90
- **Total Value**: $1,000.00

---

**That's it! Just paste your trades in any format and I'll handle the rest!**